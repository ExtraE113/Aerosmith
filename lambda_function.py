from datetime import datetime, timedelta
import json
import os

import pytz as pytz
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError
import dateutil.parser

import db

import requests


def lambda_handler(event, context):
	client_id = 53508
	client_secret = os.getenv("CLIENT_SECRET")

	token = {
		'access_token': 'bad',
		'refresh_token': db.get_key(),
		'token_type': 'Bearer',
		'expires_in': '20035',  # initially 3600, need to be updated by you
	}

	refresh_url = 'https://www.strava.com/api/v3/oauth/token'
	protected_url = 'https://www.strava.com/api/v3/athlete/activities'

	# most providers will ask you for extra credentials to be passed along
	# when refreshing tokens, usually for authentication purposes.
	extra = {
		'client_id': client_id,
		'client_secret': client_secret,
	}


	# After updating the token you will most likely want to save it.
	def token_saver(new_token):
		global token
		token = new_token
		db.put_key(new_token["refresh_token"])


	after = datetime.today() - timedelta(days=7)
	try:
		client = OAuth2Session(client_id, token=token)
		r = client.get(protected_url)
		json_data = json.loads(r.text)
		if json_data["message"] == "Authorization Error":
			raise TokenExpiredError
	except TokenExpiredError as e:
		print("refreshing token...")
		print("token: " + str(token))
		token = client.refresh_token(refresh_url, **extra)
		token_saver(token)
		client = OAuth2Session(client_id, token=token)
		r = client.get(protected_url)
		json_data = json.loads(r.text)

	best = dateutil.parser.parse(json_data[0]["start_date_local"])
	print(best)

	logged = db.get_logged()
	print(logged)
	for i in json_data:
		time = dateutil.parser.parse(i["start_date_local"])
		if (time > (datetime.today().replace(tzinfo=pytz.UTC) - timedelta(days=7))) and (time < best) \
				and str(i["id"]) not in logged:
			best = time
	print(best)

	same_day_and_older = []

	for i in json_data:
		time = dateutil.parser.parse(i["start_date_local"])
		if time.date() >= best.date():
			same_day_and_older.append(i)

	print(same_day_and_older)

	out = "<table border='1px solid black'> <tr> <th> type </th> <th> date </th> <th> name </th> <th> duration (min:sec) </th> <th> distance (mi) </th> <th> notes </th> </tr>"

	for i in same_day_and_older:
		if str(i["id"]) in logged:
			continue
		logged.append(i["id"])
		db.put_logged(i["id"])
		client = OAuth2Session(client_id, token=token)
		d = client.get("https://www.strava.com/api/v3/activities/" + str(i["id"]))
		data = json.loads(d.text)
		out += f"<tr> <td>{i['type']}</td> <td>{i['start_date_local']}</td> <td>{i['name']}</td> <td>{'{}:{}'.format(divmod(i['elapsed_time'], 60)[0], divmod(i['elapsed_time'], 60)[1])}</td> <td>{i['distance'] / 1609} </td> <td>{data['description']} </td> </tr>"

	out += "</table>"
	headers = {'Authorization': f'Bearer {os.getenv("CANVAS_TOKEN")}'}
	assignments = [99935, 99936, 99937, 99938, 99939, 99940, 99933, 99943, 99942, 99941]
	assign_index = int(db.get_index())
	db.put_index(str(assign_index+1))
	canvas = requests.post(f"https://athenian.instructure.com/api/v1/courses/4074/assignments/{assignments[assign_index]}/submissions?submission[submission_type]=online_text_entry&submission[body]={out}", headers=headers)
	print(canvas)
