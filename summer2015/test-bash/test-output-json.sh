#!/usr/bin/env bash
# Test script to write json file
echo '{
    "pulp": {
        "auth": [
            "admin",
            "admin"
        ],
        "base_url": "https://dev",
        "cli_transport": "local",
        "verify": true,
        "version": "2.9.0b1"
    }
}' | python -m json.tool > test.json
pulp-admin status | grep "Platform Version" | awk '{ print $3 }'