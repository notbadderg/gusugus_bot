FROM python:3

WORKDIR /usr/src/app

COPY /bot/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY /bot .

CMD [ "python", "./main.py" ]