FROM python:3
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ .
COPY build.sh .
RUN chmod +x build.sh
CMD ["./build.sh"]

