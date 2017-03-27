FROM ubuntu:14.04

# System packages
RUN apt-get update && apt-get install -y curl

# Install miniconda to /miniconda
RUN curl -LO http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
RUN bash Miniconda-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}

ENV FLASK_APP=run.py
ENV FLASK_CONFIG=development

# Copy Application
ADD . /app

# Install dependencies
RUN conda install python=3.5
RUN pip install -r /app/requirements.txt

ENV API_SERVER_HOME=/app
WORKDIR "$API_SERVER_HOME"

RUN cd /app

# Set the ENTRYPOINT to use bash
# (this is also where you’d set SHELL,
# if your version of docker supports this)
#ENTRYPOINT [ “/bin/bash”, “-c” ]

EXPOSE 8888

# We set ENTRYPOINT, so while we still use exec mode, we don’t
# explicitly call /bin/bash
ENTRYPOINT ["/miniconda/bin/python", "run.py"]