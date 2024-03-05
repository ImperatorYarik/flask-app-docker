FROM python:3.8
WORKDIR /app

COPY ./ /app
COPY build.sh /app
RUN chmod +x build.sh
CMD ["/app/build.sh"]

