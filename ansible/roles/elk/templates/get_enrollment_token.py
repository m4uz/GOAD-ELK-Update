#!/usr/bin/env python3

import requests
import os

requests.urllib3.disable_warnings()

headers = {
  'content-type': 'application/json',
  'kbn-xsrf': 'true'
}
username='elastic'
password='{{ elastic_password }}'

try:
  r = requests.get('https://127.0.0.1:5601/api/fleet/enrollment-api-keys',auth=(username, password), headers=headers, verify=False)
  if r.status_code != 200:
    exit('Failed to get enrollment keys: ' + r.text)

  enrollment_token = None
  for item in r.json()['items']:
    if item['policy_id'] != 'windows-agent-policy':
      continue
    else:
      enrollment_token = item['api_key']
      break

  if not enrollment_token:
    exit('windows-agent-policy API key not found')

  with open('enrollment_token.txt', 'w') as f:
    f.write(enrollment_token)

  print(f'Enrollment token: {enrollment_token} saved as {os.path.realpath('enrollment_token.txt')}')
except Exception as e:
  exit(e)
