## The goal of this folder is to compare chunking strategies between Unstructured and llangchain

## In order for this to work you must specify a unstructured API server. For development purposes I used the docker container from [https://github.com/Unstructured-IO/unstructured-api](https://github.com/Unstructured-IO/unstructured-api)

Use the commands:
docker pull downloads.unstructured.io/unstructured-io/unstructured-api:latest
docker run -p 8000:8000 -d --rm --name unstructured-api downloads.unstructured.io/unstructured-io/unstructured-api:latest --port 8000 --host 0.0.0.0

Note: The Docker container is big! It is 18GB. It would be nice to reduce the size at some point.