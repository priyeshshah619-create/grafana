import json
import urllib3
import boto3

http = urllib3.PoolManager()
grafana = boto3.client('grafana')

def handler(event, context):
    print("Received Event:", json.dumps(event))
    status = "SUCCESS"
    reason = "Plugins configured successfully"
    response_data = {}

    properties = event.get('ResourceProperties', {})
    workspace_id = properties.get('WorkspaceId')
    plugins = properties.get('Plugins', [])

    try:
        if event['RequestType'] in ['Create', 'Update']:
            print(f"Installing plugins for Workspace {workspace_id}: {plugins}")

            # 1. Map plugins to the exact list schema AWS expects: [{"id": "name"}]
            plugin_payload = [{"id": p} for p in plugins]

            # 2. Build the correct flat dictionary schema required by the AWS SDK
            config_model = {
                "pluginAdminEnabled": True,
                "plugins": plugin_payload
            }

            # 3. Pass the payload stringified as required by boto3
            grafana.update_workspace_configuration(
                workspaceId=workspace_id,
                configuration=json.dumps(config_model)
            )
            response_data['InstalledCount'] = len(plugins)

        elif event['RequestType'] == 'Delete':
            print(f"Deleting custom resources for Workspace {workspace_id}")

    except Exception as e:
        print(f"Execution Error: {str(e)}")
        status = "FAILED"
        reason = str(e)

    # Send lifecycle signals safely back to CloudFormation's callback URL
    response_body = json.dumps({
        'Status': status,
        'Reason': reason,
        'PhysicalResourceId': workspace_id or context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Data': response_data
    }).encode('utf-8')

    try:
        response = http.request('PUT', event['ResponseURL'], body=response_body)
        print(f"CloudFormation API responded with status: {response.status}")
    except Exception as e:
        print(f"Failed to signal CloudFormation callback: {str(e)}")
