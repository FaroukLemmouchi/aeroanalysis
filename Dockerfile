FROM python:3.8 


#RUN apt-get update && apt-get upgrade -y
#RUN apt install python3-opencv -y
WORKDIR /app
#RUN /usr/local/bin/python3 -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt
COPY . /app  
#RUN source /app/newflask/bin/activate
#ADD requirements.txt requirements.txt

#EXPOSE 8050

#ENTRYPOINT ["python3", "./main.py", "DEFAULT"] 
#ENTRYPOINT ["./go.sh"] 
#CMD ["gunicorn","--bind","0.0.0.0:8000","--workers","2","main:app"]
CMD ["gunicorn","--bind","0.0.0.0:8000","--workers","1","main:app"]
