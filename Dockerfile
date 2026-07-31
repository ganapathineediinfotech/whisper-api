FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    wget \
    ffmpeg \
    curl \
    build-essential \
    cmake \
    nodejs \
    npm

WORKDIR /app

# Clone Whisper.cpp
RUN git clone https://github.com/ggml-org/whisper.cpp.git

# Build Whisper
RUN cd whisper.cpp && \
    cmake -B build && \
    cmake --build build -j

# Download multilingual model
RUN cd whisper.cpp && \
    bash models/download-ggml-model.sh medium

COPY package*.json ./
RUN npm install

COPY . .

RUN mkdir uploads

EXPOSE 3000

CMD ["node","server.js"]