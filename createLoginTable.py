"""
Code adapted from AWS Docs: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/programming-with-python.html
"""

import boto3

userDetails = [
    {'email': 's39592000@student.rmit.edu.au', 'password': '012345', 'user_name': 'Krishnakanth Srikanth0'},
    {'email': 's39592001@student.rmit.edu.au', 'password': '123456', 'user_name': 'Krishnakanth Srikanth1'},
    {'email': 's39592002@student.rmit.edu.au', 'password': '234567', 'user_name': 'Krishnakanth Srikanth2'},
    {'email': 's39592003@student.rmit.edu.au', 'password': '345678', 'user_name': 'Krishnakanth Srikanth3'},
    {'email': 's39592004@student.rmit.edu.au', 'password': '456789', 'user_name': 'Krishnakanth Srikanth4'},
    {'email': 's39592005@student.rmit.edu.au', 'password': '567890', 'user_name': 'Krishnakanth Srikanth5'},
    {'email': 's39592006@student.rmit.edu.au', 'password': '678901', 'user_name': 'Krishnakanth Srikanth6'},
    {'email': 's39592007@student.rmit.edu.au', 'password': '789012', 'user_name': 'Krishnakanth Srikanth7'},
    {'email': 's39592008@student.rmit.edu.au', 'password': '890123', 'user_name': 'Krishnakanth Srikanth8'},
    {'email': 's39592009@student.rmit.edu.au', 'password': '901234', 'user_name': 'Krishnakanth Srikanth9'},
]


def create_login_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.create_table(
        TableName='login',
        KeySchema=[
            {
                'AttributeName': 'email',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='login')

    # Put items into the table
    with table.batch_writer() as batch:
        for item in userDetails:
            batch.put_item(Item=item)

    return table


if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    login_table = create_login_table(dynamodb)
    print("Table status:", login_table.table_status)
