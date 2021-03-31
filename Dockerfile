FROM python:3.8-slim

WORKDIR /TODO/
ADD . /TODO/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5353

CMD python main.py