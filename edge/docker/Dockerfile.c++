FROM ubuntu:22.04 AS builder
RUN apt-get update && apt-get install -y build-essential cmake
WORKDIR /app
COPY edge/firmware .
RUN mkdir build && cd build && cmake .. && make
FROM ubuntu:22.04
COPY --from=builder /app/build/firmware /app/firmware
CMD ["/app/firmware"]
