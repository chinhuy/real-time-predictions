from flask import Flask, jsonify, request, json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)


# function to print sentiments
# of the sentence.
def sentiment_scores(sentence):

	# Create a SentimentIntensityAnalyzer object.
	sid_obj = SentimentIntensityAnalyzer()

	# polarity_scores method of SentimentIntensityAnalyzer
	# object gives a sentiment dictionary.
	# which contains pos, neg, neu, and compound scores.
	sentiment_dict = sid_obj.polarity_scores(sentence)
	
	# print("Overall sentiment dictionary is : ", sentiment_dict)
	# print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
	# print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
	# print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")

	# print("Sentence Overall Rated As", end = " ")

	# decide sentiment as positive, negative and neutral
	if sentiment_dict['compound'] >= 0.05 :
		return "Positive"

	elif sentiment_dict['compound'] <= - 0.05 :
		return "Negative"

	else :
		return "Neutral"



@app.route('/', methods=['GET'])
def home():

    return jsonify({'hello': 'world'})

# curl -X POST -H "Content-Type: application/json" \
#     -d '{"name": "linuxize", "email": "linuxize@example.com"}' \
#     https://example/contact
@app.route('/sentiment', methods=['POST'])
def sentiment():
	record = json.loads(request.data)
	sentiment_result = sentiment_scores(record['review'])
	return jsonify({'sentiment_result': sentiment_result})


		
if __name__ == "__main__":
	app.run(debug=True)