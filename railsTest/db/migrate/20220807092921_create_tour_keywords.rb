class CreateTourKeywords < ActiveRecord::Migration[5.0]
  def change
    create_table :tour_keywords do |t|
      t.string :name
      t.text :keywords
    end
  end
end
