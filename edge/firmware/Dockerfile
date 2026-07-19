# Stage 1: Build
FROM ubuntu:22.04 AS builder

# Install build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libopencv-dev \
    libtensorflow-lite-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy CMakeLists.txt first
COPY CMakeLists.txt .
RUN mkdir -p build && cd build && cmake .. && make -j$(nproc)

# Copy source code
COPY src ./src
COPY include ./include
RUN cd build && cmake .. && make -j$(nproc)

# Stage 2: Run (Minimal Ubuntu)
FROM ubuntu:22.04

# Security: Non-root user
RUN useradd -m -u 1000 nexusguard && \
    apt-get update && apt-get install -y --no-install-recommends \
    libopencv4.5-java \
    libtensorflow-lite-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/build/firmware /app/firmware

# Run as non-root
USER nexusguard

CMD ["/app/firmware"]
