from flask import Flask, render_template, request, jsonify
import boto3

app = Flask(__name__, template_folder='template')

# Connections to AWS DynamoDB and S3
session = boto3.Session(
    aws_access_key_id="ASIA4MTWKW2QJ24N77QM",
    aws_secret_access_key="anJLTajhJu+84R7qauBpiZm2HEW6bykEDxvmdTdy",
    aws_session_token="IQoJb3JpZ2luX2VjECQaCXVzLXdlc3QtMiJIMEYCIQCzv8HkMF5NLRWo6tsiCMxkmhDQS9OutOXsldSNTy0U/wIhAKW47XS6+z1+BBUguJG4sWNLWrdI0hSvgdXH9sc826NpKrYCCF0QABoMODUxNzI1NDMyNDgwIgxxGU8K7uwnMma5xqEqkwLR5/NuaEWxMS05XGTsObjJkmiK1M1dstpK00cWLFt7vPQNAW5p6qtakfKaij8S+QHBhwesZaDmgcIMW7aTCyWivIvTuT7s8cQFwAtqJb57AHuVJIZPqqcRD1C6931kv6vVXc6X76lCD9WIN3JaEIP4HDr4uOSXy45nE+sC6rkkGzlkgAF+NT188oeze44VNiKI1Eglj+9zKO6sGRSONHL+DXGNKJvRHccoGlZJuzXCVZj4J5pmSJ3Pm+++u8IFUYNUdH9ER8Aki0yCHCVbx2pjJfB+fhklwZdu/d6tSCdc3bxDE30Wzgc/4xDzCeXsRq++WDoaTZaQlNGRdXUkiqjQUzGydrN83hwroKKsdYla4O8RGTDLv+SwBjqcARRn3+nliaF2gZggqzQQotUKsiO3bNuqwSj4PKMFRu1STZMgX1F6UBciA1VuP9xgalaiwcypBv3j9ODm8kh+9O/DXo199JGGEIkqa/rb2lA5hei66ZUPLo7AmrCYLwSJUoqhBykHIJZYJoL8JNpPXhX6Ld4tZ1WAA+0eTUSxG/wHa47UmnfLsaXr1rr5n2caF1GawcBhN2VG0HLoDw=="
)

dynamodb = session.resource('dynamodb', region_name='us-east-1')
music_table = dynamodb.Table('music')
subscription_table = dynamodb.Table('subscription')
s3 = session.resource('s3', region_name='us-east-1')


@app.route('/')
def index():
    return render_template('index.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    # Connecting to 'login' table
    login_table = dynamodb.Table('login')

    # Getting values from login page
    email = request.form['email']
    pwd = request.form['password']

    # Retrieving user details from database and Checking if the credentials are valid
    response = login_table.get_item(Key={"email": email})

    if 'Item' in response:
        orig_email = response['Item']['email']
        password = response['Item']['password']

        # Checking if the credentials are valid
        if orig_email == email and password == pwd:
            return render_template('mainpage.html', username=response['Item']['user_name'],
                                   email=response['Item']['email'])
        else:
            # If credentials are invalid, display error message
            error_msg = 'email or password is invalid'
            return render_template('index.html', error=error_msg)
    else:
        # If credentials are invalid, display error message
        error_msg = 'email or password is invalid'
        return render_template('index.html', error=error_msg)


# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('registration.html')


# Check for user registration
@app.route('/register_check', methods=['GET', 'POST'])
def register_check():
    if request.method == 'POST':
        email = request.form['email']

        # Check if the email already exists in the login table
        login_table = dynamodb.Table('login')
        response = login_table.get_item(Key={'email': email})

        item = response.get('Item')
        if item:
            # Email already exists, return error message
            error_msg = "The email already exists"
            return render_template('registration.html', error=error_msg)
        else:
            # Email is unique, proceed with registration
            password = request.form['password']
            username = request.form['name']
            login_table.put_item(
                Item={
                    'email': email,
                    'password': password,
                    'user_name': username
                }
            )
            # Registration complete, redirect to index or success page
            return render_template('index.html')
    # Render the registration form
    return render_template('index.html')


# Mainpage
@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    return render_template('mainpage.html')


# Function to fetch artist image URL from S3
def get_s3_image_url(img_key):
    return f"https://s3959200-bucket.s3.amazonaws.com/{img_key}"


# Route for retrieving subscriptions
@app.route('/get-subscriptions', methods=['POST'])
def get_subscriptions():
    email = request.form.get('email')

    # Check if there are subscription entries for the user's email
    response = subscription_table.get_item(Key={'email': email})
    if 'Item' in response:
        subscriptions = response['Item']['items']
        return jsonify(subscriptions)
    else:
        # If no subscription entries found, return empty list
        return jsonify([])


# Route for querying music
@app.route('/query', methods=['POST'])
def query_music():
    # Placeholder for querying music
    query_title = request.form.get('title')
    query_year = request.form.get('year')
    query_artist = request.form.get('artist')

    # Placeholder logic for querying
    response = music_table.scan()
    subscription_data = response['Items']

    if query_title:
        subscription_data = [item for item in subscription_data if item.get('title', '').lower() == query_title.lower()]
    if query_year:
        subscription_data = [item for item in subscription_data if item.get('year', '') == query_year]
    if query_artist:
        subscription_data = [item for item in subscription_data if item.get('artist', '').lower() == query_artist.lower()]

    # Add S3 image URLs to each item
    for item in subscription_data:
        item['image_url'] = get_s3_image_url(item['img_url'])

    return jsonify(subscription_data)


# Route for adding subscription
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    title = request.form.get('title')
    artist = request.form.get('artist')
    year = request.form.get('year')
    img_url = request.form.get('img_url')

    # Add subscription to DynamoDB
    subscription_table.update_item(
        Key={'email': email},
        UpdateExpression='SET #items = list_append(if_not_exists(#items, :empty_list), :item)',
        ExpressionAttributeNames={'#items': 'items'},
        ExpressionAttributeValues={':empty_list': [], ':item': [{'title': title, 'artist': artist, 'year': year, 'img_url': img_url}]},
        ReturnValues='UPDATED_NEW'
    )

    return jsonify({'success': True})


# Route for removing subscription
@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    email = request.form.get('email')
    title = request.form.get('title')

    # Get current subscriptions
    response = subscription_table.get_item(Key={'email': email})
    if 'Item' not in response:
        return jsonify({'success': False, 'message': 'No subscriptions found for the user'})

    subscriptions = response['Item'].get('items', [])
    # Find the index of the item with the specified title
    index_to_remove = None
    for i, item in enumerate(subscriptions):
        if item.get('title') == title:
            index_to_remove = i
            break

    if index_to_remove is None:
        return jsonify({'success': False, 'message': 'Subscription not found for the specified title'})

    # Remove the item from the list
    subscriptions.pop(index_to_remove)

    # Update DynamoDB with the modified subscriptions list
    subscription_table.update_item(
        Key={'email': email},
        UpdateExpression='SET #items = :new_items',
        ExpressionAttributeNames={'#items': 'items'},
        ExpressionAttributeValues={':new_items': subscriptions}
    )

    return jsonify({'success': True})


# Application main function
if __name__ == '__main__':
    app.run(debug=True)
