#!/bin/bash
echo "Rolling back to previous version..."
helm rollback nexusguard 1
echo "Rollback complete."
