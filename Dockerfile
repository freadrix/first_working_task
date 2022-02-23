FROM python:latest

WORKDIR /home

COPY main.py ./

COPY config.py ./

RUN pip install requests

CMD ["python", "./main.py"]