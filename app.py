from flask import Flask, render_template, request

app = Flask(__name__)


from api import rating_predictor


import pandas as pd
df = pd.read_csv("preprocessed_dataset.csv")

# Function to fetch reviews based on restaurant name
def fetch_reviews(restaurant_name):
    # Filter the dataframe based on the restaurant name
    reviews = df[df['Restaurante'] == restaurant_name]['Review'].tolist()
    return reviews


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':

        restaurant_name = request.form.get('sentences123')

        reviews = fetch_reviews(restaurant_name)

        sentences_list = reviews

        # Define keyword lists
        service_keywords = ["staff", "wait", "shutdown", "delivery", "online ordering", "accommodating", "help", "greeted", "UberEats"]
        food_keywords = ["delicious", "tasty", "flavors", "tender", "options", "sauce", "menu", "drink", "fusion", "appetizers"]
        place_keywords = ["street", "station", "close", "parking", "near", "outside seating", "location", "convenience", "easy", "find"]
        experience_keywords = ["Value", "disappoint", "recommend", "accepted", "charge", "atmosphere", "clean", "amazing", "expectation", "hygiene practices"]

        # Initialize lists to store sentences based on keywords
        service_class_sentences = []
        food_class_sentences = []
        place_class_sentences = []
        experience_class_sentences = []

        # Classify sentences based on keywords
        for sentence in sentences_list:
            if any(keyword in sentence for keyword in service_keywords):
                service_class_sentences.append(sentence)
            if any(keyword in sentence for keyword in food_keywords):
                food_class_sentences.append(sentence)
            if any(keyword in sentence for keyword in place_keywords):
                place_class_sentences.append(sentence)
            if any(keyword in sentence for keyword in experience_keywords):
                experience_class_sentences.append(sentence)

        # Get ratings for each class of sentences
        service_ratings = [rating_predictor(sentence) for sentence in service_class_sentences]
        food_ratings = [rating_predictor(sentence) for sentence in food_class_sentences]
        place_ratings = [rating_predictor(sentence) for sentence in place_class_sentences]
        experience_ratings = [rating_predictor(sentence) for sentence in experience_class_sentences]

        # Calculate average rating for each class of sentences
        average_service_rating = sum(service_ratings) / len(service_ratings) if service_ratings else 0
        average_food_rating = sum(food_ratings) / len(food_ratings) if food_ratings else 0
        average_place_rating = sum(place_ratings) / len(place_ratings) if place_ratings else 0
        average_experience_rating = sum(experience_ratings) / len(experience_ratings) if experience_ratings else 0

        # Printing the average ratings
        print("Average Service Rating:", average_service_rating)
        print("Average Food Rating:", average_food_rating)
        print("Average Place Rating:", average_place_rating)
        print("Average Experience Rating:", average_experience_rating)

        #return "Average ratings calculated successfully!"

        return render_template('index.html',average_service_rating=average_service_rating,average_food_rating=average_food_rating,average_place_rating=average_place_rating,average_experience_rating=average_experience_rating)

if __name__ == '__main__':
    app.run(debug=True)
