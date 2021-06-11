from typing_extensions import ParamSpec
import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
	print(kwargs)
	print('GET from {} '.format(url))
	try:
		response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
	except:
		print('Network exception occured')

	status_code = response.status_code
	print('With status {} '.format(status_code))
	json_data = json.loads(response.text)
	return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
	print(kwargs)
	print('POST from {} '.format(url))
	try:
		if 'api_key' in kwargs.keys():
			api_key = kwargs["api_key"]
			del(kwargs["api_key"])
			response = requests.post(
				url,
				headers={'Content-Type': 'application/json'},
				auth=HTTPBasicAuth('apikey', api_key),
				params=kwargs,
				json=json_payload
			)
		else:
			response = requests.post(
				url,
				headers={'Content-Type': 'application/json'},
				params=kwargs,
				json=json_payload
			)
	except:
		print('Network exception occured')

	status_code = response.status_code
	print('With status {} '.format(status_code))
	json_data = json.loads(response.text)
	return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
	results = []
	json_result = get_request(url)
	if json_result:
		dealers = json_result["rows"]
		for dealer in dealers:
			dealer_doc = dealer["doc"]
			dealer_obj = CarDealer(
				address=dealer_doc["address"],
				city=dealer_doc["city"],
				full_name=dealer_doc["full_name"],
				id=dealer_doc["id"],
				lat=dealer_doc["id"],
				long=dealer_doc["long"],
				short_name=dealer_doc["short_name"],
				st=dealer_doc["st"],
				zip=dealer_doc["zip"]
			)
			results.append(dealer_obj)
	return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id, **kwargs):
	results = []
	json_result = get_request(url, dealerId=dealer_id)
	if json_result:
		reviews = json_result["rows"]
		for review in reviews:
			review_doc = review["doc"]
			sentiment = analyze_review_sentiments(text=review_doc["review"])
			review_obj = DealerReview(
				id=review_doc["id"],
				name=review_doc["name"],
				dealership=review_doc["dealership"],
				review=review_doc["review"],
				purchase=review_doc["purchase"],
				purchase_date=review_doc["purchase_date"],
				car_make=review_doc["car_make"],
				car_model=review_doc["car_model"],
				car_year=review_doc["car_year"],
				sentiment=sentiment
			)
			results.append(review_obj)
	return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review, **kwargs):
	url = ''
	api_key = ''
	params = dict()
	params["text"] = kwargs["text"]
	params["version"] = kwargs["version"]
	params["features"] = 'sentiment'
	params["return_analyzed_text"] = False
	response = get_request(
		url,
		params=params,
		headers={'Context-Type': 'application/json'},
		auth=HTTPBasicAuth('apikey', api_key)
	)
	return response["sentiment"]["document"]["label"]



