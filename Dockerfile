FROM python:3.11-slim

# Install system dependencies needed for building packages
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     gcc \
#     g++ \
#     git \
#     libffi-dev \
#     libblas-dev \
#     liblapack-dev \
#     libatlas-base-dev \
#     libopenblas-dev \
#     python3-dev \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./

# RUN apt-get update && apt-get install -y libpq-dev

# RUN apt-get update && apt-get install -y curl build-essential && \
#     curl https://sh.rustup.rs -sSf | sh -s -- -y && \
#     ln -s $HOME/.cargo/bin/* /usr/local/bin/

RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

CMD ["uvicorn", "app.main.app", "--host", "0.0.0.0", "--port", "8000"]
