.PHONY: run image query

run:
	docker run -p 8035:80 --mount type=bind,source="$(PWD)/models",target=/usr/src/app/models deepspeech-server

image:
	docker build -t deepspeech-server .

query:
	pipenv run python client.py ./file16000.wav localhost:8035

activate:
	touch /media/andrew/boot/ssh
	sed -ri 's/( ip=192.168.1.222)?$$/ ip=192.168.1.222/' /media/andrew/boot/cmdline.txt