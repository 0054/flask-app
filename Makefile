

build:
	docker build -t flask-app:latest .

start-app: 
	docker run --rm -d -p 5000:5000 --name flask-app flask-app:latest

stop-app: 
	docker stop flask-app || true

delete-container:
	docker rm flask-app || true

pytest: 
	pytest || true
	docker stop flask-app || true
	

run-tests: build stop-app delete-container start-app pytest stop-app
