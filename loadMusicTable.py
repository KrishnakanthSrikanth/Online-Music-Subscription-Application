"""
Code adapted from GeeksForGeeks: https://www.geeksforgeeks.org/how-to-upload-json-file-to-amazon-dynamodb-using-python/
"""

from decimal import Decimal
import json
import boto3


def loadMusicData(music, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('music')
    for item in music['songs']:
        table.put_item(Item=item)
        title = item['title']
        artist = item['artist']
        year = int(item['year'])
        web_url = item['web_url']
        img_url = item['img_url']

        print("Music table loaded successfully!!")


if __name__ == '__main__':
    with open("a1.json") as json_file:
        inputData = json.load(json_file, parse_float=Decimal)
    loadMusicData(inputData)
