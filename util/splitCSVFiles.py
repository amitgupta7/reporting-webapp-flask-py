#create a cli main method that takes two folder names
import sys
import cxcsvtopandas.dataframeloader as dfl
import os

def splitDataFromcsv(src_root, dest_root, date):
    metricsArr = ['cpu_used', 'memory_used','task_queue_length']
    df = dfl.loadApplianceTimeSeriesData(src_root, metricsArr, [date, date])
    if df.empty:
        print(f'No data found for {date}')
    else:
        for appliance in df['appliance_id'].unique():
            appliance_df = df[df['appliance_id'] == appliance]
            if not os.path.exists(f'{dest_root}/{appliance}'):
                os.makedirs(f'{dest_root}/{appliance}')
            appliance_df.to_csv(f'{dest_root}/{appliance}/{date}.csv', index=False)

def extractDates(src_root):
    source = set()
    for path, subdirs, files in os.walk(src_root):
        for name in files:
        #extract Date from the filename ABC-YYYY-MM-DD.csv
            if name.endswith('.csv'):
                parts = name.split('-')
                if len(parts) >= 3:
                    date_part = "-".join(parts[-3:]).split('.')[0]
                    source.add(date_part)
    return source



def extractApplianceTenantdb(src_root):
    df = dfl.loadDataFrameFromFileRegex(src_root, 'SCANPROC*')
    uniq = df.drop_duplicates(subset=['tenant', 'pod'])[['pod', 'tenant']]
    uniq.to_csv(f'{dest_root}/pods.csv', index=False)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python splitCSVFiles.py <src_root> <dest_root>")
        sys.exit(1)

    src_root = sys.argv[1]
    dest_root = sys.argv[2]

    source = extractDates(src_root)
    dest = extractDates(dest_root)
    diff = source.difference(dest)
    extractApplianceTenantdb(src_root)

    for dt in diff:
        splitDataFromcsv(src_root, dest_root, dt)