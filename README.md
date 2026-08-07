# reminders-service

reminders-service — domain: appointments

- **Port:** 8602
- **Language:** Python 3.11 + Flask
- **Database:** `appointments` (Postgres, table `reminders`)
- **Event bus:** Kafka

## API

| Method    | Path                       |
|-----------|----------------------------|
| GET       | `/api/reminders/`          |
| POST      | `/api/reminders/`          |
| GET       | `/api/reminders/<id>`      |
| PUT/PATCH | `/api/reminders/<id>`      |
| DELETE    | `/api/reminders/<id>`      |
| GET       | `/health`                  |
| GET       | `/ready`                   |

## Events

**Publishes:** (none)
**Subscribes:** appointment.booked

## HTTP peer dependencies

- `notifications-service`
- `patients-service`
- `audit-log-service`

## Local dev

```bash
pip install -e ../../libs/py-healthcare-common
pip install -r requirements.txt
cp .env.example .env
(cd ../../infra && docker compose up -d postgres kafka kafka-init)
python -m app.main
```

## Tests

```bash
pytest
```
