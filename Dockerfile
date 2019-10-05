FROM python:3

COPY stock_check.py .
COPY config config

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD [ "python", "stock_check.py" ]
