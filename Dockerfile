FROM python:3.11
ADD . /app
WORKDIR /app
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
ENV FLASK_APP=/app/app
ENTRYPOINT ["flask", "run", "-h", "0.0.0.0", "--port", "5001"]