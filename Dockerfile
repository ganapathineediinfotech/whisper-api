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
    npm && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone Whisper.cpp
RUN git clone https://github.com/ggml-org/whisper.cpp.git

# Build Whisper.cpp (disable CPU-specific optimizations)
RUN cd whisper.cpp && \
    cmake -B build \
      -DGGML_NATIVE=OFF \
      -DGGML_AVX=OFF \
      -DGGML_AVX2=OFF \
      -DGGML_FMA=OFF \
      -DGGML_F16C=OFF && \
    cmake --build build -j$(nproc)

# Download multilingual model
RUN cd whisper.cpp && \
    bash models/download-ggml-model.sh medium

COPY package*.json ./

RUN npm install

COPY . .

RUN mkdir -p uploads

EXPOSE 3000

CMD ["node", "server.js"]