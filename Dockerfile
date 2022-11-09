FROM python:3
WORKDIR /

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY core core
COPY README.md README.md
COPY cfg.py cfg.py
COPY requirements.txt requirements.txt
COPY server.py server.py
CMD python server.py