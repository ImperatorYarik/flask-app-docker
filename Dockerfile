FROM python:3
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ .
COPY build.sh .

CMD ["python", "start.py"]

