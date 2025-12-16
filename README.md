# vLLM Proof of Concept Setup

This document outlines the setup for a self-hosted LLM using vLLM with Prometheus and Grafana monitoring.

## Prerequisites

* Set the environment variable HF_TOKEN, or add it to a .env file.

## Running with docker compose

```bash
docker network create common_network
docker compose -f docker-compose.vllm.yml up -d
docker compose -f docker-compose.monitoring.yml up -d
```

## Architecture

The setup supports running components independently:

- **vLLM**: Runs on `localhost:8000`
- **Prometheus**: Runs on `localhost:9090` 
- **Grafana**: Runs on `localhost:3000`

This separation allows you to manage vLLM without needing to restart the monitoring stack, or vice versa.
