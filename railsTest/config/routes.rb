Rails.application.routes.draw do
  get '' => 'home#index'
  get 'tour_map' => 'tour_map#index'
  get 'tour_keywords/search' => 'tour_keywords#search', :as => :tour_keyword_search
  resources :tour_keywords do
    get :autocomplete_tour_keyword_name, :on => :collection
  end
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
