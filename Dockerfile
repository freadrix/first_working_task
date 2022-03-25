FROM fedora:latest

WORKDIR /home

COPY issue_fetcher ./

COPY config.py ./

COPY requirements.txt ./

COPY setup.py ./

RUN dnf -y install python

RUN dnf -y install pip

RUN pip install --editable .

CMD ["issue_fetcher"]