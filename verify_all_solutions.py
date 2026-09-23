import os
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(r"D:\works\paper-lang-dist")
SOLUTIONS_DIR = WORKSPACE / "solutions_v1.5"
PROBLEMS_DIR = WORKSPACE / "problem_v1.5"

PROBLEMS = ["LC_0338", "IPOP_9012", "LC_0283", "LC_0053", "LC_0547"]
LANGUAGES = ["cpp", "c", "python", "java", "haskell", "erlang", "ocaml"]

def normalize_text(text: str) -> str:
    lines = [line.rstrip() for line in text.strip().splitlines()]
    return "\n".join(lines)

def run():
    total_passed = 0
    total_tested = 0
    failures = []

    build_dir = WORKSPACE / ".verify_build"
    build_dir.mkdir(exist_ok=True)

    for prob in PROBLEMS:
        print(f"=== Testing Problem: {prob} ===", flush=True)
        prob_sol_dir = SOLUTIONS_DIR / prob
        prob_eval_dir = PROBLEMS_DIR / prob / "evaluation"
        testcases = sorted(prob_eval_dir.glob("case*.inp"))

        # Pre-compile C++
        cpp_exe = build_dir / f"{prob}_cpp.exe"
        cmd = ["clang++", "-O2", str(prob_sol_dir / "solution.cpp"), "-o", str(cpp_exe)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"C++ build error for {prob}: {res.stderr}", flush=True)
            failures.append((prob, "cpp", "build_error", res.stderr))

        # Pre-compile C
        c_exe = build_dir / f"{prob}_c.exe"
        cmd = ["clang", "-O2", str(prob_sol_dir / "solution.c"), "-o", str(c_exe)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"C build error for {prob}: {res.stderr}", flush=True)
            failures.append((prob, "c", "build_error", res.stderr))

        # Pre-compile Java
        java_class_dir = build_dir / f"{prob}_java"
        java_class_dir.mkdir(exist_ok=True)
        cmd = ["javac", "-encoding", "UTF-8", "-d", str(java_class_dir), str(prob_sol_dir / "Main.java")]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Java build error for {prob}: {res.stderr}", flush=True)
            failures.append((prob, "java", "build_error", res.stderr))

        for lang in LANGUAGES:
            lang_passed = 0
            for tc in testcases:
                total_tested += 1
                out_path = tc.with_suffix(".out")
                expected = normalize_text(out_path.read_text(encoding="utf-8"))
                inp_text = tc.read_text(encoding="utf-8")

                if lang == "cpp":
                    run_cmd = [str(cpp_exe)]
                elif lang == "c":
                    run_cmd = [str(c_exe)]
                elif lang == "python":
                    run_cmd = [sys.executable, str(prob_sol_dir / "solution.py")]
                elif lang == "java":
                    run_cmd = ["java", "-cp", str(java_class_dir), "Main"]
                elif lang == "haskell":
                    run_cmd = ["runghc", str(prob_sol_dir / "solution.hs")]
                elif lang == "erlang":
                    run_cmd = ["escript", str(prob_sol_dir / "solution.erl")]
                elif lang == "ocaml":
                    run_cmd = ["ocaml", str(prob_sol_dir / "solution.ml")]

                try:
                    proc = subprocess.run(
                        run_cmd,
                        input=inp_text,
                        capture_output=True,
                        text=True,
                        timeout=10,
                    )
                    actual = normalize_text(proc.stdout)
                    if proc.returncode == 0 and actual == expected:
                        lang_passed += 1
                        total_passed += 1
                    else:
                        print(f"FAILED: {prob} | {lang} | {tc.name}", flush=True)
                        print(f"Return code: {proc.returncode}", flush=True)
                        print(f"Stderr: {proc.stderr[:200]}", flush=True)
                        print(f"Expected: {repr(expected[:60])}", flush=True)
                        print(f"Actual:   {repr(actual[:60])}", flush=True)
                        failures.append((prob, lang, tc.name, proc.stderr))
                except subprocess.TimeoutExpired:
                    print(f"TIMEOUT: {prob} | {lang} | {tc.name}", flush=True)
                    failures.append((prob, lang, tc.name, "timeout"))

            print(f"  [{lang}] {lang_passed}/{len(testcases)} passed", flush=True)

    print("\n=================================", flush=True)
    print(f"Total passed: {total_passed}/{total_tested}", flush=True)
    if failures:
        print(f"Failures count: {len(failures)}", flush=True)
        for f in failures:
            print(f"  FAIL: {f}", flush=True)
    else:
        print("ALL TESTS PASSED SUCCESSFULLY! 100% SUCCESS RATE", flush=True)
    print("=================================", flush=True)

if __name__ == "__main__":
    run()
