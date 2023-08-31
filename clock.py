import requests
import json
from openpyxl import Workbook
from datetime import datetime, timedelta

api_key = "MDQwOGNjZTktOTQ4MC00NDdlLTlmYmYtNWFhYzhjMzkwOTRk"
workspace_id = "64ed817b29c9f301a1529730"


today = datetime.today()
first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1, microsecond=0) - timedelta(microseconds=1)


month_year = first_day_of_month.strftime("%B_%Y")
excel_filename = f"summary_report_{month_year}.xlsx"

report_data = {
    "dateRangeStart": first_day_of_month.isoformat(),
    "dateRangeEnd": last_day_of_month.isoformat(),
    "summaryFilter": {
        "groups": ["USER", "PROJECT"],
        "sortColumn": "DURATION"
    }
}

headers = {
    "X-Api-Key": api_key,
    "Content-Type": "application/json"
}

url = f"https://reports.api.clockify.me/v1/workspaces/{workspace_id}/reports/summary"

response = requests.post(url, headers=headers, json=report_data)

if response.status_code == 200:
    report_result = response.json()

    wb = Workbook()
    ws = wb.active
    ws.title = "Summary Report"
 
    project_names = set()
    for group in report_result.get("groupOne", []):
        for project in group.get("children", []):
            project_name = project["name"]
            project_names.add(project_name)
    project_names = sorted(list(project_names))
   
    ws.append(["User"] + project_names + ["Total Hours"])

    for group in report_result.get("groupOne", []):
        user_name = group["name"]
        user_data = {project["name"]: project["duration"] / 3600 for project in group.get("children", [])}
        total_hours = sum(user_data.values())
        row_data = []
        for project_name in project_names:
            hours = user_data.get(project_name, 0)
            rounded_hours = round(hours * 4) / 4
            row_data.append(rounded_hours)
        row_data.append(round(total_hours * 4) / 4)
        ws.append([user_name] + row_data)
       
    wb.save(excel_filename)
    print(f"Wyniki zostały zapisane do pliku {excel_filename}")
else:
    print(f"Nie udało się wygenerować raportu. Kod statusu: {response.status_code}")
    print(response.text)
