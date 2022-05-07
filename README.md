# Docker beginner2

После клонирования репозитория необходимо выполнить следующий команды:
* docker build -t some-api .
* docker run --name some-api -d -p 8000:8000 some-api

После выполнения вышеуказанных команд, необходимо перейти по адресу http://localhost:8000/api/v1/products
