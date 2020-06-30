FROM python:3.8
LABEL maintainer "Johan Vroonen"
ENV DASH_DEBUG_MODE True

RUN pip install --upgrade pip
RUN set -ex && \
    pip install dash dash-daq dash-bootstrap-components
COPY requirements.txt /
RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 8050
COPY ./ ./


CMD ["python", "./app.py"]



