FROM python:3.6

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY Imports/WDIEXCEL_Data_part1.csv /app/Imports/
COPY Imports/WDIEXCEL_Data_part2.csv /app/Imports/

CMD ["python", "main.py"]