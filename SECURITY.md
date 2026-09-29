# Security

## Never commit secrets

Do not commit:

- wallet seed phrases or mnemonics
- private keys or WIF keys
- extended private keys
- RPC passwords
- API keys
- authentication cookies
- wallet files
- production configuration files

Use environment variables or local configuration files for credentials.

## Reporting security issues

Please do not disclose exploitable vulnerabilities publicly before they
have been reviewed and fixed.

## Non-custodial design

This project is intended to provide peer-to-peer, non-custodial atomic
swap software.

Users retain control of their own wallet keys and operate their own
wallet/node infrastructure.
