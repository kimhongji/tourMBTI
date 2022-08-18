# README

### init & local run
```shell
rbenv versions
rbenv install 2.7.6 && rbenv rehash

eval "$(rbenv init -)"
rbenv shell 2.7.6

gem update --system
bin/bundle install

RAILS_ENV=development bin/rails assets:precompile
RAILS_ENV=development bin/rails server -p 3000
```

### DB migrate
- https://rubykr.github.io/rails_guides/migrations.html
```
$ bin/rails db:migrate:status
$ bin/rails db:rollback STEP=1
$ RAILS_ENV=development bin/rails db:migrate
```

### Docker & Prod Run (Using Nginx & Unicorn)
```
$ docker build -t rails_test .
$ docker run -d -p 3000:3000 rails_test
```
