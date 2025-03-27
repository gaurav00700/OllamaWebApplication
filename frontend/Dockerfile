FROM python:3.9-slim

COPY ./frontend /workdir/frontend

WORKDIR /workdir

# check the contents 
RUN ls -la

# Install dependencies
RUN pip install --upgrade pip

# RUN pip3 install -r /workdir/frontend/requirements.txt
RUN pip install \
    streamlit \
    requests \
    pydantic 

EXPOSE 8500

ENV BACKEND_ENDPNT=http://localhost:8000/ask
    
CMD ["streamlit", "run", "frontend/app.py", "--server.port", "8500", "--server.address", "0.0.0.0"]
# CMD ["/bin/bash"]