FROM python:3.13-slim

WORKDIR /usr/src/app

# .pycファイルや__pycache__を生成しない
ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 依存インストール後コピー、キャッシュを最適化
COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]