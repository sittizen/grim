FROM python:3.13.1-alpine

ARG wheel=grimweb-0.0.1-py3-none-any.whl

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY dist/$wheel /app/$wheel
RUN pip install --no-cache-dir --upgrade  /app/$wheel

COPY files /
EXPOSE 8000

ENTRYPOINT ["textual", "serve", "-p", "8000", "-h", "0.0.0.0" , "/usr/local/lib/python3.13/site-packages/grim/textualweb/app.py"]
