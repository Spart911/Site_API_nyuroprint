# start by pulling the python image
FROM python:3.10.14-slim

# install libgl1-mesa-glx and libglib2.0-0
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# copy the requirements file into the image
COPY ./requirements.txt /ai/requirements.txt

# switch working directory
WORKDIR /ai

# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# copy every content from the local file to the image
COPY . /ai

EXPOSE 3000

# configure the container to run in an executed manner
ENTRYPOINT ["python"]
CMD ["main.py"]
