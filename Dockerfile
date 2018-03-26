FROM python:3.6-alpine3.7

RUN python -m pip install Flask

ADD foreman_stub.py /usr/src/app/
ENV PYTHONPATH=/usr/src/app/

EXPOSE 8080
CMD ["python", "-m", "foreman_stub"]
