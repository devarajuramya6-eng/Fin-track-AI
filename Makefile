all: install build test

install:
	python -m pip install -r backend/requirements.txt
	cd frontend && npm install

build:
	cd frontend && npm run build

test:
	pytest

start:
	python main.py

dev:
	cd frontend && npm run dev
