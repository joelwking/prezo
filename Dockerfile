#
#     Copyright (c) 2021 World Wide Technology
#     All rights reserved.
#
#     author: joel.king@wwt.com
#     written:  26 May 2021
#     references:
#       activate virtualenv: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
#       https://github.com/wwt/network-endpoint-mapper
#
FROM python:3.8.10-slim-buster
ENV VIRTUAL_ENV=/opt/prezo
LABEL maintainer="Joel W. King" email="joel.king@wwt.com"
RUN apt update && \
    apt -y install git && \
    apt -y install python3-venv && \
    apt -y install python3-dev && \
    apt -y install build-essential && \
    pip3 install --upgrade pip 
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
#
# We need the requirements.txt files for installation
#
RUN mkdir /prezo
COPY . /prezo
WORKDIR /prezo
RUN pip install -r requirements.txt
#
#   The virtual environment is /opt/prezo
#
#   The work directory is /prezo
#
#   And, finally, the underlying directory is /workspaces/prezo