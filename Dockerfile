FROM python:3.6-alpine3.7

# Pin distribution versions via pip's constraints feature
ADD constraints.txt .
# Then, install app requirements
RUN python -m pip install -c constraints.txt Flask

# Put app into work dir
WORKDIR /usr/src/app/
ADD foreman_stub.py .
ADD fixtures fixtures
ENV PYTHONPATH=.

ADD COPYING .

EXPOSE 8080
CMD ["python", "-m", "foreman_stub"]
