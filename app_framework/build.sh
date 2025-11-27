#!/usr/bin/env bash

set -e  # exit on first error

# Always run from the directory where this script lives
cd "$(dirname "$0")"

echo "🔧 Rebuilding legal_case_roster_db ..."

mysql -u root < database/01_create_schema.sql
mysql -u root < database/02_create_app_user.sql
mysql -u root < database/03_insert_sample_data.sql


