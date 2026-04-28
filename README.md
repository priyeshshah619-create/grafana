#!/bin/bash

# Use your actual workspace URL found in your browser tab
GRAFANA_URL="https://g-a07f04a423.grafana-workspace.us-east-1.amazonaws.com"
# It is better to pass the key as an environment variable: export GRAFANA_API_TOKEN='your-key'
API_KEY="${GRAFANA_API_TOKEN}"

echo "🚀 Starting Grafana Provisioning..."

# 1. Add CloudWatch datasource
echo "Configuring Data Source..."
curl -X POST "$GRAFANA_URL/api/datasources" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @datasource.json

# 2. Import dashboard
echo "Importing Dashboard..."
curl -X POST "$GRAFANA_URL/api/dashboards/db" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @dashboard.json

# 3. Import alerts (Fixed API Path for Amazon Managed Grafana)
echo "Importing Alert Rules..."
curl -X POST "$GRAFANA_URL/api/v1/provisioning/alert-rules" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @alert.json

echo "✅ Done!"
