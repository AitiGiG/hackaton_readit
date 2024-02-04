FROM python:3

ENV PYTHONIOENCODING UTF-8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir static && mkdir media 
COPY . .

RUN python3 manage.py collectstatic --noinput

EXPOSE 8000
