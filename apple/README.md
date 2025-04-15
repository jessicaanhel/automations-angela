# 🍏 Apple Certificate & Provisioning Profile Expiry Notifier

This automation checks your Apple Developer **certificates** and **provisioning profiles** for upcoming expirations and sends a summary to **Slack**.

Ideal for teams who want proactive alerts before builds start failing due to expired assets.

---

## Features

- ✅ Checks all available Apple certificates and provisioning profiles
- 📅 Warns if anything expires within a configurable number of days (default: 30)
- 🔔 Sends a formatted Slack message with details
- 🔒 Uses App Store Connect API key (recommended for CI/CD and security)

---

## Prerequisites

- [Fastlane](https://docs.fastlane.tools/)
- Ruby installed (via Homebrew or rbenv)
- Slack Incoming Webhook URL
- App Store Connect API Key (downloaded `.json` file)

---

## App Store Connect API Key Setup

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

## To Run The Lane
1. Clone the repository
2. Navigate to the directory
3. Run the lane:
```bash
bundle exec fastlane check_expiry
```

## Slack Message Example
⚠️ Certificates/Profiles expiring soon:
🔐 Cert: iOS Distribution - Expires: 2025-04-30
📄 Profile: MyApp_Dev - Expires: 2025-04-25
