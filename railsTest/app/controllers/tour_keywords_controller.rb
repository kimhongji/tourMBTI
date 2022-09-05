class TourKeywordsController < ApplicationController
  before_action :set_tour_keyword, only: %i[ show edit update destroy ]
  autocomplete :tour_keyword, :name, :full => true

  # GET /tour_keywords or /tour_keywords.json
  def index
    @tour_keywords = TourKeyword.all
    @tour_map = TourMap.all
  end

  def search
    keyword =  params[:name]

    # 검색 엔진이 들어가야함
    @keyword = TourKeyword.find_by_name(keyword)
    keywords = @keyword.keywords

    value_hash = JSON.parse(keywords)
    sorted_array = value_hash.sort_by {|_key, value| value}.reverse
    @keywords_result = sorted_array.take(10).to_h
    require 'json'
    @keywords_json = sorted_array.map{ |array|
      {
        "name": array[0],
        "weight": array[1]
      }
    }.to_json
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
