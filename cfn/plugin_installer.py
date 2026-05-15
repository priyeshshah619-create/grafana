import boto3
import json
import cfnresponse

def handler(event, context):
    grafana = boto3.client('grafana')
    
    try:
        workspace_id = event['ResourceProperties']['WorkspaceId']
        plugins = event['ResourceProperties']['Plugins']
        
        if event['RequestType'] in ['Create', 'Update']:
            print(f"Installing plugins {plugins} for workspace {workspace_id}")
            grafana.update_workspace(
                workspaceId=workspace_id,
                pluginAdminEnabled=True,
                plugins=plugins
            )
        
        # Always signal SUCCESS to CloudFormation on Delete to avoid hang
        cfn_response.send(event, context, cfn_response.SUCCESS, {"Status": "Complete"})
        
    except Exception as e:
        print(f"Error: {str(e)}")
        # Signal FAILURE so the stack rolls back properly
        cfn_response.send(event, context, cfn_response.FAILED, {"Message": str(e)})
