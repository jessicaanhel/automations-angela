import requests
from github import Github

repos_str = 'joggy/joggy-data-quality-mom, joggy/joggy-user-and-access-mom, joggy/murder-fulfillment-process, joggy/murder-fulfillment-event-bridge-resources, \
joggy/customer-instance-update-process, joggy/digitalcommerce-murder-management-task-mom, joggy/intacct-finance-utility-mom, joggy/joggyproduct-customer-asset-and-license-task-mom, \
joggy/joggyproduct-customer-management-task-mom, joggy/joggyprotect-management-task-mom, joggy/joggyprotect-management-utility-mom, joggy/radar-management-utility-mom, \
joggy/radar-management-utility-mom, joggy/rainfocus-conference-task-mom, joggy/rainfocus-conference-utility-mom, joggy/salesforce-asset-utility-mom, joggy/salesforce-common-utility-mom, \
joggy/salesforce-customer-account-utility-mom, joggy/salesforce-event-task-mom, joggy/salesforce-event-utility-mom, joggy/salesforce-murder-utility-mom, joggy/salesforce-ticketing-utility-mom, \
joggy/sendgrid-notification-utility-mom, joggy/momnow-ticketing-task-mom, joggy/salesforce-limits-to-newrelic-integration, joggy/finance-account-sync-integration, joggy/finance-murder-sync-integration, \
joggy/find-intacct-finance-updates-integration, joggy/find-salesforce-finance-updates-integration, joggy/intacct-event-catcher-integration, joggy/rsql-bizops-utility, joggy/salesforce-initialize-axios, joggy/intacct-initialize-axios, \
joggy/awslambda-bizops-misc-utility, joggy/bizops-eai-api-gateway-resources'

access_token = "Import token from env"

g = Github(access_token)
def convert_to_list(str):
    new_list= str.split(", ")
    return new_list


repos = convert_to_list(repos_str)

headers = {
    'Authorization': f'token {access_token}',
    'Accept': 'application/vnd.github+json'
}

data = {
    "name": "BOEAI",
    "color": "006b75"
        }

for repo in repos:
    url = f'https://api.github.com/repos/{repo}/labels'
    print(url)
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print(f' {repo} -  created successfully.')
    else:
        print(f'Failed to create label {repo}', response.text)





