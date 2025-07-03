import pandas as pd
import os
import dataframeloader as dfl
from datetime import datetime, timedelta
import sys

root = sys.argv[1]
appliance_id = sys.argv[2]
if len(sys.argv) == 5:
    fromDt = sys.argv[3]
    toDt = sys.argv[4]   
elif len(sys.argv) == 4:
    fromDt = datetime.strftime(datetime.now() - timedelta(days=int(sys.argv[3])), '%Y-%m-%d')
    toDt = datetime.strftime(datetime.now(), '%Y-%m-%d')
else:
    print("Usage: python sys.argv[0] <rootDir> <appliance_id> <fromDt> <toDt>")
    sys.exit(1) 
metricsArr = ['cpu_used','task_queue_length', 'memory_used']
try:
    li = []
    for filenm in os.listdir(root):
        tmp_df = pd.read_csv(f'{root}/{filenm}')
        li.append(tmp_df)
    pod_df = pd.concat(li, axis=0, ignore_index=True)
    if pod_df.empty:
        print(f'No data found for pod: {appliance_id}')
        sys.exit(1)
    pod_df['ts'] = pd.to_datetime(pod_df['ts'])
    fig  = dfl.plotMetricsFacetForApplianceId(pod_df, appliance_id).show()
except Exception as e:
    print(f"CSV Data not found")
    sys.exit(1)


