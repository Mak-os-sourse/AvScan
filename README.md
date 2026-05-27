# AvScan

<p align="center">
    <em>This is an aiogram bot that parses Avito with priority queues.</em>
</p>

<p align="center">
    <img src="https://img.shields.io/github/languages/top/OkulusDev/Oxygen">
    <img src="https://img.shields.io/github/license/OkulusDev/Oxyge">
    <img src="https://img.shields.io/github/stars/OkulusDev/Oxygen">
</p>

<p align="center">
    <img width="660" height="453" alt="image" src="https://github.com/user-attachments/assets/8f102d13-f260-4f46-a62f-e6aecee49d8c" />
</p>

## Stack
* sqlalchemy (Postgresql)
* alembic
* redis
* aiogram
* pytest
* pytest-asyncio
* playwright
* playwright-stealth
* bs4
* taskiq
* pandas
* structlog

## Installation and launch
First, you need to clone the repository:
* `git clone https://github.com/Mak-os-sourse/AvScan.git`

Now you can run the container:
* `docker-compose up -d`

## Structure
```
├───src
│   ├───app
│   │   ├───bot
│   │   │   ├───fsm
│   │   │   ├───handlers
│   │   │   ├───keyboards
│   │   │   ├───middleware
│   │   │   └───templates
│   │   ├───core
│   │   ├───crud
│   │   ├───exceptions
│   │   ├───models
│   │   ├───services
│   │   │   └───parser
│   │   ├───tasks
│   │   └───types
│   └───tests
│       ├───crud
│       ├───factories
│       ├───services
└───main.py
```
