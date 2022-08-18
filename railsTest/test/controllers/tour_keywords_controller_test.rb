require 'test_helper'

class TourKeywordsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @tour_keyword = tour_keywords(:one)
  end

  test "should get index" do
    get tour_keywords_url
    assert_response :success
  end

  test "should get new" do
    get new_tour_keyword_url
    assert_response :success
  end

  test "should create tour_keyword" do
    assert_difference('TourKeyword.count') do
      post tour_keywords_url, params: { tour_keyword: { keywords: @tour_keyword.keywords, name: @tour_keyword.name } }
    end

    assert_redirected_to tour_keyword_url(TourKeyword.last)
  end

  test "should show tour_keyword" do
    get tour_keyword_url(@tour_keyword)
    assert_response :success
  end

  test "should get edit" do
    get edit_tour_keyword_url(@tour_keyword)
    assert_response :success
  end

  test "should update tour_keyword" do
    patch tour_keyword_url(@tour_keyword), params: { tour_keyword: { keywords: @tour_keyword.keywords, name: @tour_keyword.name } }
    assert_redirected_to tour_keyword_url(@tour_keyword)
  end

  test "should destroy tour_keyword" do
    assert_difference('TourKeyword.count', -1) do
      delete tour_keyword_url(@tour_keyword)
    end

    assert_redirected_to tour_keywords_url
  end
end
