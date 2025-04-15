# Apple Certificate & Provisioning Profile Expiry Notifier

This automation checks your Apple Developer **certificates** and **provisioning profiles** for upcoming expirations and sends a summary to **Slack**.
Ideal for teams who want proactive alerts before builds start failing due to expired assets.

---

## Features

- Detects Apple certificates and provisioning profiles expiring soon
- Configurable expiry warning window (default: 30 days)
- Sends detailed Slack notifications
- Uses App Store Connect API key (no passwords or 2FA hassles)

---

## Requirements

- macOS with [Homebrew](https://brew.sh)
- Access to an Apple Developer account
- A Slack Incoming Webhook URL
- An App Store Connect API key in `.json` format

---

## Setup

### 1. Install Fastlane
```bash
brew install fastlane
```
### 2. Create App Store Connect API Key

1. Go to [App Store Connect → Users and Access → Keys](https://appstoreconnect.apple.com/access/api).
2. Create a new key and download the `.p8` file.
3. Save the full key info as a `.json` file:

```json
{
  "key_id": "ABC123",
  "issuer_id": "1111111-abcd",
  "key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----"
}
```

### 3. Configure Slack Webhook
1. Go to your Slack workspace → Integrations → Incoming Webhooks
2. Create a new webhook and copy the URL
3. Set it in your .env


### 4. To Run The Lane
1. Clone the repository
2. Navigate to the directory
3. Run the lane:
```bash
fastlane check_expiry
```

## Slack Message Example
When certificates or provisioning profiles are expiring soon, the script sends a message like this:
```markdown
⚠️ Certificates/Profiles expiring soon:
🔐 Cert: iOS Distribution - Expires: 2025-04-30
📄 Profile: MyApp_Dev - Expires: 2025-04-25
```

If nothing's expiring soon, it will send:
```markdown
✅ All certificates and provisioning profiles are valid for more than 30 days.
```

##
Made with ❤️ for automation-loving iOS teams.
PRs, feedback, and forks are welcome!