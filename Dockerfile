FROM python:3.6-alpine3.7

RUN python -m pip install Flask

WORKDIR /usr/src/app/
ADD foreman_stub.py .
ADD fixtures fixtures
ENV PYTHONPATH=.

EXPOSE 8080
CMD ["python", "-m", "foreman_stub"]
