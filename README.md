# boto3-sso-credz
This script is a Python Flask route handler that handles a POST request to the '/aws_credentials' endpoint. When the endpoint is called, it does the following:

1. It extracts the token from the request headers and the sender email from the request body.
2. It validates the sender email by checking that it matches the email address format.
3. It verifies the token with Auth0 using the 'get_token.authorize_token(token, AUDIENCE)' method, which returns the token's claims such as the user's email .
4. It gets the user's app_metadata from Auth0 using the Auth0 class.
5. It provisions an IAM user using the user's id as the username.
6. It adds the IAM user to a specified IAM group.
7. It assumes a role and retrieves temporary credentials using the boto3 sts client.
8. It generates a new ssh key pair and saves the private key to a .pem file.
9. It reads the private key from the .pem file and sends it as an attachment to the user's email address.
