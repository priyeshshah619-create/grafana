# AWS Managed Grafana Observability – End-to-End Automation

This project demonstrates how to build a complete observability stack in a **single AWS account** using Infrastructure as Code and automation.

It provisions a Grafana workspace, integrates SSO, connects CloudWatch Logs as a data source, creates dashboards and alerts, and sends notifications through SNS — all reproducible from code.

---

## 🚀 Services Used

- Amazon Managed Grafana
- AWS IAM Identity Center (SSO)
- Amazon CloudWatch Logs
- Amazon SNS
- GitHub Actions
- AWS CloudFormation (IaC)

---

## 🎯 Observability Scenario

**Order Service Log Monitoring**

A sample application log group `/app/order-service` is used to simulate logs.

Grafana dashboards visualize:

- Log ingestion rate
- Error count over time
- Log trends

An alert is configured:

> Trigger SNS notification when **error count > 0 for 2 minutes**

---

## 🧱 Architecture Flow
