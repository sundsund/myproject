import requests

def get_access_token():
    response = requests.post('http://localhost:8081/token')
    return response.json()['access_token']

if __name__ == '__main__':
    token = get_access_token()
    print(f"Access Token: {token}")
