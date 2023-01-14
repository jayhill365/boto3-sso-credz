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

# Dependencies
    Flask
    Boto3
    Auth0
    Email service (for example SES)
    
  # Configuration
  
  The following placeholders need to be replaced with your own values:
   AUTH0_DOMAIN - Your Auth0 domain.  AUDIENCE - The audience for your Auth0 API.  AUTH0_CLIENT_ID - Your Auth0 API client ID.  AUTH0_CLIENT_SECRET - Your Auth0 API client secret.  ROLE_ARN - The ARN of the role that you want to assume.  IAM_GROUP_NAME - The name of the IAM group that the user should be added to.
  
  # Running the script
 1. Install the necessary dependencies by running pip install -r requirements.txt.
 2. Replace the placeholder values with your own Auth0 and AWS configuration information.
 3. Run the script using the command flask run.
 4. Make a POST request to the endpoint with a valid token and the user's email in the request body.


    
