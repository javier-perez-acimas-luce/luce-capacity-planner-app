FROM gcr.io/google-appengine/python
MAINTAINER Luce Innovative Technologies

# Create a virtualenv for dependencies. This isolates these packages from
# system-level packages.
# Use -p python3 or -p python3.7 to select python version. Default is version 2.
RUN virtualenv /env -p python3.7

# Setting these environment variables are the same as running
# source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

WORKDIR /home/
ENV PORT='8080'
ENV HOST='0.0.0.0'
ENV GOOGLE_APPLICATION_CREDENTIALS='/home/credentials.json'
EXPOSE 8080
COPY ./ ./
RUN pip install -r requirements.txt
CMD [ "python", "-u", "main.py" ]