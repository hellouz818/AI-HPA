import requests
import time
import json
import os

SCALE_TARGET = os.environ['SCALE_TARGET']

APISERVER = "https://kubernetes.default.svc"
SVCACC = "/var/run/secrets/kubernetes.io/serviceaccount"
NS = open(SVCACC + "/namespace").readline()
TOKEN = open(SVCACC + "/token").readline()
headers = {"Authorization": "Bearer " + TOKEN}

while True:
    print('---------------------------------------------------------------------------------------------------------------')
    print(time.ctime()) 
    pods = json.loads(requests.get(APISERVER + f"/apis/metrics.k8s.io/v1beta1/namespaces/{NS}/pods", verify=SVCACC+"/ca.crt", headers=headers).text)
    if 'items' in pods.keys():
        for pod in pods['items']:
            if SCALE_TARGET in pod['metadata']['name']:
                print(f"{pod['timestamp']}\tname: {pod['metadata']['name']}\tcontainers: {len(pod['containers'])}\tusage: {pod['containers'][0]['usage']}")
    print('---------------------------------------------------------------------------------------------------------------')
    time.sleep(10)
