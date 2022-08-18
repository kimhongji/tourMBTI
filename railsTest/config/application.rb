require_relative 'boot'

require 'rails/all'

# Require the gems listed in Gemfile, including any gems
# you've limited to :test, :development, or :production.
Bundler.require(*Rails.groups)

module RailsTest
  class Application < Rails::Application
    # Settings in config/environments/* take precedence over those specified here.
    # Application configuration should go into files in config/initializers
    # -- all .rb files in that directory are automatically loaded.
    #
    config.i18n.default_locale = :ko
    config.time_zone = "Seoul"
    config.eager_load_paths << Rails.root.join('lib')
    config.exceptions_app = self.routes
    config.assets.paths << Rails.root.join("app", "assets", "fonts")

    #for Web Console is activated in the local environment
    if Rails.env.to_sym == :local
      config.log_level = :debug
      config.web_console.development_only = false
    end
  end
end
