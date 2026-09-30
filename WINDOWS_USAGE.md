# VargaMesh BasicSwap - Windows x64

This package provides a Windows x64 build of the VargaMesh-enabled
BasicSwap fork.

Native Windows support is currently experimental.

## Included

- basicswap-prepare.exe
- basicswap-run.exe

## Requirement: GnuPG

BasicSwap uses GnuPG to verify downloaded core binaries.

Before the first setup, open Command Prompt as Administrator and run:

    winget install --id GnuPG.GnuPG --exact

After installation, completely close Command Prompt and open it again.

Verify GnuPG:

    gpg --version
    where gpg

Both commands should work before continuing.

## First-time setup

Extract the complete ZIP file.

Open Command Prompt inside the extracted folder.

Example:

    cd C:\Users\<Username>\Desktop\VargaMesh-BasicSwap-Windows-x64-v0.18.9-vmesh.2

Then run:

    basicswap-prepare.exe

The default BasicSwap data directory is:

    C:\Users\<Username>\.basicswap

Wait until preparation has completed.

The setup may display wallet recovery information or a mnemonic.

Keep all recovery information private and store it securely.

Never share:

- seed phrases
- mnemonics
- private keys
- WIF keys
- extended private keys
- RPC passwords
- wallet files

## Starting BasicSwap

After preparation has completed successfully, run:

    basicswap-run.exe

Keep the program running.

Then open this address in your browser:

    http://127.0.0.1:12700

## Existing installation

If this file already exists:

    C:\Users\<Username>\.basicswap\basicswap.json

you normally do not need to run the initial preparation again.

Start BasicSwap with:

    basicswap-run.exe

## Settings file not found

If basicswap-run.exe reports:

    Settings file not found

run:

    basicswap-prepare.exe

first.

## GPG error

If preparation reports:

    Unable to run gpg

install GnuPG:

    winget install --id GnuPG.GnuPG --exact

Close and reopen Command Prompt afterwards.

Verify:

    gpg --version
    where gpg

Then retry:

    basicswap-prepare.exe

## VargaMesh Core

VargaMesh support is integrated into this BasicSwap fork.

VargaMesh Core itself is currently provided separately.
Automatic VargaMesh Core provisioning is not enabled yet.

VargaMesh:

https://vargacoin.com

VargaMesh Core:

https://github.com/ati1993de/vargamesh-core

BasicSwap VargaMesh fork:

https://github.com/ati1993de/basicswap-vmesh

## Security

The BasicSwap web interface should normally remain local at:

    127.0.0.1:12700

Do not expose the BasicSwap web interface directly to the public internet.

BasicSwap is non-custodial.
Users remain responsible for protecting their own wallet recovery data.


## Using an existing VargaMesh Desktop node

On Windows, VargaMesh BasicSwap can use the VargaMesh Core node that is
already running as part of VargaMesh Desktop.

The default VargaMesh Desktop data directory is:

    %LOCALAPPDATA%\VargaMesh

When VargaMesh Desktop is running and this directory contains
`vargamesh.conf`, `.cookie`, and `vargameshd.pid`, BasicSwap detects it
automatically.

BasicSwap does not overwrite the VargaMesh Desktop configuration and does
not start or stop the VargaMesh Desktop node.

After the initial BasicSwap preparation, add VargaMesh with:

    basicswap-prepare.exe --addcoin=vargamesh --nocores

Then start BasicSwap with:

    basicswap-run.exe

VargaMesh Desktop should remain running while VMESH is used in BasicSwap.

BasicSwap creates its own `bsx_wallet` and `bsx_watch` wallets through the
existing local VargaMesh RPC connection. It does not require a second copy
of the VargaMesh blockchain.


## Automatic VargaMesh Desktop integration

On Windows, `basicswap-run.exe` automatically checks for VargaMesh Desktop.

When VargaMesh is not yet configured in BasicSwap, the launcher:

1. detects the VargaMesh Desktop data directory at `%LOCALAPPDATA%\VargaMesh`
2. checks whether the VargaMesh Desktop node is running
3. attempts to start VargaMesh Desktop when necessary
4. waits for the local VMESH RPC node
5. runs the VargaMesh add-coin setup automatically
6. reuses the existing VargaMesh Desktop blockchain
7. starts BasicSwap normally

BasicSwap does not replace or import the user's VargaMesh Desktop spending wallet.

Dedicated BasicSwap wallets such as `bsx_wallet` and `bsx_watch` are used for swap operations.

The VargaMesh Desktop node remains externally managed. Closing BasicSwap must not stop the VargaMesh Desktop node.

If VargaMesh Desktop is not installed or cannot be detected, BasicSwap continues without automatically enabling VMESH.
