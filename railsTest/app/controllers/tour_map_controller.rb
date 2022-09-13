class TourMapController < ApplicationController
  # GET /tour_map
  def index
    @tour_keywords = TourKeyword.all
    @tour_map = TourMap.all
  end

  def tour_list_from_xy
    require 'uri'
    require 'net/http'
    require 'nokogiri'

    mapX = params[:mapX]
    mapY = params[:mapY]

    url = 'http://apis.data.go.kr/B551011/KorService/locationBasedList?' +
      'serviceKey=zvyVv9%2BUiLc7SY5wYKup3vpZnaUd05Zj4MfgBo4DqQXjTN3180b3bINu1x5CKbLqduyzU5YO%2BIPHXdIJINwjYQ%3D%3D&' +
      'numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=AppTest&mapX=' +
      mapX + '&mapY=' + mapY + '&radius=1000&listYN=Y&contentTypeId=12'

    uri = URI.parse(url)
    request = Net::HTTP::Get.new(uri)
    body = Net::HTTP.start(uri.host, uri.port) {|http|
      http.request(request)
    }.body
    response = Nokogiri::XML(body)

    result = []
    response.css("item").each do |item|
      begin
        # find 하지 못할 경우 RecordNotFound Error를 Throw합니다.
        tour = TourKeyword.find_by_name(item.css("title").text)
        keywords = tour.keywords
        value_hash = JSON.parse(keywords)
        sorted_array = value_hash.sort_by {|key, value| value}.reverse
        keywords = sorted_array.map{|key, value| key}.take(3).join(", ")

        result << {
          "addr": item.css("addr1").text,
          "title": item.css("title").text,
          "mapX": item.css("mapx").text.to_f,
          "mapY": item.css("mapy").text.to_f,
          "keywords": keywords
        }
      rescue ActiveRecord::RecordNotFound, NoMethodError => e
        result << {
          "addr": item.css("addr1").text,
          "title": item.css("title").text,
          "mapX": item.css("mapx").text.to_f,
          "mapY": item.css("mapy").text.to_f,
          "keywords": "키워드 없음"
        }
      end
    end
    render json: result
  end
end
