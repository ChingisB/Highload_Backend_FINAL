# Fault Tolerance and Resilience

## Overview

This document outlines the fault tolerance and resilience strategies available for 
implementation to ensure performance.

---

## Redundancy in Critical Components

### Database Replication

To ensure fault tolerance in the database layer, replication has been implemented with the following configuration:

#### Primary-Replica Setup
- **Primary Node:** Handles write operations.
- **Replica Nodes:** Serve read operations and act as failover in case the primary node fails.

#### Configuration Details

##### pg_hba.conf
```conf
local all all trust
host all all 0.0.0.0/0 md5
host all all ::/0 md5
host replication myuser 0.0.0.0/0 md5
```

##### postgresql.conf
```conf
wal_level = replica
max_wal_senders = 10
wal_keep_size = 64MB
listen_addresses = '*'
```

#### Failover Management
### Application Layer
- **Load Balancer:** Distributes traffic among application instances to avoid single points of failure.
- **Auto-Scaling:** Automatically adjusts the number of instances based on traffic.

---

## Backup Strategies

### Regular Backups
- **Frequency:** Daily backups for critical data (user data, orders).
- **Storage:** Backups are stored in both local and cloud storage for redundancy.
- **Tool:** `pg_dump` for logical backups and `pg_basebackup` for physical backups.

#### Backup Script Example
```bash
#!/bin/bash
DATE=$(date +%F)
BACKUP_DIR=/backups/$DATE
mkdir -p $BACKUP_DIR
pg_dump -U myuser mydb > $BACKUP_DIR/mydb.sql
pg_basebackup -U myuser -D $BACKUP_DIR/base -Ft -z -P
```

### Backup Validation
- **Checksum Validation:** Ensures integrity of backup files.
- **Restore Testing:** Periodic restore tests to verify backup usability.

---

## Disaster Recovery Plan

### Recovery Objectives
- **RPO (Recovery Point Objective):** 15 minutes.
- **RTO (Recovery Time Objective):** 1 hour.

### Disaster Scenarios and Recovery Steps

#### Database Failure
1. **Failover:** Promote a replica to primary using failover management tool. Partially implemented using database router.
2. **Data Restoration:** Restore the latest backup to bring the replica back online.

#### Application Downtime
1. **Redeploy Application:** Use container orchestration tools to redeploy failed instances. Setup via docker compose could be used.
2. **Redirect Traffic:** Update load balancer to exclude failed instances.

#### Data Center Outage
#### NOTE! I don't have money and knowledge for that
1. **Activate Secondary Data Center:** Deploy applications and database replicas in a secondary data center.
2. **DNS Update:** Redirect traffic to the secondary data center.

---

## Monitoring and Alerts

### Tools
- **Prometheus**: For metrics collection.
- **Grafana**: For visualization and alerting.

### Monitored Metrics
- Django application logs. 
Can be setup to monitor other tools.
