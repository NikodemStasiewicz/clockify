import requests
import json

api_key = "MDQwOGNjZTktOTQ4MC00NDdlLTlmYmYtNWFhYzhjMzkwOTRk"
workspace_id = "64ed817b29c9f301a1529730"


report_data = {

    "dateRangeEnd": "2023-08-31T23:59:59.999Z",  # Corrected end date

    "dateRangeStart": "2023-08-01T00:00:00.000Z", 
    "summaryFilter": {
        "groups": ["USER","PROJECT"],  # Group by user
        "sortColumn": "DURATION"  # Sort by user
    },




}


headers = {
    "X-Api-Key": api_key,
    "Content-Type": "application/json"
}


url = f"https://reports.api.clockify.me/v1/workspaces/{workspace_id}/reports/summary"


response = requests.post(url, headers=headers, json=report_data)

if response.status_code == 200:
    report_result = response.json()
    print(json.dumps(report_result, indent=2))
else:
    print(f"Nie udało się wygenerować raportu. Kod statusu: {response.status_code}")
    print(response.text)  