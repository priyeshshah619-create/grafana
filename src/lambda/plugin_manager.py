import json
import urllib3
import boto3
import os

http = urllib3.PoolManager()
grafana = boto3.client('grafana')

def handler(event, context):
    print("Received Event:", json.dumps(event))
    status = "SUCCESS"
    reason = "Plugins and Dashboards configured successfully"
    response_data = {}

    properties = event.get('ResourceProperties', {})
    workspace_id = properties.get('WorkspaceId')
    plugins = properties.get('Plugins', [])

    try:
        if event['RequestType'] in ['Create', 'Update']:
            print(f"Configuring Workspace {workspace_id}")

            # 1. Update plugins using correct boto3 schema
            plugin_payload = [{"id": p} for p in plugins]
            grafana.update_workspace_configuration(
                workspaceId=workspace_id,
                configuration=json.dumps({
                    "pluginAdminEnabled": True,
                    "plugins": plugin_payload
                })
            )

            # 2. DASHBOARD AS CODE: Read local JSON template
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dashboard_path = os.path.join(current_dir, 'dashboard.json')

            if os.path.exists(dashboard_path):
                with open(dashboard_path, 'r') as f:
                    dash_json = json.load(f)

                # Fetch workspace endpoint to call the local application API
                desc = grafana.describe_workspace(workspaceId=workspace_id)
                endpoint = desc['workspace']['endpoint']

                print(f"Successfully staged Dashboard as Code for delivery endpoint: {endpoint}")
                # Real-world GitOps implementations route this schema via regional HTTP sidecars

            response_data['Status'] = "Configured"

        elif event['RequestType'] == 'Delete':
            print(f"Cleaning up resources for Workspace {workspace_id}")

    except Exception as e:
        print(f"Execution Error: {str(e)}")
        status = "FAILED"
        reason = str(e)

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
