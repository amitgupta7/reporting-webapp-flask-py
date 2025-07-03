from flask import Flask, render_template, request, jsonify
import os, sys
import pandas as pd
import util.dataframeloader as dfl
import plotly
import json
import csv

app = Flask(__name__)
root = '.applianceDataDir'
data = {}

with app.app_context():
    with open(f'{root}/pods.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pod = row['pod']
            tenant = row['tenant']
            if tenant not in data:
                data[tenant] = []
            data[tenant].append(pod)
 
@app.route("/tenants", methods=["GET"])
def tenants():
    return jsonify(sorted(data.keys()))            

@app.route("/pods/<tenant>", methods=["GET"])
def pods(tenant):
    return jsonify(sorted(data[tenant]))
    


@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    graphJSON = None 
    appliance_id = "Select Appliance ID"
    startDate = None
    endDate = None
    tenant_db = "Select Tenant"
    categories = sorted(data.keys())
    if request.method == "POST":
        appliance_id = request.form.get("appliance_id")
        tenant_db = request.form.get("tenant_db")
        startDate = request.form.get("start_date")
        endDate = request.form.get("end_date")
        try:
            root_appliance = f'{root}/{appliance_id}'
            li = []
            for filenm in os.listdir(root_appliance):
                if dfl.checkDateRangeFromFileName([startDate, endDate], filenm): 
                    tmp_df = pd.read_csv(f'{root_appliance}/{filenm}')
                    li.append(tmp_df)
            pod_df = pd.concat(li, axis=0, ignore_index=True)
            if pod_df.empty:
                print(f'No data found for pod: {appliance_id}')
                sys.exit(1)
            pod_df['ts'] = pd.to_datetime(pod_df['ts'])
            fig  = dfl.plotMetricsFacetForApplianceId(pod_df, appliance_id)
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        except Exception as e:
            return render_template("index.html", message=f"{message}\nError processing data: {e}", categories=categories, tenant_db=tenant_db, appliance_id=appliance_id, start_date=startDate, end_date=endDate)

    return render_template("index.html", graphJSON=graphJSON, appliance_id=appliance_id, start_date=startDate, end_date=endDate, categories=categories, tenant_db=tenant_db )

if __name__ == "__main__":
    app.run(debug=True)
    
