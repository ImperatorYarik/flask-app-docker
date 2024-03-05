FROM python:3
WORKDIR /app

COPY ./ /app
COPY build.sh /app
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x build.sh
CMD ["/app/build.sh"]

