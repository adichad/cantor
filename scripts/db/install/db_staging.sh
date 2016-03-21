#!/bin/bash
mysql -h "new-rds-askme.c0wj8qdslqom.ap-southeast-1.rds.amazonaws.com" -u "askme" -p < db_create.sql
