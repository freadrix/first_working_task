FROM fedora:latest

WORKDIR /home

COPY main.py ./

COPY config.py ./

COPY requirements.txt ./

RUN dnf -y install python

RUN dnf -y install pip

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]