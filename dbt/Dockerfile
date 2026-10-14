FROM python:3.12-slim
RUN pip install --no-cache-dir dbt-core==1.10.15 dbt-postgres==1.9.1
WORKDIR /dbt
ENV DBT_PROFILES_DIR=/dbt
ENTRYPOINT ["dbt"]
