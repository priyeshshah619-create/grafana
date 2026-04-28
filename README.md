# AWS Managed Grafana Observability – End-to-End Automation

This repository contains a fully automated observability stack built as part of a technical assessment. It demonstrates the ability to provision infrastructure, configure data sources, and deploy monitoring assets (dashboards/alerts) entirely through code.

## 🎯 Assessment Scenario: SNS Health Monitoring
To demonstrate "Application specific business-driven monitoring," this setup monitors the reliability of an AWS SNS notification system.
- **Metric**: `NumberOfNotificationsFailed` (CloudWatch).
- **Automation**: If any notification fails for a 2-minute period, a Grafana Alert is triggered to notify the engineering team.

## 🚀 Key Requirements Addressed

### 1. Infrastructure as Code (Requirement 1 & 2)
- **AWS Managed Grafana**: Provisioned via CloudFormation in [grafana-workspace.yaml](./cfn/grafana-workspace.yaml).
- **SSO Integration**: Configured with `AWS_SSO` for secure workforce identity.
- **SNS Integration**: Provisioned via [sns.yaml](./cfn/sns.yaml), including the required Topic Policy for CloudWatch permissions.

### 2. Automated Provisioning (Requirement 3 & 4)
- **CI/CD Pipeline**: Uses **GitHub Actions** ([deploy-sns.yaml](.github/workflows/deploy-sns.yaml)) to push configuration changes.
- **Grafana API**: Automatically provisions the [CloudWatch Data Source](./datasource.json), [Dashboards](./dashboard.json), and [Alert Rules](./alert.json) without manual console intervention.

### 3. Modern Data Collection (Requirement 6 & 7)
- **OpenTelemetry (OTEL)**: Included [otel-config.yaml](./otel-config.yaml) to demonstrate a standardized, vendor-neutral framework for collecting application metrics and logs.
- **Consolidation**: Metrics are consolidated from OTLP receivers into AWS CloudWatch as the centralized backend.

### 4. Multi-Cloud Standards (Requirement 5)
- By using the Grafana API and standard JSON definitions, this architecture is "Cloud Agnostic." The same deployment logic used here for AWS can be extended to Azure Monitor or Google Cloud Monitoring by simply swapping the data source definition.

## ⚙️ Repository Structure
- `.github/workflows/`: GitHub Action for automated deployment.
- `cfn/`: CloudFormation templates for AWS Infrastructure.
- `scripts/`: Manual provisioning backup script.
- `*.json`: Grafana asset definitions (Data Source, Dashboard, Alerts).
- `otel-config.yaml`: Standardized OTEL collector configuration.

---
**Status**: End-to-End Automated 🚀
