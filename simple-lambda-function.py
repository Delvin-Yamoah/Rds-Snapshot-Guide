import boto3
from datetime import datetime

source_region = "us-east-1"
destination_region = "us-west-2"
db_instance_id = "your-rds-instance"  # Replace with your RDS instance
account_id = "123456789012"  # Replace with your AWS account ID
rds = boto3.client("rds", region_name=source_region)

def lambda_handler(event, context):
    # Generate unique snapshot names with timestamp
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    snapshot_name = f"rds-auto-snapshot-{timestamp}"
    copy_name = f"rds-auto-copy-{timestamp}"
    
    try:
        # Create snapshot
        print(f"Creating snapshot: {snapshot_name}")
        response = rds.create_db_snapshot(
            DBInstanceIdentifier=db_instance_id,
            DBSnapshotIdentifier=snapshot_name
        )
        print("Snapshot creation initiated:", response['DBSnapshot']['DBSnapshotIdentifier'])
        
        # Wait for snapshot to complete
        print("Waiting for snapshot to complete...")
        waiter = rds.get_waiter('db_snapshot_completed')
        waiter.wait(
            DBSnapshotIdentifier=snapshot_name,
            WaiterConfig={'Delay': 30, 'MaxAttempts': 120}  # Wait up to 60 minutes
        )
        print(f"Snapshot {snapshot_name} completed successfully")
        
        # Get RDS instance KMS key if encrypted
        instance_response = rds.describe_db_instances(DBInstanceIdentifier=db_instance_id)
        db_instance = instance_response['DBInstances'][0]
        
        # Copy snapshot to destination region using destination region client
        rds_dest = boto3.client("rds", region_name=destination_region)
        source_arn = f"arn:aws:rds:{source_region}:{account_id}:snapshot:{snapshot_name}"
        
        copy_params = {
            'SourceDBSnapshotIdentifier': source_arn,
            'TargetDBSnapshotIdentifier': copy_name,
            'SourceRegion': source_region
        }
        
        if db_instance.get('StorageEncrypted', False):
            # Use default RDS KMS key in destination region
            copy_params['KmsKeyId'] = 'alias/aws/rds'
            print(f"Using default RDS KMS key in destination region")
        
        print(f"Copying snapshot to {destination_region}...")
        copy_response = rds_dest.copy_db_snapshot(**copy_params)
        print("Snapshot copied:", copy_response['DBSnapshot']['DBSnapshotIdentifier'])
        
        return {
            'statusCode': 200,
            'body': f"Success: {snapshot_name} created and copied as {copy_name}"
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
