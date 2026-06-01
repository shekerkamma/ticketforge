SHELL := /bin/bash

.PHONY: bootstrap backend-install frontend-install dev backend frontend smoke-test

bootstrap:
	./scripts/bootstrap.sh

backend-install:
	cd backend && python3 -m pip install -e .[dev] --break-system-packages

frontend-install:
	cd frontend && npm install

dev:
	./scripts/dev.sh

backend:
	cd backend && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm run dev

smoke-test:
	./scripts/smoke_test.sh
