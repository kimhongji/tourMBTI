class TourMapController < ApplicationController
  # GET /tour_map
  def index
    @tour_keywords = TourKeyword.all
    @tour_map = TourMap.all
  end
end
