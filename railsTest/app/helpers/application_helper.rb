module ApplicationHelper
  # ERROR message
  def flash_message
    ret = []
    flash.each do |key, value|
      next unless [:success, :warning, :danger, :info, :alert, :notice].include? key.to_sym
      ret << "<div class=\"alert alert-#{key}\">#{value}</div>"
    end
    ret.join.html_safe
  end
end
