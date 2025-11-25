# 베이스 이미지
FROM python:3.12-slim

# 환경변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    sqlite3 \
    libsqlite3-dev \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# requirements 파일을 먼저 복사
COPY requirements.txt .

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# SQLite 데이터베이스 디렉토리 생성 및 권한 설정
RUN mkdir -p /app/server && \
    chmod 755 /app/server

# 포트 노출
EXPOSE 8000

# 헬스체크 추가
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# 실행 명령
CMD ["python", "server/manage.py", "runserver", "0.0.0.0:8000"]