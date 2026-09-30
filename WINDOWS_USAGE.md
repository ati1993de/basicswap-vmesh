# VargaMesh BasicSwap - Windows x64

This package provides a native Windows x64 build of the
VargaMesh-enabled BasicSwap fork.

Native Windows support is currently experimental.

## Included

- `basicswap-prepare.exe`
- `basicswap-run.exe`

## Recommended setup

For the easiest VMESH setup, install and run VargaMesh Desktop first.

BasicSwap can automatically reuse the local VargaMesh Desktop node,
blockchain and RPC connection.

Default VargaMesh Desktop data directory:

    %LOCALAPPDATA%\VargaMesh

A second copy of the VargaMesh blockchain is not required.

## 1. Verify the downloaded release

Download the Windows ZIP and `SHA256SUMS.txt` from the official
VargaMesh BasicSwap GitHub release.

Verify the ZIP before running it.

Example in PowerShell:

    Get-FileHash .\VargaMesh-BasicSwap-Windows-x64-<version>.zip -Algorithm SHA256

Compare the displayed SHA256 value with `SHA256SUMS.txt`.

Only continue when the checksum matches.

## 2. GnuPG requirement

BasicSwap uses GnuPG to verify downloaded core binaries.

Before the first setup, open Command Prompt or PowerShell as
Administrator and run:

    winget install --id GnuPG.GnuPG --exact

After installation, completely close the terminal and open it again.

Verify GnuPG:

    gpg --version
    where.exe gpg

Both commands should work before continuing.

## 3. Extract the complete ZIP

Extract the complete release ZIP to a normal local folder.

Example:

    C:\Users\<Username>\Desktop\VargaMesh-BasicSwap-Windows-x64-<version>

Do not run the executable directly from inside the ZIP archive.

## 4. Start VargaMesh Desktop

Start VargaMesh Desktop first.

If possible, wait until the VargaMesh node is running and synchronized.

BasicSwap normally detects:

    %LOCALAPPDATA%\VargaMesh

The launcher can also attempt to start VargaMesh Desktop automatically
when it is installed but not currently running.

Once detected, the VargaMesh node is treated as an externally managed
node. BasicSwap reuses it and does not require another VMESH blockchain.

## 5. First BasicSwap start

For the first start, right-click:

    basicswap-run.exe

and choose:

    Run as administrator

Keep the console window open.

The launcher automatically:

1. detects the VargaMesh Desktop installation
2. checks the local VargaMesh data directory
3. waits for the VMESH RPC service
4. configures VargaMesh in BasicSwap when necessary
5. uses `--addcoin=vargamesh --nocores`
6. reuses the existing VargaMesh Desktop node
7. starts the required BasicSwap components
8. starts the local BasicSwap web interface

The default BasicSwap data directory is:

    C:\Users\<Username>\.basicswap

## 6. The first start can take longer

The first BasicSwap start can take longer because the bundled Particl
node may need time to initialize.

Messages such as:

    Waiting for PART RPC. Trying again...

can be normal during startup and do not automatically mean that the
setup has failed.

Wait for the startup process to continue.

A successful startup should eventually contain messages similar to:

    Particl Core version ...
    VargaMesh Core version ...
    Starting HTTP server at http://127.0.0.1:12700

## 7. If the first attempt does not reach the web interface

In some Windows environments, the first launch may initialize the
required files and processes but the web interface may not become
available immediately.

If the first attempt does not complete:

1. allow the current startup attempt enough time to finish
2. close the BasicSwap launcher if it has stopped or clearly failed
3. do not leave multiple `basicswap-run.exe` instances running
4. wait approximately 15-30 seconds
5. make sure VargaMesh Desktop is still running
6. right-click `basicswap-run.exe`
7. choose `Run as administrator` again

A second launch can then reuse the Particl and BasicSwap files created
during the first attempt.

Do not repeatedly start several copies of BasicSwap at the same time.

## 8. Open BasicSwap

When startup has completed successfully, open:

    http://127.0.0.1:12700

The BasicSwap web interface should show both Particl and VargaMesh.

For VMESH, a healthy installation should show the VargaMesh wallet,
current blockchain height and synchronization status.

## 9. Expected VargaMesh startup messages

Typical successful VMESH messages include:

    [VMESH] Existing VargaMesh Desktop node detected:
    [VMESH] VargaMesh already configured.
    [VMESH] Reusing VargaMesh Desktop node.

and later:

    Reading VMESH rpc credentials from auth cookie
    VargaMesh Core version ...

The VargaMesh Desktop node remains externally managed.

Closing BasicSwap must not stop the VargaMesh Desktop node.

## 10. Dedicated BasicSwap VMESH wallets

BasicSwap does not replace or import the user's normal VargaMesh
Desktop spending wallet.

For swap operations, BasicSwap creates dedicated wallets such as:

    bsx_wallet
    bsx_watch

through the existing local VargaMesh RPC connection.

## 11. Existing BasicSwap installation

If this file already exists:

    C:\Users\<Username>\.basicswap\basicswap.json

you normally do not need to run the initial BasicSwap preparation again.

Start with:

    basicswap-run.exe

The launcher checks whether VargaMesh is already configured and reuses
the VargaMesh Desktop node automatically.

## 12. Manual VMESH setup fallback

Normally the automatic launcher is sufficient.

If automatic VMESH configuration is unavailable but VargaMesh Desktop
is already running, the manual fallback is:

    basicswap-prepare.exe --addcoin=vargamesh --nocores

Then start:

    basicswap-run.exe

Do not remove `--nocores` when the intention is to reuse the VargaMesh
Desktop node.

## 13. Settings file not found

If `basicswap-run.exe` reports:

    Settings file not found

the BasicSwap base installation may not have been initialized.

Run:

    basicswap-prepare.exe

and allow it to complete.

Then start:

    basicswap-run.exe

again.

## 14. GPG error

If preparation reports:

    Unable to run gpg

install GnuPG:

    winget install --id GnuPG.GnuPG --exact

Close and reopen Command Prompt or PowerShell afterwards.

Verify:

    gpg --version
    where.exe gpg

Then retry the BasicSwap setup.

## 15. Upstream update message

BasicSwap may display an update message for the upstream BasicSwap
project, for example:

    Update available: v0.18.10

The VargaMesh-enabled Windows package is a dedicated BasicSwap fork.

If VMESH integration is required, use releases from:

    https://github.com/ati1993de/basicswap-vmesh

Do not assume that replacing this package with an upstream BasicSwap
build will retain VargaMesh-specific integration.

## 16. Security

The BasicSwap web interface should normally remain local at:

    127.0.0.1:12700

Do not expose the BasicSwap web interface directly to the public
internet.

Running as Administrator is recommended here for the initial Windows
setup/troubleshooting only. Do not run unrelated or unverified
executables with elevated privileges.

Always verify the release SHA256 checksum before use.

BasicSwap is non-custodial.

Never share:

- seed phrases
- mnemonics
- private keys
- WIF keys
- extended private keys
- RPC passwords
- wallet files

Keep all wallet recovery information private and store it securely.

## Links

VargaMesh:

    https://vargacoin.com

VargaMesh Core:

    https://github.com/ati1993de/vargamesh-core

VargaMesh BasicSwap fork:

    https://github.com/ati1993de/basicswap-vmesh
