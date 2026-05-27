# AvScan

<p align="center">
    <em>Это бот на aiogram, который парсит авито с приоритетными очередями</em>
</p>

<p align="center">
    <img src="https://img.shields.io/github/languages/top/OkulusDev/Oxygen">
    <img src="https://img.shields.io/github/license/OkulusDev/Oxyge">
    <img src="https://img.shields.io/github/stars/OkulusDev/Oxygen">
</p>

<p align="center">
    <img width="660" height="453" alt="image" src="https://github.com/user-attachments/assets/8f102d13-f260-4f46-a62f-e6aecee49d8c" />
</p>

## Установка и запуск
Вы должны склонировать репозиторий:
* `git clone https://github.com/Mak-os-sourse/AvScan.git`

Теперь вы можете запустить контейнер: 
* `docker-compose up -d`

## Структура
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
