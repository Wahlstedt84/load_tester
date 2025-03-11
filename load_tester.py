#!/usr/bin/env python3
"""
Load Testing Script

This script performs load testing on a web application by sending multiple concurrent
requests. It's designed for legitimate testing purposes to evaluate how an application
performs under heavy load.

Usage:
    python load_tester.py --url URL [--threads THREADS] [--requests REQUESTS] [--interval INTERVAL]

Example:
    python load_tester.py --url http://myapp.com/api --threads 10 --requests 1000 --interval 0.1
"""

import argparse
import concurrent.futures
import requests
import time
import statistics
from datetime import datetime
import sys


class LoadTester:
    def __init__(self, url, num_threads=5, num_requests=100, interval=0.1):
        self.url = url
        self.num_threads = num_threads
        self.num_requests = num_requests
        self.interval = interval
        self.response_times = []
        self.status_codes = {}
        self.errors = []
        self.start_time = None
        self.end_time = None

    def send_request(self, request_id):
        """Send a single HTTP request and record the response time."""
        try:
            start = time.time()
            response = requests.get(self.url, timeout=10)
            end = time.time()
            
            response_time = end - start
            self.response_times.append(response_time)
            
            status_code = response.status_code
            if status_code in self.status_codes:
                self.status_codes[status_code] += 1
            else:
                self.status_codes[status_code] = 1
                
            return {
                'id': request_id,
                'status_code': status_code,
                'response_time': response_time,
                'success': True
            }
        except Exception as e:
            self.errors.append(str(e))
            return {
                'id': request_id,
                'error': str(e),
                'success': False
            }

    def run(self):
        """Run the load test with multiple threads."""
        print(f"\nStarting load test on {self.url}")
        print(f"Threads: {self.num_threads}, Requests: {self.num_requests}, Interval: {self.interval}s")
        print("=" * 80)
        
        self.start_time = datetime.now()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = []
            for i in range(self.num_requests):
                futures.append(executor.submit(self.send_request, i))
                time.sleep(self.interval)
                
                # Print progress
                if (i + 1) % 10 == 0 or i + 1 == self.num_requests:
                    sys.stdout.write(f"\rProgress: {i + 1}/{self.num_requests} requests sent")
                    sys.stdout.flush()
            
            # Wait for all futures to complete
            concurrent.futures.wait(futures)
        
        self.end_time = datetime.now()
        print("\n" + "=" * 80)
        self.print_results()

    def print_results(self):
        """Print the results of the load test."""
        if not self.response_times:
            print("No successful requests were made.")
            return
            
        duration = (self.end_time - self.start_time).total_seconds()
        requests_per_second = self.num_requests / duration
        
        print(f"\nLoad Test Results:")
        print(f"  Test Duration: {duration:.2f} seconds")
        print(f"  Requests Per Second: {requests_per_second:.2f}")
        print(f"  Total Requests: {self.num_requests}")
        print(f"  Successful Requests: {len(self.response_times)}")
        print(f"  Failed Requests: {len(self.errors)}")
        
        if self.response_times:
            print("\nResponse Time Statistics (seconds):")
            print(f"  Min: {min(self.response_times):.4f}")
            print(f"  Max: {max(self.response_times):.4f}")
            print(f"  Mean: {statistics.mean(self.response_times):.4f}")
            print(f"  Median: {statistics.median(self.response_times):.4f}")
            if len(self.response_times) > 1:
                print(f"  Std Dev: {statistics.stdev(self.response_times):.4f}")
        
        print("\nStatus Code Distribution:")
        for status_code, count in sorted(self.status_codes.items()):
            print(f"  {status_code}: {count} ({count/self.num_requests*100:.1f}%)")
        
        if self.errors:
            print(f"\nError Types ({len(self.errors)} total):")
            error_counts = {}
            for error in self.errors:
                if error in error_counts:
                    error_counts[error] += 1
                else:
                    error_counts[error] = 1
            
            for error, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  {error}: {count}")


def main():
    parser = argparse.ArgumentParser(description='Load Testing Tool')
    parser.add_argument('--url', required=True, help='Target URL to test')
    parser.add_argument('--threads', type=int, default=5, help='Number of concurrent threads')
    parser.add_argument('--requests', type=int, default=100, help='Total number of requests to send')
    parser.add_argument('--interval', type=float, default=0.1, help='Interval between requests in seconds')
    
    args = parser.parse_args()
    
    # Warn if the number of threads is very high
    if args.threads > 50:
        print("WARNING: Using a high number of threads may cause excessive load.")
        response = input("Do you want to continue? (y/n): ")
        if response.lower() != 'y':
            print("Load test aborted.")
            return
    
    tester = LoadTester(
        url=args.url,
        num_threads=args.threads,
        num_requests=args.requests,
        interval=args.interval
    )
    
    tester.run()


if __name__ == "__main__":
    main() 