class HomeController < ApplicationController
  def index
    @tour_keywords = TourKeyword.all
    @tour_map = TourMap.all
  end
end