# RDS Cross-Region Snapshot Replication

Complete guide for creating, copying, and restoring RDS snapshots across AWS regions with automated backup solutions.

## 📋 Overview

This repository contains everything needed to:

- Create manual RDS snapshots
- Copy snapshots across AWS regions
- Restore snapshots in target regions
- Automate the entire process with Lambda
- Troubleshoot common connection issues

## 🚀 Quick Start

### Manual Process

1. **Create Snapshot**: RDS Console → Instance → Actions → Take Snapshot
2. **Copy Snapshot**: Snapshots → Actions → Copy Snapshot → Select target region
3. **Restore**: Target region → Snapshots → Actions → Restore Snapshot

### Automated Process

1. Deploy the Lambda function from `simple-lambda-function.py`
2. Set up daily CloudWatch trigger
3. Snapshots created and copied automatically

## 📁 Repository Structure

```
├── README.md                           # This file
├── simple-lambda-function.py           # Basic Lambda automation
├── simple-setup-steps.md              # Lambda setup guide
├── lambda-iam-policy.json             # IAM permissions for Lambda
├── RDS-Cross-Region-Connection-Guide.md # Detailed troubleshooting
├── Console-Quick-Fix-Guide.md         # Quick connection fixes
├── automated-snapshot-lambda.py       # Advanced Lambda (optional)
└── automation-setup-guide.md          # Advanced setup guide
```

## 🔧 Setup Instructions

### Prerequisites

- AWS account with RDS, IAM, and Lambda permissions
- Existing RDS instance
- Two AWS regions configured

### Option 1: Simple Automation (Recommended)

Follow [`simple-setup-steps.md`](simple-setup-steps.md) for basic Lambda setup.

**Key changes needed:**

```python
# In simple-lambda-function.py
DBInstanceIdentifier='your-actual-rds-instance-name'  # Replace this
source_region = 'your-source-region'                  # Update if needed
destination_region = 'your-target-region'             # Update if needed
# In the ARN: replace 123456789012 with your account ID
```

### Option 2: Advanced Automation

Use [`automation-setup-guide.md`](automation-setup-guide.md) for enhanced features like error handling and cleanup.

## 🚨 Common Issues & Solutions

### Can't Connect to Restored Database?

**Most common cause**: Security group configuration

**Quick fix:**

1. Check [`Console-Quick-Fix-Guide.md`](Console-Quick-Fix-Guide.md) for immediate solutions
2. Use [`RDS-Cross-Region-Connection-Guide.md`](RDS-Cross-Region-Connection-Guide.md) for detailed troubleshooting

**Top 3 fixes:**

- ✅ Update security group to allow database port
- ✅ Use new endpoint from target region
- ✅ Verify VPC/subnet configuration

## 📊 Cost Optimization

### Snapshot Storage Costs

- Snapshots are charged per GB stored
- Cross-region copies incur additional charges
- Set retention policies to manage costs

### Automation Benefits

- Consistent backup schedule
- Reduced manual errors
- Automated cleanup (with advanced setup)

## 🔒 Security Best Practices

1. **IAM Permissions**: Use least privilege principle
2. **Encryption**: Enable encryption for sensitive data
3. **Network Security**: Configure security groups properly
4. **Access Control**: Limit snapshot access to authorized users

## 📈 Monitoring

### CloudWatch Metrics

- Monitor Lambda execution success/failure
- Track snapshot creation times
- Set up alerts for failed operations

### RDS Console

- Verify snapshots appear in both regions
- Check snapshot status regularly
- Monitor storage usage

## 🧪 Testing

### Manual Testing

```bash
# Test connection to restored instance
mysql -h your-new-endpoint.region.rds.amazonaws.com -u admin -p
```

### Lambda Testing

1. AWS Lambda Console → Test
2. Check CloudWatch Logs for execution details
3. Verify snapshots created in both regions

## 🔄 Maintenance

### Regular Tasks

- Review and delete old snapshots
- Update Lambda function as needed
- Monitor costs and usage
- Test restore procedures

### Cleanup Commands

```bash
# Delete old snapshots
aws rds delete-db-snapshot --db-snapshot-identifier old-snapshot-name

# Delete test instances
aws rds delete-db-instance --db-instance-identifier test-instance --skip-final-snapshot
```

## 📚 Additional Resources

- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [RDS Snapshot Pricing](https://aws.amazon.com/rds/pricing/)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Need help?** Check the troubleshooting guides or review the setup steps for common solutions.
