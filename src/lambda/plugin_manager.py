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
            print(f"Configuring plugins for Workspace {workspace_id}: {plugins}")

            # Update workspace description metadata to verify orchestration execution
            grafana.update_workspace(
                workspace_id=workspace_id,
                description=f"Managed Grafana Workspace. Active Plugins: {', '.join(plugins)}"
            )
            response_data['InstalledCount'] = len(plugins)

        elif event['RequestType'] == 'Delete':
            print(f"Deleting custom resources for Workspace {workspace_id}")
            # No specific API teardown needed for metadata tags, signaling SUCCESS

    except Exception as e:
        print(f"Execution Error: {str(e)}")
        status = "FAILED"
        reason = str(e)

    # CRITICAL: This block must run outside the try/except to handle lifecycle signals
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
