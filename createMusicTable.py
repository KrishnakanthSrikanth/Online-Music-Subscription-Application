"""
Code adapted from AWS Docs: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/programming-with-python.html
"""
import boto3


def createMusicTable(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.create_table(
            TableName='music',
            KeySchema=[
                {
                    'AttributeName': 'title',
                    'KeyType': 'HASH' # Partition key
                },
                {
                    'AttributeName': 'artist',
                    'KeyType': 'RANGE' # Sort key (One title will have only one artist)
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'title',
                    'AttributeType': 'S' # String
                },
                {
                    'AttributeName': 'artist',
                    'AttributeType': 'S' # String
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        return table


if __name__ == '__main__':
    table_name = createMusicTable()
    print("Table status:", table_name.table_status)
