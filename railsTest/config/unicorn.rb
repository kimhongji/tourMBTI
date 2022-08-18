app_path          = File.dirname(File.expand_path('..', __FILE__))

working_directory "#{app_path}"
pid               "#{app_path}/tmp/pids/unicorn.pid"
# stderr_path       "#{app_path}/log/unicorn.log"
# stdout_path       "#{app_path}/log/unicorn.log"

listen            "/tmp/unicorn.production.sock"
#listen              3000, :tcp_nopush => true
worker_processes    8
timeout             30
preload_app         true

GC.respond_to?(:copy_on_write_friendly=) and
  GC.copy_on_write_friendly = true

check_client_connection false

before_fork do |server, worker|
  defined?(ActiveRecord::Base) and
    ActiveRecord::Base.connection.disconnect!
end

after_fork do |server, worker|
  # the following is *required* for Rails + "preload_app true",
  defined?(ActiveRecord::Base) and
    ActiveRecord::Base.establish_connection
end