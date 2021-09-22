FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn uvloop \
    && mkdir store \
    && chmod 777 store/

COPY . .

ARG workers_per_core=0.25

ARG max_workers=2

ARG timeout=600

ARG port=3000

ENV WORKERS_PER_CORE=$workers_per_core \ 
    MAX_WORKERS=$max_workers \
    TIMEOUT=$timeout \
    PORT=$port

EXPOSE $port

CMD [ "python", "-m", "gunicorn", "-c", "gunicorn.conf.py", "app.main:app" ]