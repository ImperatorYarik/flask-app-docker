FROM python:3.8
WORKDIR /app

COPY ./ /app
COPY build.sh /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x build.sh
CMD ["/app/build.sh"]

