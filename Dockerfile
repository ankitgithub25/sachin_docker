FROM python:3
WORKDIR /app
COPY ./app /app
RUN  pip install -r /app/requirements.txt
CMD ["python3","./main.py","$RUN_DIR" ]