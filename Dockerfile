FROM python:3.6-alpine

WORKDIR /app

# 필요한 패키지 설치
ADD requirements.txt /app
RUN cd /app && \
    pip install -r requirements.txt

#Dockerfile이 위치한 디렉터리의 
ADD . /app

#5000번 포트 오픈
EXPOSE 5000

#컨테이너 실행 시 payloads.py 실행으로 5000번포트 리스닝
CMD ["python", "payloads.py", "--port", "5000"]
