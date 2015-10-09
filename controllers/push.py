import requests, json

GCM_API_KEY = 'AIzaSyBCCDYuRXS9QM_pwim7TlJN7tKqApBTCNs'
GCM_SENDER_ID = '627795041855'
GCM_URL = 'https://gcm-http.googleapis.com/gcm/send'

def send_push(to, data=None, notification=None):
    content = {}
    content['to'] = to
    if data is not None:
        content['data'] = data
    if notification is not None:
        content['notification'] = notification

    resp = requests.post(
        headers={
            'Authorization','key='+GCM_API_KEY,
            'Content-Type','application/json'},
        data = content
    )

    if resp.status_code != 200:
        raise Exception('Push failed!')

