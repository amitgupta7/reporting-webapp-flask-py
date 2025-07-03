$(VERBOSE).SILENT:
DAYS ?= 7
VENV=". ./venv/bin/activate"
usage:
	echo "USAGE:"
	echo "make init		Install prerequisite libs."
	echo "make auth		Authenticate aws cli with web sso."
	echo "make sync-ndays		Sync between date range. See readme for details."
	echo "make split-csv		Split the csv files into individual pod files."
	echo "make report		Generate the support report for a pod."
	echo "make run		Start flask web server."

init: venv
	eval ${VENV} && pip install --upgrade build
	eval ${VENV} && python -m build 
	eval ${VENV} && pip install .

venv:
	test -d venv || python3 -m venv venv

run: venv
	# eval ${VENV} && python app.py
	eval ${VENV} && gunicorn -w 2 --bind localhost:5000 app:app

preflight:
	echo "checking ..."
	type aws >/dev/null 2>&1 || { echo >&2 "aws-cli is not installed.  See https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html for steps."; exit 1; }
	echo "aws-cli is installed."

sync-ndays: preflight
	mkdir -p .dataDir
	echo "syncing files for days: ${DAYS}."
	aws s3 sync --size-only $(shell eval ${VENV} && python3 util/awsExcludeStrGenerator.py ${DAYS}) s3://securiti-cx-exports/cx/ .dataDir 

split-csv:
	mkdir -p .applianceDataDir
	eval ${VENV} && python util/splitCSVFiles.py '.dataDir' '.applianceDataDir'

auth: preflight
	mkdir -p ~/.aws
	test -f ~/.aws/config && cmp ~/.aws/config aws-data-sync/config || mv ~/.aws/config ~/.aws/config.bak
	cp aws-data-sync/config ~/.aws
	aws sso login --no-browser 

report:
	eval ${VENV} && python util/generateApplianceSupportReport.py '.applianceDataDir/${POD}' ${POD} ${DAYS}