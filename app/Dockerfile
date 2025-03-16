FROM python:3.11-slim

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y netcat-openbsd
RUN apt-get install -y tzdata

ENV TZ=Europe/Moscow

RUN pip install --upgrade pip



COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]