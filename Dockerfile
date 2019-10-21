FROM python:3.7.5-stretch
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --upgrade -r requirements.txt
COPY . .
CMD ["gunicorn","-b","0.0.0.0:3000","wsgi:app"]
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:3000/healthcheck || exit 1
