class TourKeywordsController < ApplicationController
  before_action :set_tour_keyword, only: %i[ show edit update destroy ]
  autocomplete :tour_keyword, :name, :full => true

  # GET /tour_keywords or /tour_keywords.json
  def index
    @tour_keywords = TourKeyword.all
    @tour_map = TourMap.all
  end

  def recommendations (tour_list, target_keyword_list)
    tour_list.map! do |tour|

      intersection = (tour[:keyword_list] & target_keyword_list).size
      union = (tour[:keyword_list] | target_keyword_list).size

      tour[:jaccard_index] = (intersection.to_f / union.to_f) rescue 0.0
      tour
    end.sort_by { |tour| 1 - tour[:jaccard_index] }
  end

  def search
    name =  params[:name]

    # 검색 엔진이 들어가야함
    begin
      require 'json'
      @keyword = TourKeyword.find_by_name(name)
      keywords = @keyword.keywords
      sorted_array = JSON
                       .parse(keywords)
                       .sort_by {|_key, value| value}
                       .reverse
      target_keyword_list = sorted_array
        .map{
          |k, v|
          result = []
          while (v > 0)
            v = v - 1
            result << k
          end
          result
        }.flatten

      tour_list = TourKeyword.all
                                  .filter { |k| k.name != name }
                                  .map {
                                    |k|
                                    {
                                      name: k.name,
                                      keywords: JSON
                                                  .parse(k.keywords)
                                                  .sort_by {|key, value| value}
                                                  .reverse
                                                  .map{|key, value| key}
                                                  .take(5)
                                                  .join(", "),
                                      keyword_list: JSON.parse(k.keywords)
                                          .sort_by {
                                            |_key, value|
                                            value
                                          }
                                          .reverse.take(10)
                                          .map{ |k, v|
                                            result = []
                                            while (v > 0)
                                              v = v - 1
                                              result << k
                                            end
                                            result
                                          }
                                          .flatten
                                    }
                                  }
      @recommend_list = recommendations(tour_list, target_keyword_list).take(10)
      @keywords_result = sorted_array.take(10).to_h
      @keywords_json = sorted_array.take(25).map{ |array|
        {
          "name": array[0],
          "weight": array[1]
        }
      }.to_json
    rescue NoMethodError => e
      flash[:notice] =  "검색어를 찾을수 없습니다!"
      redirect_to action: 'index'
    end
  end

  # GET /tour_keywords/1 or /tour_keywords/1.json
  def show
  end

  # GET /tour_keywords/new
  def new
    @tour_keyword = TourKeyword.new
  end

  # GET /tour_keywords/1/edit
  def edit
  end

  # POST /tour_keywords or /tour_keywords.json
  def create
    @tour_keyword = TourKeyword.new(tour_keyword_params)

    respond_to do |format|
      if @tour_keyword.save
        format.html { redirect_to tour_keyword_url(@tour_keyword), notice: "Tour keyword was successfully created." }
        format.json { render :show, status: :created, location: @tour_keyword }
      else
        format.html { render :new, status: :unprocessable_entity }
        format.json { render json: @tour_keyword.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /tour_keywords/1 or /tour_keywords/1.json
  def update
    respond_to do |format|
      if @tour_keyword.update(tour_keyword_params)
        format.html { redirect_to tour_keyword_url(@tour_keyword), notice: "Tour keyword was successfully updated." }
        format.json { render :show, status: :ok, location: @tour_keyword }
      else
        format.html { render :edit, status: :unprocessable_entity }
        format.json { render json: @tour_keyword.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /tour_keywords/1 or /tour_keywords/1.json
  def destroy
    @tour_keyword.destroy

    respond_to do |format|
      format.html { redirect_to tour_keywords_url, notice: "Tour keyword was successfully destroyed." }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_tour_keyword
      @tour_keyword = TourKeyword.find(params[:id])
    end

    # Only allow a list of trusted parameters through.
    def tour_keyword_params
      params.require(:tour_keyword).permit(:name, :keywords)
    end
end
