## ./Dockerfile

# 기본 이미지 설정
FROM python:3.9.7

# 작업 디렉토리 설정
WORKDIR /todo_api

# 현재 디렉토리로 소스 코드 복사
COPY . /todo_api

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask_restx flask_sqlalchemy flask_bcrypt

# 타임존 설정
ENV TZ Asia/Seoul

# 애플리케이션 실행 명령
CMD ["python", "api.py"]