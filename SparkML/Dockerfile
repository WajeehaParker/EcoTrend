FROM python:3.6

# Install Java
RUN apt-get update && apt-get install -y default-jre
#COPY java/ /usr/java/

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install scikit-learn

COPY regression.py .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"] 

CMD ["python", "regression.py"]