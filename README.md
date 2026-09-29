# BasicSwap with VargaMesh (VMESH)

This repository is a VargaMesh-enabled fork of BasicSwap.

It adds support for **VargaMesh (VMESH)** to BasicSwap for peer-to-peer,
non-custodial atomic swaps.

## VargaMesh

- Symbol: `VMESH`
- Consensus: SHA-256d
- Architecture: Bitcoin-Core-derived UTXO blockchain
- Native SegWit
- Mainnet P2P: `29666`
- Mainnet RPC: `29667`
- Bech32 HRP: `vm`

VargaMesh website:

https://vargacoin.com

VargaMesh Core:

https://github.com/ati1993de/vargamesh-core

## BasicSwap integration

The integration includes:

- VMESH chain parameters
- VMESH RPC interface
- VMESH wallet support
- VMESH/BTC atomic swap support
- VMESH/PART atomic swap support
- BasicSwap order-book integration
- manual VMESH exchange-rate entry
- VMESH wallet balance support for modern Bitcoin-Core-derived RPC
- VMESH coin artwork

VargaMesh Core is currently expected to be provided separately.

Automatic VMESH Core downloading and signature retrieval are intentionally
not enabled yet.

## Non-custodial design

BasicSwap is designed for peer-to-peer atomic swaps.

Users retain control of their own private keys and wallets.

This repository does not contain production wallets, wallet seeds,
private keys, RPC credentials or server configuration.

## Security

Never commit:

- seed phrases
- private keys
- WIF keys
- extended private keys
- RPC passwords
- wallet files
- authentication cookies
- production configuration files

See [SECURITY.md](SECURITY.md).

## VargaMesh integration details

See [VARGAMESH.md](VARGAMESH.md).

## Upstream BasicSwap

This project is based on BasicSwap:

https://github.com/basicswap/basicswap

The original upstream README is preserved as:

[README.upstream.md](README.upstream.md)

## License

This project retains the upstream BasicSwap license.

See [LICENSE](LICENSE).

---

VargaMesh project:

https://vargacoin.com
