# Quick Console Fix for RDS Cross-Region Connection Issues

> **TL;DR**: 90% of connection issues are security group problems. Check Step 3 first!

## 🚨 Quick Diagnosis (2 minutes)

### Step 1: Check Your Instance Status
1. AWS Console → **RDS** → **Databases**
2. Switch to your **target region** (top-right corner)
3. Find your restored instance
4. Status should be **Available** (if not, wait)

### Step 2: Get the New Endpoint
1. Click on your restored instance name
2. **Connectivity & security** tab
3. Copy the **Endpoint** (this is different from your original region!)

### Step 3: Check Security Groups
1. Same page → **VPC security groups** section
2. Click on the security group link
3. **Inbound rules** tab
4. Look for rule allowing your database port:
   - MySQL: Port 3306
   - PostgreSQL: Port 5432
   - SQL Server: Port 1433

## 🔧 Quick Fixes

### Fix 1: Security Group Issue (Most Common)
**If you don't see your database port in inbound rules:**

1. **EC2 Console** → **Security Groups**
2. Find your RDS security group
3. **Inbound rules** → **Edit inbound rules**
4. **Add rule**:
   - Type: **Custom TCP**
   - Port: **3306** (or your DB port)
   - Source: **My IP** (for testing) or specific IP range
5. **Save rules**

### Fix 2: Wrong Endpoint
**Update your connection string with the new endpoint:**

❌ **Old**: `original-db.us-east-1.rds.amazonaws.com`
✅ **New**: `rds-replica-instance.us-west-2.rds.amazonaws.com`

### Fix 3: VPC/Subnet Issue
**If instance is in wrong VPC:**

1. **RDS Console** → Select instance → **Modify**
2. **Network & Security** section
3. Change **Subnet group** if needed
4. **Apply immediately**

## 🧪 Test Connection

### From Command Line:
```bash
# MySQL
mysql -h YOUR-NEW-ENDPOINT -u admin -p

# PostgreSQL  
psql -h YOUR-NEW-ENDPOINT -U admin -d mydb
```

### From Application:
Update connection string to use the new endpoint from Step 2 above.

## ⚡ 30-Second Checklist

- [ ] Instance status = Available
- [ ] Using new endpoint (not old region's endpoint)
- [ ] Security group allows database port
- [ ] Correct username/password
- [ ] Application pointing to new region

## 🆘 Still Not Working?

1. **Check VPC**: Instance might be in private subnet
2. **Check Route Tables**: Ensure proper routing
3. **Check NACLs**: Network ACLs might be blocking
4. **Check Parameter Groups**: May need to create compatible one

**Most issues are solved by fixing the security group and using the correct endpoint!**