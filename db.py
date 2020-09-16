import uuid
from pprint import pprint
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


def put_key(key: str, dynamodb=None):
	if not dynamodb:
		dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

	table = dynamodb.Table('Strava')
	response = table.put_item(
		Item={
			'Type': "refreshKey",
			'Key': key
		}
	)
	return response


def get_key(dynamodb=None):
	if not dynamodb:
		dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

	table = dynamodb.Table('Strava')

	try:
		response = table.get_item(Key={'Type': 'refreshKey'})
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		return response['Item']['Key']


def put_index(index: str, dynamodb=None):
	if not dynamodb:
		dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

	table = dynamodb.Table('Strava')
	response = table.put_item(
		Item={
			'Type': "index",
			'index': index
		}
	)
	return response


def get_index(dynamodb=None):
	if not dynamodb:
		dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

	table = dynamodb.Table('Strava')

	try:
		response = table.get_item(Key={'Type': 'index'})
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		return response['Item']['index']


def put_logged(val: int, dynamodb=None):
	if not dynamodb:
		dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

	table = dynamodb.Table('Strava')
	response = table.put_item(
		Item={
			'Type': f"logged_ids{uuid.uuid4()}",
			'strava_id': val
		}
	)
	return response


def get_logged(dynamodb=None):
	if not dynamodb:
		dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

	table = dynamodb.Table('Strava')
	scan_kwargs = {
		'FilterExpression': Key('Type').begins_with("logged_ids"),
		'ProjectionExpression': "#sid",
		'ExpressionAttributeNames': {"#sid": "strava_id"}
	}

	out = []

	done = False
	start_key = None
	while not done:
		if start_key:
			scan_kwargs['ExclusiveStartKey'] = start_key
		response = table.scan(**scan_kwargs)
		out.append(response.get('Items', []))
		start_key = response.get('LastEvaluatedKey', None)
		done = start_key is None

	rout = []
	for i in out:
		for j in i:
			rout.append(str(j["strava_id"]))

	return rout


if __name__ == '__main__':
	# movie_resp = put_key("cad99b357d6d4955d0c7bf937b759a5a6180e794")
	# print("Put movie succeeded:")
	# pprint(movie_resp)

	update_response = put_index("0")
	print("Update logged succeeded:")
	pprint(update_response)
	# key = get_key()
	# if key:
	# 	print("Get movie succeeded:")
	# 	pprint(key)
	# pprint(get_logged())
