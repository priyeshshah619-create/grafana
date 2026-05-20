import boto3
import json
import sys

# Attempt to import cfnresponse, handle missing file gracefully
try:
    import cfnresponse
except ImportError:
    # If cfnresponse.py is not in the zip, we mock the signal
    class cfnresponse:
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"
        def send(event, context, status, reason): pass
    print("WARNING: cfnresponse not found in deployment package.")

grafana = boto3.client('managedgrafana')

def handler(event, context):
    if event['RequestType'] == 'Delete':
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        return
    try:
        props = event['ResourceProperties']
        grafana.update_workspace_configuration(
            workspaceId=props['WorkspaceId'],
            configuration=json.dumps({"plugins": [{"pluginId": p} for p in props['Plugins']]})
        )
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {"Status": "Success"})
    except Exception as e:
        print(f"Error: {str(e)}")
        cfnresponse.send(event, context, cfnresponse.FAILED, {"Error": str(e)})
