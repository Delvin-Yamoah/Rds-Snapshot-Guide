# RDS Automated Snapshot Setup Guide

## Console Setup (10 minutes)

### Step 1: Create Lambda Function
1. **AWS Lambda Console** → **Create function**
2. **Author from scratch**
3. Configuration:
   - **Function name**: `rds-snapshot-automation`
   - **Runtime**: Python 3.9
   - **Architecture**: x86_64
4. **Create function**

### Step 2: Add Function Code
1. In the Lambda function → **Code** tab
2. Replace default code with the provided `automated-snapshot-lambda.py`
3. **Update these variables**:
   ```python
   db_instance_id = 'your-actual-rds-instance-name'
   account_id = 'your-12-digit-account-id'
   source_region = 'your-source-region'
   destination_region = 'your-target-region'
   ```
4. **Deploy**

### Step 3: Create IAM Role
1. **IAM Console** → **Roles** → **Create role**
2. **AWS service** → **Lambda** → **Next**
3. **Create policy** → **JSON** → Paste `lambda-iam-policy.json` content
4. **Policy name**: `RDSSnapshotAutomationPolicy`
5. **Create policy** → Attach to role
6. **Role name**: `RDSSnapshotAutomationRole`
7. **Create role**

### Step 4: Attach Role to Lambda
1. **Lambda Console** → Your function → **Configuration** → **Permissions**
2. **Execution role** → **Edit**
3. **Existing role** → Select `RDSSnapshotAutomationRole`
4. **Save**

### Step 5: Set Up CloudWatch Trigger
1. **Lambda function** → **Add trigger**
2. **EventBridge (CloudWatch Events)**
3. **Create new rule**:
   - **Rule name**: `daily-rds-snapshot`
   - **Rule type**: Schedule expression
   - **Schedule expression**: `rate(1 day)` or `cron(0 2 * * ? *)` (2 AM daily)
4. **Add**

## Quick Test
1. **Lambda Console** → Your function → **Test**
2. **Create test event** → **Hello World template**
3. **Test** → Check logs for success

## Enable Built-in Automated Backups (Recommended)
1. **RDS Console** → Select your instance → **Modify**
2. **Backup**:
   - **Backup retention period**: 7 days
   - **Backup window**: Choose low-traffic time
3. **Apply immediately**

## Monitoring
- **CloudWatch Logs**: Check Lambda execution logs
- **RDS Console** → **Snapshots**: Verify snapshots are created
- **Target region**: Verify copied snapshots appear

## Cost Optimization
- Set snapshot retention policy
- Delete old snapshots automatically:

```python
# Add to Lambda function
def cleanup_old_snapshots(rds_client, days_to_keep=7):
    snapshots = rds_client.describe_db_snapshots(
        SnapshotType='manual',
        MaxRecords=100
    )
    
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    
    for snapshot in snapshots['DBSnapshots']:
        if snapshot['SnapshotCreateTime'].replace(tzinfo=None) < cutoff_date:
            rds_client.delete_db_snapshot(
                DBSnapshotIdentifier=snapshot['DBSnapshotIdentifier']
            )
```