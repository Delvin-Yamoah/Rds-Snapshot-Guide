import boto3

source_region = "us-east-1"
destination_region = "us-west-2"
snapshot_name = "rds-auto-snapshot"
copy_name = "rds-auto-copy"

rds = boto3.client("rds", region_name=source_region)


def lambda_handler(event, context):
    response = rds.create_db_snapshot(
        DBInstanceIdentifier="your-rds-instance", DBSnapshotIdentifier=snapshot_name
    )

    print("Snapshot created:", response)

    copy_response = rds.copy_db_snapshot(
        SourceDBSnapshotIdentifier=f"arn:aws:rds:{source_region}:123456789012:snapshot/{snapshot_name}",
        TargetDBSnapshotIdentifier=copy_name,
        SourceRegion=source_region,
        DestinationRegion=destination_region,
    )

    print("Snapshot copied:", copy_response)
