FROM python:3.9-slim

# working directory in the container
WORKDIR /usr/src/app

# Install the necessary packages 
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
#CMD ["sh", "-c", "python app.py & python another_script.py"]
# To DO : MAhaveer : A python script can be added to keep loading data automatically
