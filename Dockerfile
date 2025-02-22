# 
FROM python:3.9

# 
WORKDIR /app

# 
COPY ./requirements.txt /app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
# 
COPY ./src/server.py /app/
COPY ./src/interfaces /app/interfaces 
COPY ./src/utils /app/utils
COPY ./src/log /app/log

# 
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]

