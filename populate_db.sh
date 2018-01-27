#!/usr/bin/env bash
source ./venv/bin/activate
python db_create_tables.py
python db_create_users.py
