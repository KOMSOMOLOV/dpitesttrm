import asyncio
import aiohttp
import random
import time  # Добавляем импорт time
from typing import List, Dict
from protocols.http_proxy import HTTPProxyTester
from protocols.socks5_proxy import SOCKS5Tester
from utils.network_tools import get_random_user_agent

class ProxyHunter:
    def __init__(self):
        self.working_proxies = []
        self.bypass_proxies = []
        self.session = None
        
    async def init_session(self):
        timeout = aiohttp.ClientTimeout(total=10)
        self.session = aiohttp.ClientSession(timeout=timeout)
    
    async def scan_proxy_list(self, proxies: List[str]):
        """Сканирование списка прокси"""
        tasks = []
        for proxy in proxies:
            task = self.test_proxy(proxy)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if r and isinstance(r, dict) and r.get('working')]
    
    async def test_proxy(self, proxy: str) -> Dict:
        """Тестирование одного прокси"""
        try:
            if self.session is None:
                await self.init_session()
                
            # Тестирование HTTP
            http_tester = HTTPProxyTester()
            http_result = await http_tester.test_proxy(proxy, self.session)
            
            # Тестирование SOCKS5
            socks_tester = SOCKS5Tester()
            socks_result = await socks_tester.test_proxy(proxy, self.session)
            
            # Проверка обхода блокировок
            bypass_result = await self.test_bypass_capability(proxy)
            
            return {
                'proxy': proxy,
                'working': http_result['working'] or socks_result['working'],
                'protocols': {
                    'http': http_result,
                    'socks5': socks_result
                },
                'bypass': bypass_result,
                'speed': min(http_result.get('speed', 999), socks_result.get('speed', 999))
            }
            
        except Exception as e:
            return {'proxy': proxy, 'working': False, 'error': str(e)}
    
    async def test_bypass_capability(self, proxy: str) -> Dict:
        """Тестирование возможности обхода блокировок"""
        test_targets = [
            'https://www.google.com',
            'https://www.youtube.com', 
            'https://telegram.org',
            'https://api.telegram.org'
        ]
        
        results = {}
        for target in test_targets:
            try:
                async with self.session.get(
                    target,
                    proxy=f'http://{proxy}',
                    headers={'User-Agent': get_random_user_agent()},
                    timeout=10
                ) as response:
                    results[target] = response.status == 200
            except:
                results[target] = False
        
        return {
            'can_bypass': any(results.values()),
            'details': results
        }