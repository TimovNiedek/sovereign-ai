# vLLM Proof of Concept Setup

This document outlines the setup for a self-hosted LLM using vLLM with Prometheus and Grafana monitoring.

## Prerequisites

Environment variables supplied through .env file:

```
# Your token from huggingface hub for downloading models with vllm
HF_TOKEN=...

# Can be any key starting with `sk-...`, e.g. sk-1234
LITELLM_MASTER_KEY=...

# or development for only running cpu-models
LITELLM_ENVIRONMENT=production

# Only needed when connecting Open WebUI to the remote litellm
# If not specified, will attempt to connect to litellm within the docker compose network, suitable for development
LITELLM_URL=http://host.docker.internal:4000
```

## Running with docker compose

```bash
docker network create common_network
docker compose --profile production -f docker-compose.yml up -d
```

## Local setup (MacOS)

Checkout the [vllm repo](https://github.com/vllm-project/vllm) next to this one. This is needed to be able to build the CPU-based image from source for MacOS.

```
brew install prometheus
brew install grafana

prometheus --config.file=monitoring/prometheus-local.yaml

docker compose --profile development -f docker-compose.yml up -d
```

## Architecture

This repository composes a small self-hosted LLM stack. Services, their purpose, and the ports they expose are listed below.

- **vllm-qwen3**: vLLM CPU-based model server (development). Serves Qwen/Qwen3-1.7B model on port `8000`. Profile: `local`.
- **vllm-llama3**: vLLM CPU-based model server for Llama-3 (development). Serves meta-llama/Llama-3.2-3B-Instruct on port `8001`. Profile: `local`.
- **vllm-coder**: vLLM GPU-based model server (remote profile). Serves a coder model on port `8000` (host:container `8000:8000`) when run in the `remote` profile; typically run on a GPU host. Shares the `common_network` for cluster use.
- **litellm**: `litellm` OpenAI-compatible API adapter (used as an API backend). Exposes port `4000` (host:container `4000:4000`). The stack uses this as the `OPENAI_API_BASE_URL` for frontends.
- **open-webui**: Web UI frontend for interacting with models. Exposes port `8080`. Connects to `litellm` via the internal Docker network.
- **prometheus**: Metrics server for scraping application metrics. Exposes port `9090`. Config: `monitoring/prometheus.yaml`.
- **grafana**: Dashboarding service. Exposes port `3000` and is pre-provisioned with dashboards/datasources from `monitoring/grafana/provisioning/`.

## Resource Allocation Strategy

### CPU-Based Models (Development)

CPU allocation is split equally across development models to maximize throughput:
- **vllm-qwen3**: Cores 0-3 (4 cores), 4GB RAM for KV cache
- **vllm-llama3**: Cores 4-7 (4 cores), 4GB RAM for KV cache

This configuration assumes the host has **at least 8+ CPU cores**. Adjust `VLLM_CPU_OMP_THREADS_BIND` ranges and `VLLM_CPU_KVCACHE_SPACE` in `docker-compose.vllm.yml` if your system has fewer cores or less available RAM.

### GPU-Based Models (Production)

GPU memory allocation is constrained to prevent OOM errors:
- **GPU utilization**: 45% per model (90% total)
- **Max context length**: 16k tokens

**Allocation rationale:**
- Initial attempts with 65k context length using 90% GPU utilization resulted in vLLM out-of-memory errors
- Reduced to 32k context length: still insufficient for concurrent model execution
- Reduced to 16k context length: successfully supports parallel execution of both models with room for headroom
- `vllm-gpt-oss` only starts once `vllm-coder` is healthy to avoid concurrent GPU memory claims spiking during model loading.

See [benchmarks/README.md](benchmarks/README.md) for detailed benchmark results and performance metrics.

Notes:
- Services are split into `development` and `production` profiles. When running locally, enable the `development` profile to avoid starting GPU/remote-only services. When running on a GPU host, use the `production` profile for GPU-backed model containers.
- Some services may bind to the same host ports in different profiles (for example `8000` for CPU vs GPU vLLM). Ensure you run only the intended profile(s) concurrently or change host port mappings as needed.
