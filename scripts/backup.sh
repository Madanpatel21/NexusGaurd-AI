#!/bin/bash
echo "Backing up PostgreSQL..."
pg_dump -U user nexusguard > backup_$(date +%F).sql
echo "Backup complete."
