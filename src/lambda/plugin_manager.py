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

    # PASTE YOUR SERVICE ACCOUNT TOKEN FROM STEP 1 HERE
    GRAFANA_TOKEN = glsa_PiE4w5o2MRqrVFupaZmVJ7XMPffr0ND7_1d9a7962

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

            # 2. DASHBOARD AS CODE: Import directly into the UI engine
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dashboard_path = os.path.join(current_dir, 'dashboard.json')

            if os.path.exists(dashboard_path) and "glsa_" in GRAFANA_TOKEN:
                with open(dashboard_path, 'r') as f:
                    dash_json = json.load(f)

                # Fetch workspace live HTTP endpoint
                desc = grafana.describe_workspace(workspaceId=workspace_id)
                raw_endpoint = desc['workspace']['endpoint']
                url = f"https://{raw_endpoint}/api/dashboards/db"

                # Format standard Grafana API payload object
                api_payload = json.dumps({
                    "dashboard": dash_json,
                    "overwrite": True
                })

                print(f"Pushing Dashboard asset directly to: {url}")

                # Send the dashboard authenticated via the Service Account Token
                response = http.request(
                    'POST',
                    url,
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f"Bearer {GRAFANA_TOKEN}"
                    },
                    body=api_payload
                )
                print(f"Grafana Dashboard API responded with code: {response.status}")

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
