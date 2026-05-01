# AWS Managed Grafana Observability – End-to-End Automation

This repository contains a fully automated observability stack built as part of a technical assessment. It demonstrates the ability to provision infrastructure, configure data sources, and deploy monitoring assets (dashboards/alerts) entirely through code.

## 🎯 Assessment Scenario: SNS Health Monitoring
To demonstrate "Application-specific business-driven monitoring," this setup monitors the reliability of an AWS SNS notification system.
- **Metric**: `NumberOfNotificationsFailed` (CloudWatch).
- **Automation**: If any notification fails for a 2-minute period, a Grafana Alert is triggered to notify the engineering team.

## 🚀 Key Requirements Addressed

### 1. Infrastructure as Code & Custom Resources (Requirement 1)
- **AWS Managed Grafana**: Provisioned via CloudFormation in [grafana-workspace.yaml](https://github.com/priyeshshah619-create/grafana/blob/main/cfn/grafana-workspace.yaml).
- **SSO Integration**: Configured with `AWS_SSO` for secure workforce identity.
- **Plugin Automation (Custom Resource)**: Features a **Lambda-backed Custom Resource** (`Custom::GrafanaPluginInstaller`) that programmatically installs plugins (like `grafana-piechart-panel`) during stack creation. This extends standard CloudFormation logic to ensure the workspace is fully functional upon deployment.

### 2. CloudWatch & Alerting (Requirement 2 & 3)
- **SNS Integration**: Provisioned via [sns.yaml](https://github.com/priyeshshah619-create/grafana/blob/main/cfn/sns.yaml), including a Topic Policy allowing Grafana to publish alerts.
- **Notification Loop**: Automated link between Grafana alerts and the [Health-Alerts-Topic](https://us-east-1.console.aws.amazon.com/sns/v3/home?region=us-east-1#/topic/arn:aws:sns:us-east-1:882352060841:Health-Alerts-Topic) via [contact-point.json](https://github.com/priyeshshah619-create/grafana/blob/main/contact-point.json).

### 3. Automated Provisioning (Requirement 4)
- **CI/CD Pipeline**: Uses **GitHub Actions** ([deploy-sns.yaml](https://github.com/priyeshshah619-create/grafana/blob/main/.github/workflows/deploy-sns.yaml)) to push configuration changes.
- **Grafana API**: Automatically provisions the [Data Source](https://github.com/priyeshshah619-create/grafana/blob/main/datasource.json), [Dashboard](https://github.com/priyeshshah619-create/grafana/blob/main/dashboard.json), and [Alert Rules](https://github.com/priyeshshah619-create/grafana/blob/main/alert.json) without manual console intervention.

### 4. Modern Data Collection & OTEL (Requirement 6 & 7)
- **OpenTelemetry (OTEL)**: Included [otel-config.yaml](https://github.com/priyeshshah619-create/grafana/blob/main/otel-config.yaml) to demonstrate a standardized framework for collecting and consolidating application metrics and logs into CloudWatch.

### 5. Multi-Cloud Standards (Requirement 5)
- **Standardization**: Utilizes **Prometheus** definitions in [datasource.json](https://github.com/priyeshshah619-create/grafana/blob/main/datasource.json) to demonstrate cloud-agnostic observability practices.

## ⚙️ Repository Structure
- `.github/workflows/`: GitHub Action for automated deployment.
- `cfn/`: CloudFormation templates including the Custom Resource logic.
- `*.json`: Grafana asset definitions (Data Source, Dashboard, Alerts).
- `otel-config.yaml`: Standardized OTEL collector configuration.

**Status**: 100% Automated & Requirement Compliant 🚀
