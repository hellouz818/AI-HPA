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
    print(time.ctime(), end=" : ") 
    pods = json.loads(requests.get(APISERVER + f"/apis/metrics.k8s.io/v1beta1/namespaces/{NS}/pods", verify=SVCACC+"/ca.crt", headers=headers).text)
    
    total_cpu_usage = 0
    if 'items' in pods.keys():
        for pod in pods['items']:
            if SCALE_TARGET in pod['metadata']['name']:
                cur_usage = pod['containers'][0]['usage']['cpu']
                if cur_usage[-1] == 'n':
                    cur_usage = cur_usage[:-1]
                total_cpu_usage += int(cur_usage)
    print(total_cpu_usage)
    time.sleep(10)
