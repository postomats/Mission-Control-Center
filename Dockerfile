FROM python:3.11


RUN apt update -y && apt -y upgrade && apt -y install wireguard
COPY wg0.conf /etc/wireguard/wg0.conf
RUN wg-quick wg0.conf
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

ENTRYPOINT [ "wg-quick", "wg0.conf", "&&", \
        "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]