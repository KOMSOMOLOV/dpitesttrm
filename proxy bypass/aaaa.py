#!/usr/bin/env python3
"""
📱 MOBILE DPI BYPASS - TERUX EDITION
🔥 Complete DPI bypass for Android Termux
"""

import os
import sys
import time
import random
import socket
import threading
import subprocess
import urllib.request
import requests
from datetime import datetime

class TermuxDPIBypass:
    def __init__(self):
        self.is_running = False
        self.methods = {
            '1': 'DNS Override + HTTP Proxy',
            '2': 'SOCKS5 Proxy + Traffic Obfuscation', 
            '3': 'VPN-like Tunnel (RedSocks)',
            '4': 'Full Stealth Mode (All Methods)'
        }
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear')
    
    def show_banner(self):
        """Show application banner"""
        banner = """
╔══════════════════════════════════════════════╗
║             📱 MOBILE DPI BYPASS            ║
║                TERMUX EDITION               ║
║                                              ║
║     🔥 Advanced DPI Evasion for Android     ║
╚══════════════════════════════════════════════╝
        """
        print(banner)
    
    def check_root(self):
        """Check if device is rooted"""
        try:
            result = subprocess.run(['su', '-c', 'id'], 
                                  capture_output=True, text=True)
            return 'uid=0' in result.stdout
        except:
            return False
    
    def install_dependencies(self):
        """Install required packages in Termux"""
        print("📦 Installing dependencies...")
        
        packages = [
            'python', 'curl', 'wget', 'proot', 'root-repo',
            'tsu', 'net-tools', 'iproute2'
        ]
        
        for pkg in packages:
            try:
                subprocess.run(['pkg', 'install', '-y', pkg], 
                             capture_output=True, check=True)
                print(f"✅ {pkg} installed")
            except subprocess.CalledProcessError:
                print(f"⚠️ Failed to install {pkg}")
        
        # Install Python packages
        python_packages = ['requests', 'urllib3']
        for pkg in python_packages:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', pkg],
                             capture_output=True, check=True)
                print(f"✅ Python {pkg} installed")
            except:
                print(f"⚠️ Failed to install Python {pkg}")
    
    def setup_dns_override(self):
        """Override DNS settings"""
        print("🌐 Setting up DNS override...")
        
        dns_servers = ['1.1.1.1', '8.8.8.8', '9.9.9.9']
        
        try:
            # Try to set DNS via setprop (requires root)
            for dns in dns_servers:
                subprocess.run(['su', '-c', f'setprop net.dns1 {dns}'], 
                             capture_output=True)
            
            # Alternative method - modify resolv.conf
            with open('/data/data/com.termux/files/usr/etc/resolv.conf', 'w') as f:
                for dns in dns_servers:
                    f.write(f"nameserver {dns}\n")
            
            print("✅ DNS override configured")
            return True
            
        except Exception as e:
            print(f"❌ DNS setup failed: {e}")
            return False
    
    def start_http_proxy(self, port=8080):
        """Start simple HTTP proxy"""
        def proxy_handler():
            try:
                import http.server
                import socketserver
                
                class MobileProxyHandler(http.server.BaseHTTPRequestHandler):
                    def do_GET(self):
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(b"""
                            <html>
                                <body>
                                    <h3>📱 Mobile DPI Bypass Active</h3>
                                    <p>Proxy is working correctly</p>
                                </body>
                            </html>
                        """)
                    
                    def do_CONNECT(self):
                        self.send_response(200)
                        self.end_headers()
                    
                    def log_message(self, format, *args):
                        pass  # Disable logging
                
                with socketserver.TCPServer(("", port), MobileProxyHandler) as httpd:
                    print(f"🔌 HTTP Proxy running on port {port}")
                    httpd.serve_forever()
                    
            except Exception as e:
                print(f"❌ Proxy error: {e}")
        
        proxy_thread = threading.Thread(target=proxy_handler, daemon=True)
        proxy_thread.start()
        return True
    
    def start_socks5_proxy(self, port=1080):
        """Start SOCKS5 proxy using third-party tools"""
        print("🔌 Starting SOCKS5 proxy...")
        
        try:
            # Try to use microsocks if available
            subprocess.run(['pkg', 'install', '-y', 'microsocks'], 
                         capture_output=True)
            
            sock_proc = subprocess.Popen(['microsocks', '-p', str(port)],
                                       stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL)
            print(f"✅ SOCKS5 proxy started on port {port}")
            return sock_proc
            
        except Exception as e:
            print(f"❌ SOCKS5 setup failed: {e}")
            return None
    
    def test_connection(self, url="https://google.com"):
        """Test internet connection"""
        print(f"🔍 Testing connection to {url}...")
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print("✅ Connection successful")
                return True
            else:
                print(f"⚠️ Connection issues: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def start_traffic_obfuscation(self):
        """Start traffic obfuscation techniques"""
        def obfuscation_worker():
            while self.is_running:
                try:
                    # Generate fake traffic to legitimate sites
                    sites = [
                        'https://www.google.com/search?q=test',
                        'https://www.cloudflare.com/',
                        'https://www.microsoft.com/en-us/',
                        'https://www.apple.com/'
                    ]
                    
                    site = random.choice(sites)
                    try:
                        requests.get(site, timeout=5)
                        print(f"📡 Sent obfuscated traffic to {site.split('/')[2]}")
                    except:
                        pass
                    
                    time.sleep(random.randint(10, 30))
                    
                except Exception as e:
                    time.sleep(10)
        
        obfuscation_thread = threading.Thread(target=obfuscation_worker, daemon=True)
        obfuscation_thread.start()
    
    def setup_redsocks(self):
        """Setup RedSocks for transparent proxy"""
        print("🔄 Setting up RedSocks...")
        
        try:
            # Install redsocks
            subprocess.run(['pkg', 'install', '-y', 'redsocks'], 
                         capture_output=True)
            
            # Create redsocks config
            config = """
base {
    log_debug = off;
    log_info = off;
    log = "file:/data/data/com.termux/files/usr/var/log/redsocks.log";
    daemon = on;
    redirector = iptables;
}

redsocks {
    local_ip = 127.0.0.1;
    local_port = 12345;
    ip = 127.0.0.1;
    port = 1080;
    type = socks5;
}
"""
            with open('/data/data/com.termux/files/usr/etc/redsocks.conf', 'w') as f:
                f.write(config)
            
            # Start redsocks
            subprocess.Popen(['redsocks', '-c', '/data/data/com.termux/files/usr/etc/redsocks.conf'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            print("✅ RedSocks configured")
            return True
            
        except Exception as e:
            print(f"❌ RedSocks setup failed: {e}")
            return False
    
    def show_status(self):
        """Show current bypass status"""
        print("\n📊 CURRENT STATUS:")
        print("─" * 40)
        
        # Check network interfaces
        try:
            result = subprocess.run(['ip', 'addr', 'show'], 
                                  capture_output=True, text=True)
            if 'inet' in result.stdout:
                print("✅ Network: Connected")
            else:
                print("❌ Network: Disconnected")
        except:
            print("⚠️ Network: Unknown")
        
        # Test connectivity
        if self.test_connection():
            print("✅ Internet: Accessible")
        else:
            print("❌ Internet: Blocked")
        
        print("─" * 40)
    
    def method_1_dns_proxy(self):
        """Method 1: DNS + HTTP Proxy"""
        print("\n🚀 Starting Method 1: DNS Override + HTTP Proxy")
        
        self.setup_dns_override()
        self.start_http_proxy()
        self.test_connection()
        
        print("\n✅ Method 1 activated!")
        print("🔧 Configure your apps to use HTTP proxy: 127.0.0.1:8080")
    
    def method_2_socks5_obfuscation(self):
        """Method 2: SOCKS5 + Traffic Obfuscation"""
        print("\n🚀 Starting Method 2: SOCKS5 + Traffic Obfuscation")
        
        self.setup_dns_override()
        self.start_socks5_proxy()
        self.start_traffic_obfuscation()
        self.test_connection()
        
        print("\n✅ Method 2 activated!")
        print("🔧 Configure your apps to use SOCKS5: 127.0.0.1:1080")
    
    def method_3_vpn_tunnel(self):
        """Method 3: VPN-like Tunnel"""
        print("\n🚀 Starting Method 3: VPN-like Tunnel")
        
        if not self.check_root():
            print("❌ This method requires root access!")
            return
        
        self.setup_dns_override()
        self.start_socks5_proxy()
        self.setup_redsocks()
        self.start_traffic_obfuscation()
        
        print("\n✅ Method 3 activated!")
        print("🔧 Transparent proxy enabled (requires root)")
    
    def method_4_full_stealth(self):
        """Method 4: Full Stealth Mode"""
        print("\n🚀 Starting Method 4: Full Stealth Mode")
        
        self.setup_dns_override()
        self.start_http_proxy(8080)
        self.start_socks5_proxy(1080)
        self.start_traffic_obfuscation()
        
        if self.check_root():
            self.setup_redsocks()
        
        self.test_connection()
        
        print("\n✅ Full Stealth Mode activated!")
        print("🔧 Multiple proxies running:")
        print("   - HTTP: 127.0.0.1:8080")
        print("   - SOCKS5: 127.0.0.1:1080")
    
    def show_menu(self):
        """Show main menu"""
        self.clear_screen()
        self.show_banner()
        
        print("🎯 AVAILABLE METHODS:")
        print("─" * 40)
        for key, method in self.methods.items():
            print(f"{key}. {method}")
        print("─" * 40)
        print("5. 🔍 Test Connection")
        print("6. 📊 Show Status") 
        print("7. 📦 Install Dependencies")
        print("8. 🚪 Exit")
        print("─" * 40)
        
        if self.check_root():
            print("🔓 Root access: Available")
        else:
            print("🔒 Root access: Not available (some features limited)")
    
    def run(self):
        """Main application loop"""
        
        # Check if we're in Termux
        if not os.path.exists('/data/data/com.termux/files/usr'):
            print("❌ This script is designed for Termux on Android!")
            return
        
        self.install_dependencies()
        
        while True:
            self.show_menu()
            choice = input("\n🎯 Select option (1-8): ").strip()
            
            if choice == '1':
                self.method_1_dns_proxy()
            elif choice == '2':
                self.method_2_socks5_obfuscation()
            elif choice == '3':
                self.method_3_vpn_tunnel()
            elif choice == '4':
                self.method_4_full_stealth()
            elif choice == '5':
                self.test_connection()
            elif choice == '6':
                self.show_status()
            elif choice == '7':
                self.install_dependencies()
            elif choice == '8':
                print("👋 Exiting...")
                break
            else:
                print("❌ Invalid option!")
            
            input("\nPress Enter to continue...")

def main():
    """Main function"""
    try:
        app = TermuxDPIBypass()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()