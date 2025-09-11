#IMAGE
FROM python:3.12-slim

#DIRECTORY
WORKDIR /app

#COPY requeriments.txt
COPY requeriments.txt .

#INSTALL DEPENDENCIES
RUN pip install --no-cache-dir -r requeriments.txt

#COPY CODE
EXPOSE 5000

#RUN
CMD ["python", "main.py"]