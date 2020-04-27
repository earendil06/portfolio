FROM python:3-alpine


WORKDIR /app

COPY . /app
RUN apk add curl && pip install --no-cache-dir -r requirements.txt

HEALTHCHECK CMD curl --fail http://localhost:5000/health || exit 1

CMD [ "python", "./app.py" ]
