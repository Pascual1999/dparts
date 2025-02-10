# pull official base image
FROM python:3.13.2-slim-bullseye

# set work directory
WORKDIR /dparts

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
#COPY ./entrypoint.sh .
#RUN sed -i 's/\r$//g' /dparts/entrypoint.sh
#RUN chmod +x /dparts/entrypoint.sh

# copy project
COPY . .

# copy entrypoint.sh
#ENTRYPOINT [ "/dparts/entrypoint.sh"]