# Hotels Project
Современный сервис для бронирования отелей с полным циклом работы с бронированиями, управлением номерами и удобствами.

## Возможности
### Аутентификация и авторизация
- JWT-токены для безопасной аутентификации
- Регистрация и вход пользователей
- Защищенные эндпоинты с проверкой прав доступа

### Управление отелями
- Создание, редактирование, получение и удаление отелей
- Детальная информация об отелях
- Пагинация и фильтрация при выводе списка отелей

### Управление номерами
- Создание и управление типами номеров
- Указание удобств и amenities для каждого номера
- Контроль доступности номеров на даты

### Система бронирования
- Бронирование номеров на выбранные даты
- Проверка доступности номеров
- Управление бронированиями (создание, просмотр, отмена)

### Производительность
- Кэширование с Redis для ускорения ответов API
- Асинхронная обработка запросов
- Фоновые задачи с Celery

## Технологический стек
### Backend
FastAPI - современный асинхронный фреймворк
SQLAlchemy - ORM для работы с базой данных
Pydantic - валидация данных и сериализация
Alembic - миграции базы данных

### Базы данных и кэширование
PostgreSQL - основная реляционная база данных
Redis - кэширование и брокер сообщений для Celery

### Фоновые задачи
Celery - распределенная очередь задач
Celery Beat - планировщик периодических задач

### Тестирование и качество кода
Pytest - тестирование приложения
Ruff - линтер и форматтер кода
Docker - контейнеризация приложения

## Быстрый старт
Предварительные требования
Docker и Docker Compose

Python 3.12

### Запуск с Docker
Клонируйте репозиторий:
```bash
git clone <repository-url>
cd Hotels_Project
```

Создайте файл окружения:
```bash
cp .env.example .env
# Отредактируйте .env при необходимости
```

Запустите сервисы:
```bash
docker-compose up -d
```

Приложение будет доступно по адресу:
- API: http://localhost:8000
- Документация: http://localhost:8000/docs





```bash
# Команды для docker

docker network create myNetwork


docker run --name booking_db
-p 6432:5432
-e POSTGRES_USER=admin
-e POSTGRES_PASSWORD=ew48ufpas9e4fpw9e4fUIWEH
-e POSTGRES_DB=booking
--network=myNetwork
--volume pg-booking-data:/var/lib/postgresql/data
-d postgres:16

docker run --name booking_db -p 6432:5432 -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=ew48ufpas9e4fpw9e4fUIWEH -e POSTGRES_DB=booking --network=myNetwork --volume pg-booking-data:/var/lib/postgresql/data -d postgres:16


docker run --name booking_cache
-p 7379:6379
--network=myNetwork
-d redis:7.4

docker run --name booking_cache -p 7379:6379 --network=myNetwork -d redis:7.4


docker run --name booking_back
-p 7777:8000
--network=myNetwork
booking_image

docker run --name booking_back -p 7777:8000 --network=myNetwork booking_image


docker run --name booking_celery_worker
--network=myNetwork
booking_image
celery --app=src.tasks.celery_app:celery_instance worker -l INFO

docker run --name booking_celery_worker --network=myNetwork booking_image celery --app=src.tasks.celery_app:celery_instance worker -l INFO


docker run --name booking_celery_beat
--network=myNetwork
booking_image
celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

docker run --name booking_celery_worker --network=myNetwork booking_image celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B


docker build -t booking_image .


docker run --name booking_nginx
-v ./nginx.conf:/etc/nginx/nginx.conf
--network=MyNetwork
--rm -p 80:80 nginx

docker run --name booking_nginx -v ./nginx.conf:/etc/nginx/nginx.conf --network=MyNetwork --rm -p 80:80 nginx
```