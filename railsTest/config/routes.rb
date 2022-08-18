Rails.application.routes.draw do
  get '' => 'home#index'
  resources :tour_keywords
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
