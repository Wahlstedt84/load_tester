# Load Testing Tool

This tool allows you to perform load testing on your web application to evaluate its performance under high traffic conditions. It's designed for legitimate testing purposes only.

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with the following command:

```bash
python load_tester.py --url URL [--threads THREADS] [--requests REQUESTS] [--interval INTERVAL]
```

### Parameters:

- `--url`: (Required) The target URL to test
- `--threads`: (Optional) Number of concurrent threads (default: 5)
- `--requests`: (Optional) Total number of requests to send (default: 100)
- `--interval`: (Optional) Interval between requests in seconds (default: 0.1)

### Example:

```bash
python load_tester.py --url http://myapp.com/api --threads 10 --requests 1000 --interval 0.1
```

## Safety Considerations

- Always test on your own applications or with explicit permission
- Start with a low number of threads and requests, then gradually increase
- Monitor your application's performance during testing
- Be aware that excessive load testing can be indistinguishable from a DDoS attack

## Output

The script will provide detailed statistics about the load test, including:

- Test duration
- Requests per second
- Response time statistics (min, max, mean, median, standard deviation)
- Status code distribution
- Any errors encountered during testing 
