"""
Code adapted from AWS Docs: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/programming-with-python.html
"""

import boto3


def create_subs_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.create_table(
        TableName='subscription',
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
    table.meta.client.get_waiter('table_exists').wait(TableName='subscription')
    return table


if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    subs_table = create_subs_table(dynamodb)
    print("Table status:", subs_table.table_status)
