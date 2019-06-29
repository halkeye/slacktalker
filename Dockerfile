FROM python:3.7.3-stretch
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "./main.py"]
