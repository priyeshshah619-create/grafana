import boto3
import cfnresponse
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(f"Received event: {event}")
    try:
        if event['RequestType'] == 'Delete':
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
            return

        workspace_id = event['ResourceProperties']['WorkspaceId']
        plugins = event['ResourceProperties']['Plugins']
        
        client = boto3.client('grafana')
        
        # Install plugins for the Managed Grafana workspace
        response = client.update_workspace_configuration(
            workspaceId=workspace_id,
            configuration=f'{{"plugins": {plugins}}}'
        )
        
        logger.info(f"Plugin update response: {response}")
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {'Status': 'Plugins Installed'})
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        cfnresponse.send(event, context, cfnresponse.FAILED, {'Error': str(e)})
