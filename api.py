import requests

api_key = 'YzMzZDFhMzItN2E0OS00NTEwLTgzMTAtNGE4ZGVkNzE3NTFi'
headers = {
    'x-api-key': api_key
}

workspace_id = '64ed817b29c9f301a1529730'
url = f'https://api.clockify.me/api/v1/workspaces/{workspace_id}'
response = requests.get(url, headers=headers)

if response.status_code == 200:
    workspace_info = response.json()
    print("Nazwa workspace:", workspace_info['name'])
    print("ID workspace:", workspace_info['id'])
    # Dodaj tutaj kod do pobrania innych informacji o workspace
else:
    print('Nie udało się połączyć ze stroną API Clockify')

