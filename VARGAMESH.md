# VargaMesh support for BasicSwap

This fork adds VargaMesh (VMESH) support to BasicSwap.

VargaMesh is a Bitcoin-Core-derived UTXO blockchain using SHA-256d and
native SegWit.

Project website:

https://vargacoin.com

VargaMesh Core source:

https://github.com/ati1993de/vargamesh-core

## Architecture

VMESH support is designed for peer-to-peer, non-custodial atomic swaps.

The software does not require custody of user funds.

Users operate their own wallets and retain their own private keys.

Offers are exchanged using BasicSwap's decentralized messaging system.

## Mainnet

VargaMesh mainnet:

- P2P: 29666
- RPC default: 29667
- Bech32 HRP: vm

Genesis block:

00000000b0c55c00c13e2ee67b54fe33c327c8806f8da5050cfa47095d182d9a

## Important

Never copy production RPC credentials, wallet files, private keys,
mnemonics or BasicSwap runtime data into this repository.

This repository contains software only.
