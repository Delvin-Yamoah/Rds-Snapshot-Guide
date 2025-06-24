# Simple Lambda Setup for RDS Snapshot Automation

> **Quick Start**: Follow these steps to set up automated daily snapshots with cross-region copying.

## Console Setup Steps

### 1. Create Lambda Function
1. **AWS Lambda** → **Create Function**
2. **Author from Scratch**
3. **Function name**: `rds-snapshot-automation`
4. **Runtime**: Python 3.9
5. **Create function**

### 2. Add the Code
1. Replace the default code with `simple-lambda-function.py`
2. **Update these values**:
   - `'your-rds-instance'` → Your actual RDS instance name
   - `'123456789012'` → Your AWS account ID
   - Change regions if needed

### 3. Create IAM Role
1. **IAM** → **Roles** → **Create role**
2. **AWS service** → **Lambda**
3. **Permissions**: Attach these policies:
   - `AmazonRDSFullAccess` (or create custom policy)
   - `AWSLambdaBasicExecutionRole`
4. **Role name**: `lambda-rds-role`

### 4. Assign Role to Lambda
1. **Lambda function** → **Configuration** → **Permissions**
2. **Execution role** → **Edit**
3. Select `lambda-rds-role`

### 5. Set CloudWatch Trigger
1. **Add trigger** → **EventBridge (CloudWatch Events)**
2. **Create new rule**:
   - **Rule name**: `daily-snapshot`
   - **Schedule expression**: `rate(1 day)`
3. **Add**

## Test the Function
1. **Test** tab → **Create test event**
2. **Test** → Check logs for "Snapshot created" and "Snapshot copied"

## What You Need to Change
- Replace `'your-rds-instance'` with your RDS instance identifier
- Replace `'123456789012'` with your 12-digit AWS account ID
- Update regions if different from us-east-1/us-west-2

That's it! The function will run daily and create + copy snapshots automatically.