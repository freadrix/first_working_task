FROM fedora:latest

WORKDIR /home

COPY . .

RUN dnf -y install python

RUN dnf -y install pip

RUN pip install --editable .

CMD ["issue_fetcher", "issues"]