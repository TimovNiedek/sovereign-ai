# VLLM Benchmark Scripts

This directory contains benchmark scripts for testing vLLM performance.

## vllm_benchmark.sh

This script performs benchmarking of the vLLM inference server using the ShareGPT dataset.

### Usage

1. Make sure vLLM is installed in your environment
2. Run the benchmark script:
   ```bash
   ./benchmarks/vllm_benchmark.sh [MODEL_NAME] [PORT]
   ```
   Model name and port number should match configuration in [../docker-compose.vllm.yml](../docker-compose.vllm.yml)

### What it does

- Creates a `benchmarks` directory if it doesn't exist
- Downloads the ShareGPT dataset from Hugging Face
- Runs a vLLM benchmark using the configured` model
- Limits the number of concurrent requests to mimick a set number of users (20)
- Outputs benchmark results to the console

### Prerequisites

- `uv` installed
- dependencies installed with `uv sync --group benchmark`
- Internet connectivity to download the ShareGPT dataset

## Results

The following results are gathered by running the benchmark against both models at the same time. This simulates a scenario where 20 users are continuously accessing both models at the same time.

The full stack is executed on a single L40s GPU.

### stelterlab/Qwen3-Coder-30B-A3B-Instruct-AWQ

```
============ Serving Benchmark Result ============
Successful requests:                     1000      
Failed requests:                         0         
Maximum request concurrency:             20        
Benchmark duration (s):                  401.50    
Total input tokens:                      217393    
Total generated tokens:                  199372    
Request throughput (req/s):              2.49      
Output token throughput (tok/s):         496.57    
Peak output token throughput (tok/s):    1037.00   
Peak concurrent requests:                30.00     
Total Token throughput (tok/s):          1038.03   
---------------Time to First Token----------------
Mean TTFT (ms):                          97.61     
Median TTFT (ms):                        95.76     
P99 TTFT (ms):                           179.29    
-----Time per Output Token (excl. 1st token)------
Mean TPOT (ms):                          39.55     
Median TPOT (ms):                        42.97     
P99 TPOT (ms):                           50.36     
---------------Inter-token Latency----------------
Mean ITL (ms):                           39.32     
Median ITL (ms):                         41.66     
P99 ITL (ms):                            86.21     
==================================================
```

### openai/gpt-oss-20b

```
============ Serving Benchmark Result ============
Successful requests:                     1000      
Failed requests:                         0         
Maximum request concurrency:             20        
Benchmark duration (s):                  397.05    
Total input tokens:                      215312    
Total generated tokens:                  197770    
Request throughput (req/s):              2.52      
Output token throughput (tok/s):         498.10    
Peak output token throughput (tok/s):    1036.00   
Peak concurrent requests:                30.00     
Total Token throughput (tok/s):          1040.39   
---------------Time to First Token----------------
Mean TTFT (ms):                          92.35     
Median TTFT (ms):                        87.77     
P99 TTFT (ms):                           242.76    
-----Time per Output Token (excl. 1st token)------
Mean TPOT (ms):                          39.23     
Median TPOT (ms):                        42.68     
P99 TPOT (ms):                           47.65     
---------------Inter-token Latency----------------
Mean ITL (ms):                           39.55     
Median ITL (ms):                         41.89     
P99 ITL (ms):                            69.36     
==================================================
```