FROM  --platform=linux/amd64 ubuntu:18.04
RUN apt update -y
RUN apt -y install apache2
RUN apt -y install python2.7
RUN apt -y install zip
RUN rm -f /var/www/html/index.html
WORKDIR /home/picksmart
