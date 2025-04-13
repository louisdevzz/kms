start docker for mongo db

```docker compose -f docker-compose.mongo.yml up -d
```
start docker for minio storage

```docker compose -f docker-compose.minio.yml up -d
``
at KMS-SoftwareDesign folder run this command to start system

```uvicorn backend.app:app --reload
```
