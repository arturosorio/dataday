FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip
RUN ./aws/install
RUN pip install --no-cache-dir -r requirements.txt

COPY inference_container .

#CMD ["python", "-i", "./main.py"] LOCAL TEST
CMD [ "python", "./main.py" ]
