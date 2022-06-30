import time
import os
from utils import scale, get_metric

SCALE_TARGET = os.environ['SCALE_TARGET']

while True:
    print(time.ctime(), end=" : ")
    
    total_cpu_usage = get_metric(SCALE_TARGET)
    print(total_cpu_usage, end=", scaled to ")
    
    # 모델에 데이터를 보내 replicas 를 받아옴

    replicas = int(time.ctime().split(':')[-1][0]) % 3 + 1
    scale(SCALE_TARGET, replicas)
    print(replicas)

    time.sleep(10)
