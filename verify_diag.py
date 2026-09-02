import contextlib
import importlib.util
import io
import os
import sys
import traceback
from pathlib import Path

ROOT = Path(r"C:\Users\s8001\OneDrive\Desktop\Muve-fit\MuveFit--AI-Assist-Trainer")
LOG_PATH = ROOT / "verification_diag_log.txt"

checks = []


def record(label, fn):
    stream = io.StringIO()
    exc = None
    try:
        with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
            fn()
        checks.append((label, "PASS", stream.getvalue().strip()))
    except Exception as e:
        exc = traceback.format_exc()
        checks.append((label, "FAIL", (stream.getvalue() + "\n---EXCEPTION---\n" + exc).strip()))


def import_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_backend_imports():
    modules = [
        "backend.main",
        "backend.exercises.base",
        "backend.exercises.registry",
        "backend.exercises.squat",
        "backend.exercises.plank",
        "backend.exercises.burpee",
        "backend.exercises.squat_hold",
        "backend.exercises.glute_bridge",
    ]
    for module in modules:
        __import__(module)


def check_legacy_exercise_imports():
    files = [
        ROOT / "exercises" / "squat_test2.py",
        ROOT / "exercises" / "plank.py",
        ROOT / "exercises" / "burpee_test.py",
        ROOT / "exercises" / "squat_hold.py",
        ROOT / "exercises" / "glute_bridge.py",
    ]
    for p in files:
        import_module_from_path(f"legacy_{p.stem}", p)


def check_backend_exercise_registry():
    from backend.exercises.registry import get_exercise_analyzer
    for name in ["squat", "plank", "burpee", "squat_hold", "glute_bridge"]:
        analyzer = get_exercise_analyzer(name)
        print(name, type(analyzer).__name__)


def check_glute_bridge():
    from backend.exercises.glute_bridge import GluteBridgeAnalyzer
    analyzer = GluteBridgeAnalyzer()
    print("initial", analyzer.state)
    result = analyzer.analyze([
        {"x": 0.5, "y": 0.5, "z": 0.0},
        {"x": 0.6, "y": 0.4, "z": 0.0},
        {"x": 0.7, "y": 0.3, "z": 0.0},
    ] * 11)
    print(result)


def check_fastapi():
    from fastapi.testclient import TestClient
    from backend.main import app
    client = TestClient(app)
    res = client.get("/api/health")
    print(res.status_code)
    print(res.json())


def check_backend_pytest():
    import pytest
    raise SystemExit(0)


record("BACKEND_IMPORTS", check_backend_imports)
record("LEGACY_EXERCISE_IMPORTS", check_legacy_exercise_imports)
record("BACKEND_EXERCISE_REGISTRY", check_backend_exercise_registry)
record("GLUTE_BRIDGE_ANALYZER", check_glute_bridge)
record("FASTAPI_HEALTH", check_fastapi)

with LOG_PATH.open("w", encoding="utf-8") as fh:
    for label, status, output in checks:
        fh.write(f"=== {label} ===\n")
        fh.write(f"STATUS: {status}\n")
        fh.write(output)
        fh.write("\n\n")

print(f"WROTE {LOG_PATH}")
print(f"TOTAL_CHECKS {len(checks)}")
for label, status, output in checks:
    print(label, status)
