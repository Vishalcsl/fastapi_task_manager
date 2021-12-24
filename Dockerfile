FROM python:3.6.1-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./backend /code/backend

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0", "--port", "80"]