import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(event)
    dims = json.loads(event["Records"][0]["Sns"]["Message"])['Trigger']['Dimensions']
    for dim in dims:
        if dim['name'] == 'InstanceId':
            instance_id = dim['value']
    print(instance_id)
    
    ssm_client = boto3.client('ssm')
    response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': ["sudo su", "cd /home/ec2-user", "./size.sh"]}, )

    command_id = response['Command']['CommandId']
    output = ssm_client.get_command_invocation(
        CommandId=command_id,
        InstanceId=instance_id,
        )
    print(output)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }