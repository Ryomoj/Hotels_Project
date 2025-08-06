FROM python:3.12

RUN echo ls
WORKDIR /app
RUN echo ls

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .


# CMD ["python", "src/main.py"]
CMD alembic upgrade head; python src/main.py