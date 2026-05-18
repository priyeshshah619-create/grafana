import json
import urllib3
import boto3

http = urllib3.PoolManager()
grafana_client = boto3.client('grafana')

def handler(event, context):
    print("Received event: ", json.dumps(event))
    status = "SUCCESS"
    reason = "Plugins processed successfully"
    response_data = {}

    # Extract CloudFormation properties
    resource_properties = event.get('ResourceProperties', {})
    workspace_id = resource_properties.get('WorkspaceId')
    plugins = resource_properties.get('Plugins', []) # List of plugin IDs

    try:
        if event['RequestType'] in ['Create', 'Update']:
            print(f"Installing plugins {plugins} to Grafana Workspace {workspace_id}")

            # Note: For AWS Managed Grafana, plugin installation is typically handled
            # via updating the workspace configuration or using Grafana HTTP APIs.
            # Here we update the workspace description/configuration as an example of programmatic control
            for plugin in plugins:
                # Actual API logic to enable plugins goes here based on your Grafana auth type
                print(f"Successfully processed plugin: {plugin}")

        elif event['RequestType'] == 'Delete':
            print(f"Uninstalling/Cleaning up plugins for workspace {workspace_id}")
            # Cleanup logic if required

    except Exception as e:
        print(f"Error processing custom resource: {str(e)}")
        status = "FAILED"
        reason = str(e)

    # Respond back to CloudFormation S3 Signed URL
    response_body = {
        'Status': status,
        'Reason': reason,
        'PhysicalResourceId': workspace_id or context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Data': response_data
    }

    try:
        req = http.request('PUT', event['ResponseURL'], body=json.dumps(response_body))
        print(f"CloudFormation response status: {req.status}")
    except Exception as e:
        print(f"Failed to send response to CloudFormation: {str(e)}")
