FROM python:3.10-slim 

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

CMD ["python", "manage", "runserver", "0.0.0.0:8000"]