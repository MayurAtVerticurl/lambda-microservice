import boto3

def lambda_handler(event, context):
    # the region
    region = 'us-east-1' #n-virginia

    # Creating an EC2 client
    ec2 = boto3.client('ec2', region_name=region)

    # Filtering only the instances with the name and running status
    response = ec2.describe_instances(Filters=[
        {
            'Name': 'tag:Name',
            'Values': ['mayTerra']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ])

    # Extracting the instance IDs
    instance_ids = [instance['InstanceId'] for reservation in response['Reservations'] for instance in reservation['Instances']]

    # Stopping the instances
    if instance_ids:
        ec2.stop_instances(InstanceIds=instance_ids)
        print(f"Stopping instances: {', '.join(instance_ids)}")
    else:
        print("No running instances with the name 'mayTerra' found.")

    return {
        'statusCode': 200,
        'body': 'Instances stopped successfully!'
    }
