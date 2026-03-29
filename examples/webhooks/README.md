# Webhook Integrations for Goal

This directory contains webhook integration examples for notifications.

## Available Integrations

- [Slack](slack-webhook.py) - Slack notifications
- [Discord](discord-webhook.py) - Discord notifications
- [Microsoft Teams](teams-webhook.py) - Teams notifications
- [Generic HTTP](generic-webhook.py) - Custom webhook support

## Configuration

Add to your `goal.yaml`:

```yaml
advanced:
  notifications:
    webhooks:
      slack:
        url: "${SLACK_WEBHOOK_URL}"
        events: ["commit", "push", "publish"]
      
      discord:
        url: "${DISCORD_WEBHOOK_URL}"
        events: ["publish"]
```

## Environment Variables

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
export TEAMS_WEBHOOK_URL="https://outlook.office.com/webhook/..."
```

## Usage

Webhooks are automatically triggered by Goal events. To test manually:

```bash
python slack-webhook.py "Test message"
```
