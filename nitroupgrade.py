import requests
import json

# from decouple import config

credentials = json.dumps({
    "login":
        {
            "username": "nsroot",
            "password": "nsroot"
        }
})


class nitro:
    def __init__(self, host, cred):
        self.host = host
        self.cred = cred  # instance variable

    def login(self):
        """Login function"""
        try:
            baseurl = "http://{}/nitro/v1/config/login".format(self.host)
            '''creating the URL to the API endpoint'''
            headers = {'Content-Type': 'application/json'}
            '''headers to append to the request'''
            response = requests.post(baseurl, data=self.cred, headers=headers)
            '''HTTP POST request'''
            token = response.json()['sessionid']
            return token
        except Exception as inst:
            print(inst)

    def getvs(self):
        '''function to retrieve all Virtual Servers on the ADC'''
        try:
            baseurl = "http://{}/nitro/v1/stat/lbvserver".format(self.host)
            '''creating the URL to the API endpoint'''
            headers = {'Cookie': 'NITRO_AUTH_TOKEN={}'.format(nitro.login(self))}
            '''headers to append to the request'''
            response = requests.get(baseurl, headers=headers)
            '''HTTP GET request'''
            print(response.status_code)
            data = response.json()
            virtual_servers = data['lbvserver']
            print(virtual_servers)
        except Exception as inst:
            print(inst)

    def install(self):
        try:
            print('Initiating connection to ADC {} .................'.format(self.host))
            baseurl = "http://{}/nitro/v1/config/install".format(self.host)
            headers = {'Cookie': 'NITRO_AUTH_TOKEN={}'.format(nitro.login(self)), "Content-Type": "application/json"}
            data = json.dumps({"install": {"url": "file:///var/nsinstall/NSVPX-KVM-13.0-79.64_nc_64.tgz"}, })
            response = requests.post(baseurl, headers=headers, data=data)
            print('Successfully connected to ADC {} .'.format(self.host))
            print('Staring install operations on ADC {} .................'.format(self.host))
            print(response.status_code)
            print(response.json())
            if response.status_code == 201:
                print("Operation Successful!!!")
            else:
                print("We encountered errors while performing upgrades on {}".format(self.host))
        except Exception as inst:
            print("We encountered errors while connecting to {}".format(self.host))
            print(inst)


ns_session = nitro('172.20.10.10', cred=credentials)
ns_session.install()
