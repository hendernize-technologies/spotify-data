# Spotify Data Pipeline

A containerized ETL pipeline that extracts user and public Spotify data for analysis. The pipeline runs on Google Cloud Platform using Airflow deployed on GKE (Google Kubernetes Engine).

## Overview

This pipeline extracts:

- User-specific listening data
- Public track and artist data
- Playlist information

The data is loaded into BigQuery for analysis and comparison between personal listening habits and public music trends.

## Architecture

### Technologies Used

- **Google Cloud Platform**
  - Container Registry (GCR) for container image storage
  - Secret Manager for secure credentials management
  - BigQuery for data warehousing
  - Google Kubernetes Engine (GKE) for orchestration
- **Apache Airflow** for workflow orchestration
- **Terraform** for infrastructure as code
- **Spotify Web API** for data extraction
- **Python** for ETL logic
- **GitHub Actions** for CI/CD

### Authentication Flow

The pipeline uses Spotify's Authorization Code Flow with automatic token refresh for continuous data access. This enables:

- Access to user-specific data
- Long-running automated processes
- Secure credential management

## DAGs

### 1. Daily Incremental Load

- Schedule: Daily at 00:00 UTC
- Extracts:
  - Previous day's listening history
  - New tracks and artists
  - Updated playlist information
- Implements incremental loading strategy
- Handles deduplication and updates

### 2. Historical Backfill

- One-time execution for historical data
- Configurable date range
- Full historical extract of:
  - Listening history
  - Saved tracks and playlists
  - Artist and track metadata

## Setup and Deployment

### Prerequisites

1. GCP Project with enabled services:
   - Container Registry
   - Secret Manager
   - BigQuery
   - GKE
2. Spotify Developer Account
3. Terraform installed locally

### Initial Setup

1. Run Terraform to provision infrastructure
2. Configure Spotify API credentials in Secret Manager
3. Run initial authorization flow to obtain refresh token
4. Store refresh token in Secret Manager

### Container Build and Deploy

The repository includes GitHub Actions workflows for:

1. `build_container.yml`: Builds and pushes container to GCR
2. `terraform.yml`: Manages infrastructure deployment

## Repository Structure

├── container/
│ └── spotify_elt/
│ ├── entrypoint.py
│ ├── helpers.py
│ └── requirements.txt
├── terraform/
├── .github/workflows/
├── README.md
└── .gitignore

## Development

### Local Testing

bash

#### Build container locally

docker build -t spotify-elt .

#### Run container with environment variables

docker run -e SPOTIFY_CLIENT_ID=xxx \
-e SPOTIFY_CLIENT_SECRET=xxx \
spotify-elt
