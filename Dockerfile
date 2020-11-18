# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:latest

# create root directory for our project in the container
RUN mkdir /myfit_utility

# Set the working directory to /music_service
WORKDIR /myfit_utility

RUN apt-get update
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 libgbm1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN apt-get -fy install
RUN /usr/bin/google-chrome --disable-gpu --headless --no-sandbox --remote-debugging-address=0.0.0.0 --remote-debugging-port=9222 --user-data-dir=/data &

# Copy the current directory contents into the container at /music_service
ADD . /myfit_utility/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
EXPOSE 3306
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
