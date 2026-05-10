# Aurora Analytics – News Ingestion Service

A real-time news ingestion pipeline that fetches data from NewsAPI, processes it, and streams structured records into AWS Kinesis using a Redis-backed cursor for state management.

---

## 🧭 Architecture Overview
`NewsAPI → Cursor (Redis) → Processor → AWS Kinesis Stream`

- **NewsAPI**: Source of news articles
- **Redis**: Stores ingestion cursor (last processed timestamp)
- **Processor**: Cleans and transforms articles
- **Kinesis**: Streaming ingestion layer

---

## 🐍 Python Version

This project requires:
`Python 3.12.3`

If running locally:

```bash
python3.12 -m venv venv
source venv/bin/activate
```

## 📦 Installation (Local)

```bash
pip install -r requirements.txt
```

## 🔐 Environment Variables

Create a copy of example.env and rename it to .env

- **NEWS_QUERY**: The query parameter used for searching news articles. It is set to `technology` by default.
- **NEWS_API_KEY**: The Everything API Key required to be able to query the News API.
- **AWS_ACCESS_KEY_ID**: The Access Key ID required to be able to connect and ingest data to AWS Kinesis.
- **AWS_SECRET_ACCESS_KEY**: The Secret Access Key required to be able to connect and ingest data to AWS Kinesis.
- **AWS_REGION**: The AWS Region the Kinesis data stream is currenly hosted on. It is set to `ap-southeast-2` by default.
- **REDIS_HOST**: The hostname of redis used for tracking latest queried articles. Set to `redis` by default.
- **REDIS_PORT**: The port number of redis used for tracking latest queried articles. Set to `6379` by default.

## 🧹 Pre-commit Setup

This project uses:

- `black` (code formatting)
- `flake8` (linting)

Install pre-commit
```bash
pip install pre-commit
```

Install hooks
```bash
pre-commit install
```

Run manually
```bash
pre-commit run --all-files
```

## 🐳 Running with Docker Compose
1. Build and start services
```bash
docker compose up --build
```

This will start:
- App (ingestion service)
- Redis (cursor storage)

2. Run in detached mode
```bash
docker compose up -d
```

3. View logs (app only)
```bash
docker compose logs -f app
```

4. Stop services
```bash
docker compose down
```

## 🧠 Redis Persistence

Redis is used to store the ingestion cursor (last processed timestamp).

Data is persisted via Docker volume:
```yaml
volumes:
  - redis_data:/data
```

## 🔁 Ingestion Flow
1. Cursor reads last processed timestamp from Redis
2. System queries NewsAPI using (from → to) window
3. Articles are transformed into structured format
4. Data is sent to AWS Kinesis
5. Cursor updates to timestamp in Redis

## 📡 Output Schema (Kinesis)

Each record sent to Kinesis contains:
```json
{
  "article_id": "string",
  "source_name": "string",
  "title": "string",
  "content": "string",
  "url": "string",
  "author": "string",
  "published_at": "string",
  "ingested_at": "string"
}
```

## ⚠️ Key Design Notes
- Cursor is Redis-backed (not file-based)
Deduplication handled via time windowing strategy
- System is designed for continuous polling ingestion
- Kinesis acts as a streaming backbone, not a queryable database

## 🛠️ Tech Stack
- Python 3.12.3
- Redis
- AWS Kinesis
- httpx
- boto3
- pydantic
- Docker + Docker Compose
- pre-commit (black + flake8)