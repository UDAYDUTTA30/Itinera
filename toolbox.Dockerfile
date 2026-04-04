FROM --platform=linux/amd64 ubuntu:22.04
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN curl -L -o toolbox https://storage.googleapis.com/genai-toolbox/v0.9.0/linux/amd64/toolbox &&     chmod +x toolbox
COPY tools.yaml /app/tools.yaml
EXPOSE 8080
ENTRYPOINT ["/bin/sh", "-c", "/app/toolbox --tools-file /app/tools.yaml --address 0.0.0.0 --port ${PORT:-8080}"]
