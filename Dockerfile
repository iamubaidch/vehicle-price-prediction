# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN python -m pip install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app


