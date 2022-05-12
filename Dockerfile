FROM python:3.10-alpine

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN pip install gunicorn

EXPOSE 8000

# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]