FROM python:3.8


COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./src .
EXPOSE 5000
CMD ["python", "start.py"]

