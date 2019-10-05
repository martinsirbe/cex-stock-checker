FROM python:3

ENV CUSTOM_CONFIG "/config/checker.yaml"

COPY stock_check.py .
COPY config config

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD [ "python", "stock_check.py" ]
