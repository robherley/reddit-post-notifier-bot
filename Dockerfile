FROM python:3.7

WORKDIR /bot

COPY bot.py requirements.txt ./

RUN pip install -r requirements.txt

CMD [ "python", "-u", "bot.py" ]