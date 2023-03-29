# Define Variable

import requests, json, base64

import time, datetime



#Global Variables to be used

organizations_ids = []

dictionary_of_organitations = {}

report_of_devices = {}

report_of_organizations = []

org_lastupdates = {}

devices_ages_and_companies = []

report_of_outdates_devices = []

#Functions Block

#functions for connecting to Ninja Organizations


def connect_to_orgs():
    token_url = ""
    test_api_url = ""
    #client (application) credentials
    client_id = ''
    client_secret = ''
    #call with client credentials - will return access_token
    data = {'grant_type': 'client_credentials', 'redirect_uri': 'https://localhost', 'scope': 'monitoring'}
    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    tokens = json.loads(access_token_response.text)
    #endpoint calls with the returned access_token
    api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
    api_call_response = requests.request("GET", test_api_url, headers=api_call_headers, verify=False).json()
    numberoforgs = len(api_call_response)
    for x in range(numberoforgs):
        dictionary_of_organitations = {"company_name" : api_call_response[x]["name"], "company_id" : api_call_response[x]["id"]}
        organizations_ids.append(dictionary_of_organitations)



#Function for Getting amount of devices per organizations on Ninja RMM
def get_devices_from_orgs(a):
    token_url = ""
    test_api_url = "Link or Url APi" + str(a) + "/devices"
    #client (application) credentials
    client_id = ''
    client_secret = ''
    #call with client credentials - will return access_token
    data = {'grant_type': 'client_credentials', 'redirect_uri': 'https://localhost', 'scope': 'monitoring'}
    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    tokens = json.loads(access_token_response.text)
    #endpoint calls with the returned access_token
    api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
    api_call_response = requests.request("GET", test_api_url, headers=api_call_headers, verify=False).json()
    #counting variables for function
    workstation_count = 0
    cloud_monitor_count = 0
    server_count = 0
    vmhos_count = 0
    vmguest_count = 0
    numberoforgs = len(api_call_response)
    for h in range(numberoforgs):

        if api_call_response[h]["nodeClass"] == "WINDOWS_WORKSTATION":

            workstation_count = workstation_count + 1

        if api_call_response[h]["nodeClass"] == "MAC":

            workstation_count = workstation_count + 1

        if api_call_response[h]["nodeClass"] == "WINDOWS_SERVER":

            server_count = server_count + 1

        if api_call_response[h]["nodeClass"] == "CLOUD_MONITOR_TARGET":

            cloud_monitor_count = cloud_monitor_count + 1

        if api_call_response[h]["nodeClass"] == "VMWARE_VM_HOST":

            vmhos_count = vmhos_count + 1

        if api_call_response[h]["nodeClass"] == "VMWARE_VM_GUEST":

            vmguest_count = vmguest_count + 1
    report_of_devices = {"company_name" : organizations_ids[x]["company_name"], "Number of Servers" : server_count,  "Number of Workstations" : workstation_count, "Number of Clouds" : cloud_monitor_count,  "Number of VM Hots" : vmhos_count, "Number of VM Guests" : vmguest_count}

    report_of_organizations.append(report_of_devices)

def age_of_devices_per_org(x):

    token_url = ""
    test_api_url = "Link URL for API" + str(x) + "/devices"
    #client (application) credentials
    client_id = ''
    client_secret = ''
    #call with client credentials - will return access_token
    data = {'grant_type': 'client_credentials', 'redirect_uri': 'https://localhost', 'scope': 'monitoring'}
    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    tokens = json.loads(access_token_response.text)
    #endpoint calls with the returned access_token
    api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
    api_call_response = requests.request("GET", test_api_url, headers=api_call_headers, verify=False).json()
    number_of_devices = len(api_call_response)
    
    for h in range(number_of_devices):
        if api_call_response[h]['nodeClass'] == 'WINDOWS_WORKSTATION':
            if api_call_response[h]['lastUpdate'] == None:
                print("Device", api_call_response[h]['systemName'],'was incorrectly created')
            else:
                time1 = datetime.datetime.fromtimestamp(api_call_response[h]['lastUpdate'])
                time2 = datetime.datetime.today()
                time3 = time2 - time1
                days = int(time3.days)
                if days >= 90:
                    org_lastupdates = {'Company' : api_call_response[h]['organizationId'], 'device_name' : api_call_response[h]['systemName']}
                    devices_ages_and_companies.append(org_lastupdates)
        if api_call_response[h]['nodeClass'] == 'MAC':
            if api_call_response[h]['lastUpdate'] == None:
                print("Device", api_call_response[h]['systemName'],'was incorrectly created')
            else:
                time1 = datetime.datetime.fromtimestamp(api_call_response[h]['lastUpdate'])
                time2 = datetime.datetime.today()
                time3 = time2 - time1
                days = int(time3.days)
                if days >= 90:
                    org_lastupdates = {'Company' : api_call_response[h]['organizationId'], 'device_name' : api_call_response[h]['systemName']}
                    devices_ages_and_companies.append(org_lastupdates)

#API and Functions Block
def connect_to_API():
    apiKey = ""
    loginString = apiKey + ":"
    encodedBytes = base64.b64encode(loginString.encode())
    encodedUserPassSequence = str(encodedBytes,'utf-8')
    authorizationHeader = "Basic " + encodedUserPassSequence
    apiEndpoint_Url = ""
    request = '{"params": {},"jsonrpc": "2.0","method": "getEndpointsList","id": "301f7b05-ec02-481b-9ed6-c07b97de2b7b"}'
    result = requests.post(apiEndpoint_Url,data=request,verify=False,headers= {"Content-Type":"application/json","Authorization":authorizationHeader})
    print(result.json())

#Organizations Count Block

connect_to_orgs()
totalorgs = len(organizations_ids)

for x in range(totalorgs):
    get_devices_from_orgs(organizations_ids[x]["company_id"])

for y in range(totalorgs):
    age_of_devices_per_org(organizations_ids[y]['company_id']) 
#Data OutPut

for t in range(totalorgs):
    print("Company name", report_of_organizations[t]['company_name'])
    print(report_of_organizations[t]['Number of Servers'],'Servers,',report_of_organizations[t]['Number of Workstations'],'Workstations,',report_of_organizations[t]['Number of Clouds'],'Clouds,',report_of_organizations[t]['Number of VM Hots'],'VM Hosts,',report_of_organizations[t]['Number of VM Guests'],'VM Guests')
