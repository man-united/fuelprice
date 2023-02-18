FROM python:3.10.9

WORKDIR /

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py .
COPY fuel-app /fuel-app

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["gunicorn", "app:app"]