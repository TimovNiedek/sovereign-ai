# VLLM Benchmark Scripts

This directory contains benchmark scripts for testing vLLM performance.

## vllm_benchmark.sh

This script performs benchmarking of the vLLM inference server using the ShareGPT dataset.

### Usage

1. Make sure vLLM is installed in your environment
2. Run the benchmark script:
   ```bash
   ./benchmarks/vllm_benchmark.sh
   ```

### What it does

- Creates a `benchmarks` directory if it doesn't exist
- Downloads the ShareGPT dataset from Hugging Face
- Runs a vLLM benchmark using the `stelterlab/Qwen3-Coder-30B-A3B-Instruct-AWQ` model
- Limits the number of concurrent requests to mimick a set number of users (20)
- Outputs benchmark results to the console

### Prerequisites

- `uv` installed
- dependencies installed with `uv sync --group benchmark`
- Internet connectivity to download the ShareGPT dataset