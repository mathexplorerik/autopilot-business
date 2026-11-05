"""
Run log (V16)
Saves everything a run prints (stdout and stderr) to output/logs/run_<time>.log
with colour codes removed, while still showing it on screen. Keeps the newest
logs only. If the log cannot be created, the run continues without one.
"""

import os
import re
import sys
import time

ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")

_state = {"path": None, "file": None, "stdout": None, "stderr": None}


class _Tee:
    def __init__(self, stream, log_file):
        self._stream = stream
        self._log = log_file

    def write(self, text):
        self._stream.write(text)
        try:
            self._log.write(ANSI.sub("", text))
            self._log.flush()
        except Exception:
            pass
        return len(text)

    def flush(self):
        self._stream.flush()
        try:
            self._log.flush()
        except Exception:
            pass

    def __getattr__(self, name):
        return getattr(self._stream, name)


def _prune(log_dir, keep):
    keep = max(keep, 0)
    names = sorted(n for n in os.listdir(log_dir) if n.startswith("run_") and n.endswith(".log"))
    old = names if keep == 0 else names[:-keep]
    for name in old:
        try:
            os.remove(os.path.join(log_dir, name))
        except OSError:
            pass


def start_run_log(log_dir="output/logs", keep=30, argv=None):
    if _state["file"] is not None:
        return _state["path"]
    try:
        os.makedirs(log_dir, exist_ok=True)
        _prune(log_dir, keep - 1)
        path = os.path.join(log_dir, "run_" + time.strftime("%Y%m%d_%H%M%S") + ".log")
        log_file = open(path, "a", encoding="utf-8")
    except Exception:
        return None

    log_file.write("# started " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    if argv:
        log_file.write("# command: " + " ".join(str(a) for a in argv) + "\n")
    log_file.flush()

    _state["path"] = path
    _state["file"] = log_file
    _state["stdout"] = sys.stdout
    _state["stderr"] = sys.stderr
    sys.stdout = _Tee(sys.stdout, log_file)
    sys.stderr = _Tee(sys.stderr, log_file)
    return path


def stop_run_log():
    path = _state["path"]
    if _state["file"] is None:
        return None
    sys.stdout = _state["stdout"]
    sys.stderr = _state["stderr"]
    try:
        _state["file"].close()
    except Exception:
        pass
    _state.update({"path": None, "file": None, "stdout": None, "stderr": None})
    return path
