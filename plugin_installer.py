import boto3
import json
import cfnresponse

def handler(event, context):
    grafana = boto3.client('grafana')
    workspace_id = event['ResourceProperties']['WorkspaceId']
    plugins = event['ResourceProperties']['Plugins'] # List like ["grafana-clock-panel"]
    
    try:
        if event['RequestType'] in ['Create', 'Update']:
            print(f"Installing plugins {plugins} for workspace {workspace_id}")
            grafana.update_workspace(
                workspaceId=workspace_id,
                plugins=plugins
            )
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    except Exception as e:
        print(f"Error: {str(e)}")
        cfnresponse.send(event, context, cfnresponse.FAILED, {"Message": str(e)})
