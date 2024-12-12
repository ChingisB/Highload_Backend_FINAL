# Distributed Systems and Data Consistency

## Overview

This document outlines the distributed architecture for handling data replication and ensuring consistency across multiple nodes.

---

## Distributed Database Options

### DynamoDB

DynamoDB is a fully managed NoSQL database service provided by AWS. It is designed to handle large-scale, high-performance data storage and retrieval. 

#### Configuration:
- Region: `us-east-1`
- Tables: `my_table`
- Read/Write Capacity: `5/5`

---

## PostgreSQL Configuration

### PostgreSQL Cluster Setup

For the PostgreSQL distributed system, we configure data replication and ensure consistency using the following settings:

#### pg_hba.conf

Configuration is set for permissions and user and defining the hosts that can 
connect to the database. Could be specified to use replication host and 
app host

```conf
local all all trust
host all all 0.0.0.0/0 md5
host all all ::/0 md5
host replication myuser 0.0.0.0/0 md5
```

#### postgresql.conf

This document is used for the master db.

```conf
wal_level = replica
max_wal_senders = 10
wal_keep_size = 64MB
listen_addresses = '*'
```
## Data Replication and Consistency Models
### Data Replication Strategies
* Master-Slave Replication: Writes occur on the master, and changes are propagated to slaves.
* Multi-Master Replication: Multiple masters and synchronization ensures consistency.
* CRDT (Conflict-free Replicated Data Types): Utilized for eventual consistency across nodes.

## Consistency Models
* Strong Consistency: All nodes are in sync and transactions are ACID-compliant.
* Eventual Consistency: Systems converge to a consistent state over time.
* Linearizability: Strong form of consistency ensuring a globally agreed state.