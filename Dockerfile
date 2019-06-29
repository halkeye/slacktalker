FROM python:3.7.3-stretch
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "./main.py"]
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:3000/healthcheck || exit 1
