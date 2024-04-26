FROM apache/airflow:2.8.1
USER root
RUN apt-get update && apt-get install -y --no-install-recommends wget unzip build-essential libsndfile1 libopenmpi-dev && apt-get autoremove -yqq --purge && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get install wget

COPY requirements.txt /


USER airflow
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt