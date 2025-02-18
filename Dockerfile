FROM mcr.microsoft.com/vscode/devcontainers/python:3.10
RUN apt-get update && \
    apt-get install -y git --no-install-recommends
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install black && \
    pip install --no-cache-dir --upgrade -r /requirements.txt && \
    rm requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/home"
WORKDIR /home
