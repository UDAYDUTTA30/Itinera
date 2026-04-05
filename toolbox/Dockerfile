FROM ubuntu:22.04

WORKDIR /app

COPY toolbox /app/toolbox
COPY tools.yaml /app/tools.yaml

RUN chmod +x /app/toolbox

EXPOSE 8080

ENTRYPOINT ["/app/toolbox"]
CMD ["--tools-file", "/app/tools.yaml", "--address", "0.0.0.0", "--port", "8080"]
