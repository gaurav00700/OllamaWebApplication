FROM python:3.9-slim

COPY ./backend /workdir/backend

WORKDIR /workdir

# check the contents 
RUN ls -la

RUN pip install --upgrade pip

# RUN pip3 install -r /workdir/backend/requirements.txt
RUN pip install \
        fastapi \
        uvicorn \
        pydantic \
        redis \
        requests 

ENV LLM_NAME=qwen2.5-coder:3b
ENV LLM_HOST_NAME=localhost
ENV LLM_PORT=11433
ENV REDIS_HOST_NAME=localhost
ENV REDIS_PORT=6379

EXPOSE 8000

CMD ["uvicorn", "backend.app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]