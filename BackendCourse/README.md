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