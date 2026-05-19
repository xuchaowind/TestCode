#!/usr/bin/env python3
"""
Network Test Script
A comprehensive network testing tool for checking connectivity, DNS resolution,
HTTP responses, port connectivity, and network latency.

Author: xuchaowind
Date: 2026-05-19
"""

import socket
import subprocess
import sys
import platform
import time
import json
from datetime import datetime
from typing import Dict, Any, List
import urllib.request
import urllib.error


class NetworkTester:
    """Network testing utility class"""

    def __init__(self, timeout: int = 5):
        """Initialize the network tester

        Args:
            timeout (int): Default timeout for network operations in seconds
        """
        self.timeout = timeout
        self.results: Dict[str, Any] = {
            'timestamp': datetime.now().isoformat(),
            'system': platform.system(),
            'tests': {
                'dns': {},
                'ping': {},
                'http': {},
                'ports': {},
                'latency': {}
            }
        }

    def test_dns_resolution(self, hostname: str) -> Dict[str, Any]:
        """Test DNS resolution

        Args:
            hostname (str): Hostname to resolve

        Returns:
            Dict with test results
        """
        try:
            ip_address = socket.gethostbyname(hostname)
            result = {
                'status': 'success',
                'hostname': hostname,
                'ip_address': ip_address
            }
            print(f"✓ DNS Test: {hostname} -> {ip_address}")
        except socket.gaierror as e:
            result = {
                'status': 'failed',
                'hostname': hostname,
                'error': str(e)
            }
            print(f"✗ DNS Test Failed: {hostname} - {e}")
        except Exception as e:
            result = {
                'status': 'error',
                'hostname': hostname,
                'error': str(e)
            }
            print(f"✗ DNS Test Error: {hostname} - {e}")

        self.results['tests']['dns'][hostname] = result
        return result

    def test_ping(self, hostname: str) -> Dict[str, Any]:
        """Test ping connectivity

        Args:
            hostname (str): Hostname or IP to ping

        Returns:
            Dict with test results
        """
        try:
            # Determine ping command based on OS
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = f'ping {param} 1 -W {self.timeout * 1000} {hostname}'

            output = subprocess.check_output(
                command, shell=True, universal_newlines=True,
                stderr=subprocess.STDOUT, timeout=self.timeout + 5
            )

            result = {
                'status': 'success',
                'host': hostname,
                'output': output.strip()
            }
            print(f"✓ Ping Test: {hostname} is reachable")
        except subprocess.CalledProcessError as e:
            result = {
                'status': 'failed',
                'host': hostname,
                'error': 'Host unreachable'
            }
            print(f"✗ Ping Test Failed: {hostname} is unreachable")
        except subprocess.TimeoutExpired:
            result = {
                'status': 'timeout',
                'host': hostname,
                'error': 'Ping timeout'
            }
            print(f"✗ Ping Test Timeout: {hostname}")
        except Exception as e:
            result = {
                'status': 'error',
                'host': hostname,
                'error': str(e)
            }
            print(f"✗ Ping Test Error: {hostname} - {e}")

        self.results['tests']['ping'][hostname] = result
        return result

    def test_http_request(self, url: str) -> Dict[str, Any]:
        """Test HTTP request

        Args:
            url (str): URL to test

        Returns:
            Dict with test results
        """
        try:
            start_time = time.time()
            request = urllib.request.Request(url)
            request.add_header('User-Agent', 'NetworkTester/1.0')

            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                response_time_ms = (time.time() - start_time) * 1000
                content_length = len(response.read())

                result = {
                    'status': 'success',
                    'url': url,
                    'status_code': response.status,
                    'response_time_ms': round(response_time_ms, 2),
                    'content_length': content_length
                }
                print(f"✓ HTTP Test: {url} - Status {response.status} ({response_time_ms:.2f}ms)")
        except urllib.error.HTTPError as e:
            response_time_ms = (time.time() - start_time) * 1000
            result = {
                'status': 'http_error',
                'url': url,
                'status_code': e.code,
                'response_time_ms': round(response_time_ms, 2),
                'error': str(e)
            }
            print(f"✗ HTTP Test: {url} - HTTP Error {e.code}")
        except urllib.error.URLError as e:
            result = {
                'status': 'failed',
                'url': url,
                'error': str(e.reason)
            }
            print(f"✗ HTTP Test Failed: {url} - {e.reason}")
        except socket.timeout:
            result = {
                'status': 'timeout',
                'url': url,
                'error': 'Request timeout'
            }
            print(f"✗ HTTP Test Timeout: {url}")
        except Exception as e:
            result = {
                'status': 'error',
                'url': url,
                'error': str(e)
            }
            print(f"✗ HTTP Test Error: {url} - {e}")

        self.results['tests']['http'][url] = result
        return result

    def test_port_connectivity(self, host: str, port: int) -> Dict[str, Any]:
        """Test port connectivity

        Args:
            host (str): Hostname or IP address
            port (int): Port number

        Returns:
            Dict with test results
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)

        try:
            result_obj = sock.connect_ex((host, port))
            if result_obj == 0:
                result = {
                    'status': 'success',
                    'host': host,
                    'port': port,
                    'message': f'Port {port} is open'
                }
                print(f"✓ Port Test: {host}:{port} is open")
            else:
                result = {
                    'status': 'failed',
                    'host': host,
                    'port': port,
                    'message': f'Port {port} is closed'
                }
                print(f"✗ Port Test: {host}:{port} is closed")
        except socket.gaierror:
            result = {
                'status': 'failed',
                'host': host,
                'port': port,
                'error': 'Hostname could not be resolved'
            }
            print(f"✗ Port Test: {host}:{port} - Hostname resolution failed")
        except socket.error:
            result = {
                'status': 'failed',
                'host': host,
                'port': port,
                'error': 'Connection error'
            }
            print(f"✗ Port Test: {host}:{port} - Connection error")
        except Exception as e:
            result = {
                'status': 'error',
                'host': host,
                'port': port,
                'error': str(e)
            }
            print(f"✗ Port Test Error: {host}:{port} - {e}")
        finally:
            sock.close()

        key = f"{host}_{port}"
        self.results['tests']['ports'][key] = result
        return result

    def test_network_latency(self, host: str, count: int = 4) -> Dict[str, Any]:
        """Test network latency using ping

        Args:
            host (str): Hostname or IP to ping
            count (int): Number of ping attempts

        Returns:
            Dict with test results
        """
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = f'ping {param} {count} -W {self.timeout * 1000} {host}'

            output = subprocess.check_output(
                command, shell=True, universal_newlines=True,
                stderr=subprocess.STDOUT, timeout=self.timeout + 5
            )

            # Parse latency information
            lines = output.split('\n')
            latencies = []

            for line in lines:
                if 'time=' in line:
                    try:
                        time_str = line.split('time=')[1].split('ms')[0].strip()
                        latencies.append(float(time_str))
                    except (IndexError, ValueError):
                        continue

            if latencies:
                result = {
                    'status': 'success',
                    'host': host,
                    'avg_ms': round(sum(latencies) / len(latencies), 2),
                    'min_ms': round(min(latencies), 2),
                    'max_ms': round(max(latencies), 2),
                    'count': len(latencies)
                }
                print(f"✓ Latency Test: {host} - Avg {result['avg_ms']}ms")
            else:
                result = {
                    'status': 'partial',
                    'host': host,
                    'error': 'Could not parse latency data',
                    'raw_output': output
                }
                print(f"⚠ Latency Test: {host} - Partial results")
        except subprocess.CalledProcessError:
            result = {
                'status': 'failed',
                'host': host,
                'error': 'Host unreachable'
            }
            print(f"✗ Latency Test Failed: {host} is unreachable")
        except subprocess.TimeoutExpired:
            result = {
                'status': 'timeout',
                'host': host,
                'error': 'Ping timeout'
            }
            print(f"✗ Latency Test Timeout: {host}")
        except Exception as e:
            result = {
                'status': 'error',
                'host': host,
                'error': str(e)
            }
            print(f"✗ Latency Test Error: {host} - {e}")

        self.results['tests']['latency'][host] = result
        return result

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all network tests

        Returns:
            Dict with all test results
        """
        print("\n" + "="*60)
        print("Starting Network Tests")
        print("="*60 + "\n")

        # DNS Tests
        print("[DNS Resolution Tests]")
        for hostname in ['github.com', 'google.com', 'cloudflare.com']:
            self.test_dns_resolution(hostname)
        print()

        # Ping Tests
        print("[Ping Connectivity Tests]")
        for hostname in ['github.com', 'google.com']:
            self.test_ping(hostname)
        print()

        # HTTP Tests
        print("[HTTP Request Tests]")
        for url in ['https://github.com', 'https://www.google.com', 'https://www.cloudflare.com']:
            self.test_http_request(url)
        print()

        # Port Tests
        print("[Port Connectivity Tests]")
        ports_to_test = [
            ('github.com', 22),   # SSH
            ('github.com', 443),  # HTTPS
            ('8.8.8.8', 53)       # DNS
        ]
        for host, port in ports_to_test:
            self.test_port_connectivity(host, port)
        print()

        # Latency Tests
        print("[Network Latency Tests]")
        for hostname in ['github.com', 'google.com']:
            self.test_network_latency(hostname)
        print()

        print("="*60)
        print("Network Tests Completed")
        print("="*60 + "\n")

        return self.results

    def save_results(self, filename: str = 'network_test_results.json') -> None:
        """Save test results to JSON file

        Args:
            filename (str): Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            print(f"✓ Results saved to {filename}")
        except Exception as e:
            print(f"✗ Failed to save results: {e}")

    def print_summary(self) -> None:
        """Print a summary of test results"""
        print("\n" + "="*60)
        print("Test Summary")
        print("="*60)

        for test_type, tests in self.results['tests'].items():
            if tests:
                success_count = sum(1 for t in tests.values() if t.get('status') == 'success')
                total_count = len(tests)
                percentage = (success_count / total_count * 100) if total_count > 0 else 0
                print(f"{test_type.upper():15} : {success_count}/{total_count} passed ({percentage:.0f}%)")

        print("="*60 + "\n")


def main():
    """Main function"""
    try:
        tester = NetworkTester(timeout=5)
        results = tester.run_all_tests()
        tester.save_results()
        tester.print_summary()

        print("\nTest results have been saved to 'network_test_results.json'")
        return 0
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        return 1
    except Exception as e:
        print(f"\nFatal error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
