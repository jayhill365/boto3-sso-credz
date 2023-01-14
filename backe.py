import re
from flask import request, jsonify
from Auth0 import Auth0
from get_token import authorize_token
from boto3 import client as boto3_client

AUTH0_DOMAIN = 'YOUR_AUTH0_DOMAIN'
AUTH0_CLIENT_ID = 'YOUR_AUTH0_CLIENT_ID'
AUTH0_CLIENT_SECRET = 'YOUR_AUTH0_CLIENT_SECRET'
AUDIENCE = 'YOUR_AUDIENCE'
IAM_GROUP_NAME = 'YOUR_IAM_GROUP_NAME'
ROLE_ARN = 'YOUR_ROLE_ARN'

app = Flask(__name__)

iam_client = boto3_client('iam')
sts_client = boto3_client('sts')
ec2_client = boto3_client('ec2')
ses_client = boto3_client('ses')

@app.route('/aws_credentials', methods=['POST'])
def get_aws_credentials():
    # Get the token from the request
    token = request.headers.get('Authorization').split()[1]
    # Get the sender email from the request
    sender_email = request.json.get('sender_email')
    # verify the sender_email is a valid email address
    if not re.match(r"[^@]+@[^@]+\.[^@]+", sender_email):
        return jsonify(error='Invalid email address'), 400
    # Verify the token with Auth0
    id_token = authorize_token(token, AUDIENCE)
    user_id = id_token['sub']
    email = id_token['email']

    # Get the user's app_metadata from Auth0
    auth0 = Auth0(AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET)
    user = auth0.users.get(user_id)
    app_metadata = user['app_metadata']

    # Provision an IAM user
    iam_username = user_id
    iam_client.create_user
    
 # Add the user to the specified IAM group
    iam_client.add_user_to_group(GroupName=IAM_GROUP_NAME, UserName=iam_username)

    # Assume a role and get temporary credentials
    temp_credentials = sts_client.assume_role(
        RoleArn=ROLE_ARN,
        RoleSessionName=user_id
    )
    # Generate a new ssh key pair
    key_pair = ec2_client.create_key_pair(KeyName=user_id)
    private_key = key_pair['KeyMaterial']

    # Save the private key to a .pem file
    with open(user_id + '.pem', 'w') as key_file:
        key_file.write(private_key)
    
        # Send the .pem file to the user's email
    with open(user_id + '.pem', 'rb') as data:
        ses_client.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': [email]
            },
            Message={
                'Subject': {'Data': 'AWS Key Pair'},
                'Body': {
                    'Text': {'Data': 'Please find your AWS key pair attached.'},
                    'Attachment': {
                        'Filename': 'key_pair.pem',
                        'Content': data.read().encode('base64'),
                        'ContentType': 'application/x-pem-file',
                    }
                }
            }
        )
    return 'The key pair has been sent to the specified email address.'
