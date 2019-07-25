FROM python:3-alpine

ENV APP_DIR /app

RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

COPY . ${APP_DIR}
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
HEALTHCHECK CMD curl --fail http://localhost:5000 || exit 1

CMD [ "python", "./app.py" ]