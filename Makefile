.PHONY: run image query configure

install:
	ansible-playbook -i hosts playbook.yml

run:
	docker run -p 8035:80 --mount type=bind,source="$(PWD)/models",target=/usr/src/app/models deepspeech-server

image:
	docker build -t deepspeech-server .

query:
	pipenv run python client.py ./file16000.wav alpha.local:8035

activate:
	touch /media/andrew/boot/ssh
	umount /media/andrew/boot
	umount /media/andrew/rootfs

setup:
	./setup_host.sh

deepspeech:
	python DeepSpeech/util/taskcluster.py --arch arm --target native

wifi:
	./wifi_host.sh
