#!/bin/bash
set -euo pipefail

# Benchmark script for vLLM using ShareGPT dataset
# Usage: ./vllm_benchmark.sh [MODEL_NAME] [PORT]
# Default model: stelterlab/Qwen3-Coder-30B-A3B-Instruct-AWQ

DEFAULT_MODEL="stelterlab/Qwen3-Coder-30B-A3B-Instruct-AWQ"
DEFAULT_PORT=8000

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || "${2:-}" == "-h" || "${2:-}" == "--help" ]]; then
    echo "Usage: $0 [MODEL_NAME] [PORT]"
    echo "Example: $0 openai/gpt-oss-20b 8000"
    exit 0
fi

# MODEL: first positional arg, defaults to DEFAULT_MODEL
MODEL="${1:-$DEFAULT_MODEL}"
# PORT: second positional arg, environment variable `PORT` takes precedence if set
PORT="${2:-${PORT:-$DEFAULT_PORT}}"


echo "Starting vLLM benchmark..."

# Create benchmarks directory if it doesn't exist
mkdir -p benchmarks

# Download the ShareGPT dataset
echo "Downloading ShareGPT dataset..."
wget -q -O benchmarks/ShareGPT_V3_unfiltered_cleaned_split.json https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/ShareGPT_V3_unfiltered_cleaned_split.json

# Run the benchmark with vLLM against
echo "Running vLLM benchmark with ${MODEL} model against port ${PORT}..."
uv run vllm bench serve \
    --port "$PORT" \
    --model "$MODEL" \
    --endpoint /v1/completions \
    --dataset-name sharegpt \
    --dataset-path benchmarks/ShareGPT_V3_unfiltered_cleaned_split.json \
    --request-rate inf \
    --max-concurrency 20 \
    --ready-check-timeout-sec 20

echo "Benchmark completed."