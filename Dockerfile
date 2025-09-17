FROM python:3.11

ADD requirements.txt requirements.txt
ADD bot bot

RUN pip install -r requirements.txt
CMD python3 -m bot
