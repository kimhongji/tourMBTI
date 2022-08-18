#!/bin/bash

# start Nginx
service nginx start

export RAILS_ENV=production

RAILS_ENV=${RAILS_ENV} bin/rails assets:precompile
RAILS_ENV=${RAILS_ENV} bin/rails db:create
RAILS_ENV=${RAILS_ENV} bin/rails db:migrate
RAILS_ENV=${RAILS_ENV} bin/rails db:migrate:status
#RAILS_ENV=${RAILS_ENV} bin/rails server -b 0.0.0.0 -p 3000

# start Unicorn
bin/bundle exec unicorn -c config/unicorn.rb