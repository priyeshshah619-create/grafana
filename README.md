# Observability Infrastructure Assessment
Automated observability stack using AWS Managed Grafana, CloudWatch, and OpenTelemetry.

## Requirements Checklist
1. **Managed Grafana & SSO:** Managed Workspace with IAM Identity Center.
2. **CloudWatch Observability:** Standardized metrics collection.
3. **Dashboard/Alerts:** Dashboard defined in `main.yaml` (Condition C); Alerts via SNS.
4. **CI/CD:** Full automation via GitHub Actions.
5. **Multi-cloud Standards:** OTEL used for vendor-neutral telemetry.
6. **Business-Driven Monitoring:** OTEL collector configured for business metrics.
7. **Data Consolidation:** Managed Grafana provides a single-pane-of-glass view.

## Conditions
- **Condition A & B:** Custom Resource + Lambda triggered by CI/CD pipeline.
- **Condition C:** Dashboard-as-Code via CloudFormation `AWS::CloudWatch::Dashboard`.
