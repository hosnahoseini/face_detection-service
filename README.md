# docker-test
## What does this script do?
Its a service implemented by fast API and python opencv to detect faces in one given image

We test it with fast API and Swagger

Pushed to docker hub and you can easily pull it from docker hub and enjoy!

## How to run
1. run `docker-compose up`

2. then open `http://127.0.0.1:8008/docs#/` in your browser

3. choose file in /detect_with_image/ or put your image on input folder and enter image relative path (start after /app/) in /detect_with_path/{imagePath:path} API and see the last result in /result/ 
(you can use images in test folder to test)

you can see inside of DB by `docker-compose exec db psql --username=fastapi_traefik --dbname=postgres`
## What did we use?
python3.8,
opencv,
fast API,
swagger,
docker,
docker compose,
postgres sql