# docker-test
## What does this script do?
Its a service implemented by fast API and python opencv to detect faces in one given image

We test it with fast API and Swagger

Pushed to docker hub and you can easily pull it from docker hub and enjoy!

## How to run
1. `docker run -d -p 8001:8001 hosnahoseini/face-detection-simple` or just run `docker-compose up`

2. then open `http://0.0.0.0:8001/docs#/` in your browser

3. choose file in /image/ or by entre image path in /path/{imagePath:path} API and see the last result in /last_output/ 
(you can use images in test folder to test)

## What did we use?
python3.8,
opencv,
fast API,
swagger,
docker
