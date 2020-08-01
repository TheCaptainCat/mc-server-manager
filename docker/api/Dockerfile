FROM python:3.8-slim-buster
WORKDIR /api
COPY server_mgr server_mgr
COPY requirements.txt requirements.txt
COPY api.py api.py

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["python", "api.py", "run_server"]
