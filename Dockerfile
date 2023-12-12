FROM python:3.10
WORKDIR /app

RUN apt-get update -qq && \
    apt-get install -y \
    libfluidsynth3 build-essential libasound2-dev libjack-dev git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN git clone --branch=main https://github.com/magenta/mt3 /app/mt3

RUN pip install jax[cuda11_local] nest-asyncio pyfluidsynth==1.3.0 -e /app/mt3 -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html

RUN apt-get update -qq && \
    apt-get install -y curl && \
    curl https://sdk.cloud.google.com | bash && \
    apt-get remove -y --auto-remove curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
ENV PATH $PATH:/root/google-cloud-sdk/bin

RUN mkdir -p /app/checkpoints && \
    gsutil -q -m cp -r gs://mt3/checkpoints/* /app/checkpoints/

# COPY . /app

RUN pip install note-seq Streamlit protobuf

RUN apt-get update -qq && \
    apt-get install -y ffmpeg


COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "--server.port", "8501", "MT3_MIDI.py"]