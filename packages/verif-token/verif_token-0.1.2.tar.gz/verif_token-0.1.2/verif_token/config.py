import os

KEYCLOAK_URL = os.environ['KEYCLOAK_URL']
API_NAME = None

def configure(api_name):
    global API_NAME
    API_NAME = api_name
