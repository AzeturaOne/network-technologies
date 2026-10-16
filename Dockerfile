FROM python:3.14.7-alpine3.23

WORKDIR /project

COPY ./requirements.txt /project/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /project/requirements.txt

COPY ./app /project/app
COPY ./templates /project/templates

EXPOSE 80

CMD ["python", "-m", "uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "80"]
