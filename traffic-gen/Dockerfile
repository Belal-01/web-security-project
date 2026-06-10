FROM alpine:latest
RUN apk add --no-cache curl
COPY script.sh /script.sh
RUN chmod +x /script.sh
CMD ["/script.sh"]
