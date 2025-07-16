FROM python:3.10-slim
WORKDIR /app
COPY sample_redis.py /app/
RUN pip install redis
CMD ["python", "sample_redis.py"]