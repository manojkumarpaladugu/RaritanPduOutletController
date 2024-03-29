ARG IMAGE_BASE="ubuntu:22.04"

FROM ${IMAGE_BASE}

ARG DEBIAN_FRONTEND=noninteractive

# Update the system
RUN apt-get update      && \
    apt-get upgrade -y

RUN apt-get install -y  \
    python3             \
    python3-pip         \
    python3-tk          \
    python3-pil         \
    python3-pil.imagetk

RUN pip3 install    \
    raritan         \
    customtkinter   \
    pyinstaller