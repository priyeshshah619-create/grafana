#!/bin/bash

GRAFANA_URL="https://your-workspace-url"
API_KEY="your-api-key"

# Add CloudWatch datasource
curl -X POST "$GRAFANA_URL/api/datasources" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @datasource.json

# Import dashboard
curl -X POST "$GRAFANA_URL/api/dashboards/db" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @dashboard.json

# Import alerts
curl -X POST "$GRAFANA_URL/api/ruler/grafana/api/v1/rules" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @alert.json
