import requests
import json
from pathlib import Path
import time

config_file = './strava_config.json'
config_file_path = str(Path(__file__).parent / config_file)

strava_base_url = 'https://www.strava.com/api/v3/'

STRAVA_ENDPOINTS = {
    'token': 'oauth/token',
    'upload': 'uploads'
}

class Strava:
    def __init__(self):
        with open(config_file_path, 'r') as cf:
            config = json.load(cf)
        
        self.client_config = config['client']
        self.user_config = config['user']

        self.client_id = self.client_config['client_id']
        self.client_secret = self.client_config['client_secret']
        self.refresh_token = self.user_config['refresh_token']
        self.auth_token_expiry =  self.user_config['expires_at']
        if time.time() > float(self.auth_token_expiry):
            self.refresh_auth()
        
        # Set initial Auth token
        self.__auth_token = self.user_config['access_token']
    
    def refresh_auth(self):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }
        res = requests.post(strava_base_url + STRAVA_ENDPOINTS['token'], data=payload)
        if res.status_code != 200:
            raise Exception(f'Auth refresh failed:\n{res.text}')
        res_json = res.json()
        self.__auth_token = res_json['access_token']
        self.refresh_token = res_json['refresh_token']
        self.auth_token_expiry = res_json['expires_at']

        self.user_config['refresh_token'] = self.refresh_token
        self.user_config['access_token'] = self.__auth_token
        self.user_config['expires_at'] = self.auth_token_expiry
        config = { 'client': self.client_config, 'user': self.user_config }
        with open(config_file_path, 'w') as cf:
            json.dump(config, cf, indent=2)
    
    def upload_activity(self, activity_file_path: str):
        headers = {
            'Authorization': f'Bearer {self.__auth_token}'
        }
        with open(activity_file_path, 'rb') as af:
            files = [
                ('file', (activity_file_path, af, 'application/octet-stream')),
                ('name', (None, 'Ride', 'application/json')),
                ('description', (None, '', 'application/json')),
                ('trainer', (None, '', 'application/json')),
                ('commute', (None, '', 'application/json')),
                ('data_type', (None, 'fit', 'application/json')),
                ('external_id', (None, Path(activity_file_path).stem, 'application/json'))
            ]

            print(f'Uploading {activity_file_path} to Strava...')
            res = requests.post(strava_base_url + STRAVA_ENDPOINTS['upload'], headers=headers, files=files)
            if res.status_code != 200:
                raise Exception(f'Activity upload failed:\n{json.dumps(res.json(), indent=2)}')                
            print(json.dumps(res.json(), indent=2))
