web: gunicorn backend.main:app --workers 1 --threads 8 --preload
release: (cd frontend && yarn && yarn build)
