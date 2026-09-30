from __future__ import annotations

import ctypes
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from basicswap.bin.run import main as run_main


def _argument_value(name: str) -> str | None:
    args = sys.argv[1:]

    for i, arg in enumerate(args):
        if arg.startswith(name + "="):
            return arg.split("=", 1)[1]

        if arg == name and i + 1 < len(args):
            return args[i + 1]

    return None


def _meta_invocation() -> bool:
    return any(
        arg in ("--help", "-h", "--version", "-v")
        for arg in sys.argv[1:]
    )


def _normal_path(value: str | Path) -> str:
    return os.path.normcase(
        os.path.abspath(
            os.path.expanduser(str(value))
        )
    )


def _desktop_data_dir() -> Path | None:
    local_app_data = os.getenv("LOCALAPPDATA", "").strip()

    if not local_app_data:
        return None

    return Path(local_app_data) / "VargaMesh"


def _read_pid(pid_file: Path) -> int | None:
    try:
        value = pid_file.read_text(
            encoding="utf-8"
        ).strip()

        pid = int(value)

        if pid <= 0:
            return None

        return pid
    except Exception:
        return None


def _process_running(pid: int | None) -> bool:
    if pid is None:
        return False

    if os.name != "nt":
        return False

    try:
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

        handle = ctypes.windll.kernel32.OpenProcess(
            PROCESS_QUERY_LIMITED_INFORMATION,
            False,
            pid,
        )

        if not handle:
            return False

        ctypes.windll.kernel32.CloseHandle(handle)
        return True
    except Exception:
        return False


def _desktop_node_ready(data_dir: Path) -> bool:
    if not data_dir.is_dir():
        return False

    required = (
        data_dir / "vargamesh.conf",
        data_dir / ".cookie",
        data_dir / "vargameshd.pid",
    )

    if not all(path.exists() for path in required):
        return False

    pid = _read_pid(data_dir / "vargameshd.pid")

    return _process_running(pid)


def _launch_vargamesh_desktop() -> bool:
    """
    Locate the installed VargaMesh Desktop Start-menu application
    and start it without depending on its WindowsApps version path.
    """

    powershell = (
        "$a = Get-StartApps | "
        "Where-Object { $_.Name -like '*VargaMesh*' } | "
        "Select-Object -First 1; "
        "if ($null -eq $a) { exit 2 }; "
        "$target = 'shell:AppsFolder\\' + $a.AppID; "
        "Start-Process explorer.exe -ArgumentList $target; "
        "exit 0"
    )

    try:
        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                powershell,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=20,
            check=False,
        )

        return result.returncode == 0
    except Exception:
        return False


def _wait_for_desktop_node(
    data_dir: Path,
    timeout: int = 90,
) -> bool:
    deadline = time.time() + timeout

    while time.time() < deadline:
        if _desktop_node_ready(data_dir):
            return True

        time.sleep(1)

    return False


def _ensure_desktop_node(data_dir: Path) -> bool:
    if _desktop_node_ready(data_dir):
        print(
            "[VMESH] Existing VargaMesh Desktop node detected:",
            data_dir,
        )
        return True

    print(
        "[VMESH] VargaMesh Desktop node is not running."
    )
    print(
        "[VMESH] Trying to start VargaMesh Desktop automatically..."
    )

    if not _launch_vargamesh_desktop():
        print(
            "[VMESH] VargaMesh Desktop could not be started automatically."
        )
        return False

    print(
        "[VMESH] Waiting for VargaMesh Desktop RPC..."
    )

    if not _wait_for_desktop_node(data_dir):
        print(
            "[VMESH] VargaMesh Desktop started, "
            "but its node did not become ready in time."
        )
        return False

    print(
        "[VMESH] VargaMesh Desktop node is ready."
    )
    return True


def _load_settings(settings_path: Path) -> dict:
    with settings_path.open(
        "r",
        encoding="utf-8",
    ) as fp:
        return json.load(fp)


def _rpc_port_from_conf(data_dir: Path) -> int:
    default_port = 29667
    conf = data_dir / "vargamesh.conf"

    try:
        for raw_line in conf.read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines():
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            if line.lower().startswith("rpcport="):
                return int(
                    line.split("=", 1)[1].strip()
                )
    except Exception:
        pass

    return default_port


def _prepare_executable() -> Path:
    candidate = Path(sys.executable).resolve().with_name(
        "basicswap-prepare.exe"
    )

    if not candidate.exists():
        raise RuntimeError(
            "basicswap-prepare.exe was not found next to "
            "basicswap-run.exe."
        )

    return candidate


def _run_vmesh_addcoin(
    basicswap_data_dir: Path,
    desktop_data_dir: Path,
) -> None:
    prepare_exe = _prepare_executable()

    rpc_port = _rpc_port_from_conf(
        desktop_data_dir
    )

    env = os.environ.copy()

    env["VMESH_DATA_DIR"] = str(
        desktop_data_dir
    )
    env["VMESH_RPC_HOST"] = "127.0.0.1"
    env["VMESH_RPC_PORT"] = str(rpc_port)

    command = [
        str(prepare_exe),
        f"--datadir={basicswap_data_dir}",
        "--addcoin=vargamesh",
        "--nocores",
    ]

    print()
    print(
        "[VMESH] VargaMesh is not configured in BasicSwap."
    )
    print(
        "[VMESH] Adding the existing VargaMesh Desktop node automatically..."
    )
    print(
        "[VMESH] Desktop data directory:",
        desktop_data_dir,
    )
    print(
        "[VMESH] RPC:",
        f"127.0.0.1:{rpc_port}",
    )
    print()

    result = subprocess.run(
        command,
        env=env,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Automatic VargaMesh BasicSwap setup failed "
            f"with exit code {result.returncode}."
        )

    settings_path = (
        basicswap_data_dir
        / "basicswap.json"
    )

    settings = _load_settings(
        settings_path
    )

    if (
        "vargamesh"
        not in settings.get(
            "chainclients",
            {},
        )
    ):
        raise RuntimeError(
            "VargaMesh setup finished but vargamesh "
            "is missing from basicswap.json."
        )

    print()
    print(
        "[VMESH] VargaMesh successfully added to BasicSwap."
    )
    print(
        "[VMESH] BasicSwap uses dedicated swap wallets "
        "and does not replace the VargaMesh Desktop wallet."
    )
    print()


def _bootstrap_windows_vmesh() -> None:
    if os.name != "nt":
        return

    if _meta_invocation():
        return

    requested_data_dir = _argument_value(
        "--datadir"
    )

    if requested_data_dir:
        basicswap_data_dir = Path(
            requested_data_dir
        ).expanduser()
    else:
        basicswap_data_dir = (
            Path.home()
            / ".basicswap"
        )

    settings_path = (
        basicswap_data_dir
        / "basicswap.json"
    )

    if not settings_path.exists():
        print(
            "[VMESH] BasicSwap has not been initialised yet."
        )
        print(
            "[VMESH] Run basicswap-prepare.exe once first."
        )
        print(
            "[VMESH] VMESH attachment will then be automatic "
            "on future basicswap-run.exe starts."
        )
        return

    settings = _load_settings(
        settings_path
    )

    chainclients = settings.get(
        "chainclients",
        {},
    )

    desktop_data_dir = _desktop_data_dir()

    if desktop_data_dir is None:
        return

    vmesh_settings = chainclients.get(
        "vargamesh"
    )

    if vmesh_settings is not None:
        configured_data_dir = vmesh_settings.get(
            "datadir",
            "",
        )

        uses_desktop_node = (
            vmesh_settings.get(
                "external_node",
                False,
            )
            and configured_data_dir
            and _normal_path(
                configured_data_dir
            )
            == _normal_path(
                desktop_data_dir
            )
        )

        if uses_desktop_node:
            if not _ensure_desktop_node(
                desktop_data_dir
            ):
                raise RuntimeError(
                    "VargaMesh is configured to use "
                    "VargaMesh Desktop, but the Desktop "
                    "node is unavailable."
                )

            print(
                "[VMESH] VargaMesh already configured."
            )
            print(
                "[VMESH] Reusing VargaMesh Desktop node."
            )

        return

    if not _ensure_desktop_node(
        desktop_data_dir
    ):
        print()
        print(
            "[VMESH] VargaMesh Desktop not available."
        )
        print(
            "[VMESH] Continuing BasicSwap without automatic "
            "VMESH activation."
        )
        print()
        return

    _run_vmesh_addcoin(
        basicswap_data_dir,
        desktop_data_dir,
    )


def main():
    try:
        _bootstrap_windows_vmesh()
    except SystemExit:
        raise
    except Exception as exc:
        print()
        print(
            "[VMESH] Automatic Windows integration failed:"
        )
        print(
            "[VMESH]",
            str(exc),
        )
        print()
        raise SystemExit(1)

    return run_main()


if __name__ == "__main__":
    main()
