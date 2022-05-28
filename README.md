# backend

# install
```bash
git clone https://github.com/warlus-hackathon/backend.git
cd backend
```

## start minio
```bash
docker-compose up -d minio
docker-compose up -d createbuckets
```
## start data base
```bash
docker-compose up -d db
```

# install dependencies

## install poetry:

```bash
pip install poetry
```
## install of packages:

```bash
poetry install
```

## set enviroment

create .env file (see .env.default)

## usage:

```bash
make run
```
