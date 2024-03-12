FROM selenium/standalone-chrome:latest

USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]