FROM python:3.10.12
RUN pip install notebook==7.0.6
RUN pip install pysolr==3.9.0
RUN pip install spacy==3.6.0
RUN pip install de_dep_news_trf@https://github.com/explosion/spacy-models/releases/download/de_dep_news_trf-3.5.0/de_dep_news_trf-3.5.0.tar.gz
RUN useradd -u 1000 docker_user
RUN mkdir /home/docker_user
RUN chown -R docker_user:docker_user /home/docker_user
USER docker_user

