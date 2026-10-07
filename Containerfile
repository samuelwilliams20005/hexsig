FROM python:3.13-slim
WORKDIR /app
COPY hexsig.py .
ENTRYPOINT ["python", "hexsig.py"]