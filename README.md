# vLLM Proof of Concept Setup

This document outlines the setup for a self-hosted LLM using vLLM with Prometheus and Grafana monitoring.

## Prerequisites

Environment variables supplied through .env file:

```
HF_TOKEN=...
LITELLM_MASTER_KEY=...
PROFILE=remote  # or local
```

## Running with docker compose

```bash
docker network create common_network
docker compose --profile remote -f docker-compose.yml up -d
```

## Local setup (MacOS)

Checkout the [vllm repo](https://github.com/vllm-project/vllm) next to this one. This is needed to be able to build the CPU-based image from source for MacOS.

```
brew install prometheus
brew install grafana

prometheus --config.file=monitoring/prometheus-local.yaml

docker compose --profile local -f docker-compose.yml up -d
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

Notes:
- Services are split into `local` and `remote` profiles. When running locally, enable the `local` profile to avoid starting GPU/remote-only services. When running on a GPU host, use the `remote` profile for GPU-backed model containers.
- Some services may bind to the same host ports in different profiles (for example `8000` for CPU vs GPU vLLM). Ensure you run only the intended profile(s) concurrently or change host port mappings as needed.
