import requests
from github import Github

repos_str = 'jamf/jamf-data-quality-service, jamf/jamf-user-and-access-service, jamf/order-fulfillment-process, jamf/order-fulfillment-event-bridge-resources, \
jamf/customer-instance-update-process, jamf/digitalcommerce-order-management-task-service, jamf/intacct-finance-utility-service, jamf/jamfproduct-customer-asset-and-license-task-service, \
jamf/jamfproduct-customer-management-task-service, jamf/jamfprotect-management-task-service, jamf/jamfprotect-management-utility-service, jamf/radar-management-utility-service, \
jamf/radar-management-utility-service, jamf/rainfocus-conference-task-service, jamf/rainfocus-conference-utility-service, jamf/salesforce-asset-utility-service, jamf/salesforce-common-utility-service, \
jamf/salesforce-customer-account-utility-service, jamf/salesforce-event-task-service, jamf/salesforce-event-utility-service, jamf/salesforce-order-utility-service, jamf/salesforce-ticketing-utility-service, \
jamf/sendgrid-notification-utility-service, jamf/servicenow-ticketing-task-service, jamf/salesforce-limits-to-newrelic-integration, jamf/finance-account-sync-integration, jamf/finance-order-sync-integration, \
jamf/find-intacct-finance-updates-integration, jamf/find-salesforce-finance-updates-integration, jamf/intacct-event-catcher-integration, jamf/rsql-bizops-utility, jamf/salesforce-initialize-axios, jamf/intacct-initialize-axios, \
jamf/awslambda-bizops-misc-utility, jamf/bizops-eai-api-gateway-resources'

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





