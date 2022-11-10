# Use https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/
# hello world demo
# FROM tiangolo/uwsgi-nginx-flask:python3.8

# COPY ./app /app
FROM python:3.8

# LABEL maintainer="xxx <xx@qq.com>"

COPY . /detectweb

WORKDIR /detectweb

# RUN -m pip install --upgrade pip
RUN pip install -r requirements.txt -i https://mirror.baidu.com/pypi/simple && pip install gunicorn
# &&chmod 755 run_server.sh

EXPOSE 8080

# ENTRYPOINT [ "./run_server.sh" ]
