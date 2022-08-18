FROM ruby:2.7.6-bullseye

# see update.sh for why all "apt-get install"s have to stay as one long line
RUN apt-get update && apt-get install -y nodejs --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get install -y ca-certificates \
    && echo '-k' > ~/.curlrc \
    && curl -sL https://deb.nodesource.com/setup_10.x | bash - \
    && apt-get install -y --force-yes nginx \
    && apt-get install -y --force-yes nodejs

ENV RAILS_VERSION 5.2.8

RUN gem install rails --version "$RAILS_VERSION"

RUN mkdir -p /app /app/web/tmp/pids
WORKDIR /app

COPY . /app/web/
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf


WORKDIR /app/web

RUN gem install bundler \
        && bin/bundle install \
        && bin/bundle version

EXPOSE 3000

CMD ["/app/web/script-web.sh"]