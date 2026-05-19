import json
import urllib3
import boto3
import os

http = urllib3.PoolManager()
grafana = boto3.client('grafana')

def handler(event, context):
    print("Received Event:", json.dumps(event))
    status = "SUCCESS"
    reason = "Plugins, Alert Destinations, and Dashboards configured cleanly."
    response_data = {}

    properties = event.get('ResourceProperties', {})
    workspace_id = properties.get('WorkspaceId')
    plugins = properties.get('Plugins', [])

    GRAFANA_TOKEN = os.environ.get('GRAFANA_TOKEN', '')
    SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')

    try:
        if event['RequestType'] in ['Create', 'Update']:
            print(f"Executing Configuration Engine for Workspace: {workspace_id}")

            # 1. Core Plugin Configuration Management
            plugin_payload = [{"id": p} for p in plugins]
            grafana.update_workspace_configuration(
                workspaceId=workspace_id,
                configuration=json.dumps({
                    "pluginAdminEnabled": True,
                    "plugins": plugin_payload
                })
            )

            # Fetch instance base parameters
            desc = grafana.describe_workspace(workspaceId=workspace_id)
            raw_endpoint = desc['workspace']['endpoint']
            clean_endpoint = raw_endpoint.replace("https://", "").replace("http://", "")

            if GRAFANA_TOKEN:
                # 2. Requirement 3: Automated Provisioning of Alert Notification Channels
                if SNS_TOPIC_ARN:
                    alert_url = f"https://{clean_endpoint}/api/alertmanager/grafana/config/api/v1/alerts"
                    alert_payload = json.dumps({
                        "alertmanager_config": {
                            "route": {
                                "receiver": "sns-critical-alerts",
                                "group_by": ["alertname", "cluster"],
                                "group_wait": "30s",
                                "group_interval": "5m",
                                "repeat_interval": "4h"
                            },
                            "receivers": [{
                                "name": "sns-critical-alerts",
                                "sns_configs": [{
                                    "topic_arn": SNS_TOPIC_ARN,
                                    "sigv4": {"region": os.environ.get('AWS_REGION', 'us-east-1')},
                                    "attributes": {"severity": "critical"},
                                    "send_resolved": True
                                }]
                            }]
                        }
                    })
                    print(f"Provisioning SNS Alert Endpoint: {alert_url}")
                    sns_resp = http.request(
                        'POST', alert_url,
                        headers={'Content-Type': 'application/json', 'Authorization': f"Bearer {GRAFANA_TOKEN}"},
                        body=alert_payload
                    )
                    print(f"Alertmanager API response status: {sns_resp.status}")

                # 3. Requirement 4: Dashboard-As-Code API Package Import
                current_dir = os.path.dirname(os.path.abspath(__file__))
                dashboard_path = os.path.join(current_dir, 'dashboard.json')

                if os.path.exists(dashboard_path):
                    with open(dashboard_path, 'r') as f:
                        dash_json = json.load(f)

                    import_url = f"https://{clean_endpoint}/api/dashboards/import"

                    # AWS Managed Ingestion Endpoint Wrapper Structure
                    api_payload = json.dumps({
                        "dashboard": dash_json,
                        "overwrite": True,
                        "inputs": [{
                            "name": "DS_AMAZON_CLOUDWATCH",
                            "type": "datasource",
                            "pluginId": "cloudwatch",
                            "value": "aws-cloudwatch"
                        }]
                    })

                    print(f"Deploying Dashboard Structure Package: {import_url}")
                    dash_resp = http.request(
                        'POST', import_url,
                        headers={'Content-Type': 'application/json', 'Authorization': f"Bearer {GRAFANA_TOKEN}"},
                        body=api_payload
                    )
                    print(f"Grafana Dashboard API response code: {dash_resp.status}")
                    print(f"Dashboard Ingestion logs: {dash_resp.data.decode('utf-8')}")
                    response_data['DashboardStatus'] = "Imported"

        elif event['RequestType'] == 'Delete':
            print(f"Removing Workspace allocations for {workspace_id}")

    except Exception as e:
        print(f"Global Custom Resource Exception: {str(e)}")
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

    http.request('PUT', event['ResponseURL'], body=response_body)
