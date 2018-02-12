# blockchain_proto

Docker 이미지 생성 및 테스트방법

1. Docker 실행 및 Dockerfile 디렉터리로 이동 후 아래 단계 차례로 수행

	docker build -t blockchain_proto .

	*blockchain_proto는 생성할 이미지 명이므로 자유롭게 입력가능

    docker images

    docker run --rm -p 5001:5000 --name blockproto blockchain_proto

    *포트 5001은 도커 호스트에 할당 및 request시 사용하므로 자유롭게 사용가능

    위 명령 까지 수행 시 0.0.0.0:5000 포트로 리스닝 중


2. Docker 컨테이너 정상 기동 후 현재 가능한 테스트 종류 
    *도커 호스트 IP가 192.168.99.100이라고 가정
    1) http://192.168.99.100:5001/chains
    	-체인에 등록된 전체 블록 리스트 요청
	2) http://192.168.99.100:5001/transactions/new
		-체인에 새로운 거래 블록 생성
	3) http://192.168.99.100:5001/chains/hash
		-체인에 등록된 모든 블록의 해시값 요청 (추후 해시값 검증 시 사용가능 로직)