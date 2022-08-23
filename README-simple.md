# docker-test
## What does this script do?
Its a service implemented by fast API and python opencv to detect faces in one given image


## How to run
1. run `docker-compose -f solution/docker-compose.yml up `

2. then open `http://0.0.0.0:8008/face/v1/docs#/` for face detection service in your browser
   or open `http://0.0.0.0:8008/text/v1/docs#/` for text service in your browser

3. choose file in /detect_with_image/ or put your image on input folder and enter image relative path (start after /app/) in /detect_with_path/{imagePath:path} API and see the last result in /result/ 
(you can use images in test folder to test)

## How to run Test
## What did we use?
python3.8,
opencv,
fast API,
swagger,
docker,
docker compose,
postgres sql,
traefik,
pytest
