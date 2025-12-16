#!/bin/bash

# Simplified benchmark script for vLLM using ShareGPT dataset
# Uses the Qwen3-Coder-30B-A3B-Instruct-AWQ model

echo "Starting vLLM benchmark..."

# Create benchmarks directory if it doesn't exist
mkdir -p benchmarks

# Download the ShareGPT dataset
echo "Downloading ShareGPT dataset..."
wget -O benchmarks/ShareGPT_V3_unfiltered_cleaned_split.json https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/ShareGPT_V3_unfiltered_cleaned_split.json

# Run the benchmark with vLLM
echo "Running vLLM benchmark with Qwen3-Coder-30B-A3B-Instruct-AWQ model..."
uv run vllm bench serve \
    --model stelterlab/Qwen3-Coder-30B-A3B-Instruct-AWQ \
    --served-model-name qwen3-coder-30B-A3B-Instruct-AWQ \
    --endpoint /v1/completions \
    --dataset-name sharegpt \
    --dataset-path benchmarks/ShareGPT_V3_unfiltered_cleaned_split.json \
    --request-rate inf \
    --max-concurrency 20 \
    --ready-check-timeout-sec 20

echo "Benchmark completed."