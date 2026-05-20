import boto3
import json
import cfnresponse

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
        cfnresponse.send(event, context, cfnresponse.FAILED, {"Error": str(e)})
