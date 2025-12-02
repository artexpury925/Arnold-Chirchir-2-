FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt update && apt install -y git curl build-essential

# Install vLLM or use llama.cpp
RUN pip install vllm fastapi uvicorn[standard] httpx

# Copy everything
COPY . .

EXPOSE 8000 8001

CMD ["bash start.sh