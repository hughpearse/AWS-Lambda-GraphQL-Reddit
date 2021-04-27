FROM public.ecr.aws/bitnami/python:latest
USER root
COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py
RUN pip3 install -r requirements.txt
EXPOSE 80
CMD ["python3", "/app/app.py"]

