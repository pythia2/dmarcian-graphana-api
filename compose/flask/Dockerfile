FROM  python:3.13 AS builder

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY /project/ /app

CMD ["gunicorn", "-w", "2", "--threads", "4", "-b", "0.0.0.0:5000", "main:app"]
