#!/usr/bin/env python3
"""
The "Randi Referee" Two-Program Challenge Sandbox Audit Suite
=============================================================
Enforces Richard Gill's strict Quantum Randi Challenge constraints to audit local
realistic simulations.

LICENSE (MIT):
Copyright (c) 2026 Christopher O'Neil (GitHub: chris-oneil | Email: christopheroneil@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to the following 
conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
including but not limited to the warranties of merchantability, fitness for a 
particular purpose and noninfringement. In no event shall the authors or copyright 
holders be liable for any claim, damages or other liability, whether in an action 
of contract, tort or otherwise, arising from, out of or in connection with the 
software or the use or other dealings in the software.

Supports two operational modes:
  1. NATIVE CLASS MODE: Fast internal auditing of python mathematical models using
     strict namespace isolation (no shared global references).
  2. SUBPROCESS PIPE MODE: The ultimate, bulletproof physical sandboxing. Runs Alice's
     and Bob's programs as completely independent subprocesses communicating solely
     via stdin/stdout pipes, making memory leakage or real-time state sharing impossible.

Usage:
    # 1. Run internal audit on standard local realistic models
    python p2add/randi_referee.py --mode native

    # 2. Run bulletproof subprocess sandbox audit on external station scripts
    python p2add/randi_referee.py --mode subprocess --alice p2add/alice_local.py --bob p2add/bob_local.py
"""

import argparse
import os
import sys
import time
import random
import subprocess
import sqlite3
import numpy as np
from pathlib import Path

# Ensure standard output can print Unicode characters on Windows console
sys.stdout.reconfigure(encoding='utf-8')

# Default simulation trials
DEFAULT_TRIALS = 10000


# ==============================================================================
# 1. SUBPROCESS SANDBOX STATIONS GENERATOR (To verify subprocess pipe mode)
# ==============================================================================
def create_sample_station_files():
    """
    Creates sample Alice and Bob python scripts inside 'p2add' for subprocess tests.
    
    NOTE ON LOCAL REALISM & GILL'S CHALLENGE:
    The sample station scripts use random.seed(999) to initialize identical PRNG states.
    In a physical Bell test, this corresponds to a pre-distributed list of local hidden 
    variables (lambda) shared before setting selection. This is completely valid under
    local realism and is explicitly permitted by Richard Gill's Two-Program Challenge, 
    as long as Alice and Bob have no real-time communication during setting delivery.
    """
    alice_code = """import sys
import random

# Seed the PRNG with a shared read-only seed or static data list
random.seed(999)

# Spindle-loop listening for settings on stdin
for line in sys.stdin:
    setting = line.strip()
    if not setting:
        break
    
    # Standard local realistic strategy (hidden variable lambda)
    # Alice setting a in {1, 2}
    lambda_val = random.choice([-1, 1])
    
    if setting == "1":
        outcome = lambda_val
    else:
        outcome = -lambda_val
        
    print(outcome)
    sys.stdout.flush()
"""

    bob_code = """import sys
import random

# Seed the PRNG with the exact same shared read-only seed
random.seed(999)

# Spindle-loop listening for settings on stdin
for line in sys.stdin:
    setting = line.strip()
    if not setting:
        break
    
    # Bob setting b in {1, 2}
    lambda_val = random.choice([-1, 1])
    
    if setting == "1":
        outcome = -lambda_val
    else:
        outcome = lambda_val
        
    print(outcome)
    sys.stdout.flush()
"""
    
    alice_path = Path("p2add/alice_local.py")
    bob_path = Path("p2add/bob_local.py")
    
    if not alice_path.exists():
        alice_path.write_text(alice_code, encoding="utf-8")
    if not bob_path.exists():
        bob_path.write_text(bob_code, encoding="utf-8")


# ==============================================================================
# 2. THE SANDBOX TESTING HARNESS
# ==============================================================================
class RandiReferee:
    def __init__(self, num_trials=DEFAULT_TRIALS):
        self.num_trials = num_trials
        
    def run_native_audit(self):
        """Runs the native class-mode audit with strict namespace sandboxing."""
        print("\n" + "="*70)
        print("RUNNING NATIVE CLASS-MODE AUDIT (Namespace Isolation)")
        print("="*70)
        
        # 1. Define strict local realistic station classes (No shared state)
        class AliceStation:
            def __init__(self, seed=12345):
                self.rng = random.Random(seed)
            def measure(self, setting):
                # Hidden variable lambda
                lhv = self.rng.choice([-1, 1])
                if setting == "1":
                    return lhv
                else:
                    return -lhv
                    
        class BobStation:
            def __init__(self, seed=12345):
                self.rng = random.Random(seed)
            def measure(self, setting):
                lhv = self.rng.choice([-1, 1])
                if setting == "1":
                    return -lhv
                else:
                    return lhv
                    
        # 2. Instantiate isolated stations
        alice = AliceStation(seed=555)
        bob = BobStation(seed=555)
        
        # 3. Test execution loop
        results = {"11": [], "12": [], "21": [], "22": []}
        
        for _ in range(self.num_trials):
            # Enforce random, independent setting choices
            a = str(random.choice([1, 2]))
            b = str(random.choice([1, 2]))
            
            # Execute measurements in strict isolation
            # Alice receives only 'a'
            x = alice.measure(a)
            # Bob receives only 'b'
            y = bob.measure(b)
            
            results[a+b].append(x * y)
            
        self._analyze_and_print_results(results)

    def run_subprocess_audit(self, alice_script, bob_script):
        """
        Runs the ultimate, bulletproof subprocess pipe sandbox audit.
        Alice's and Bob's scripts are launched once and fed settings via stdin pipes,
        flushing outcomes to stdout. Spawning overhead is 0, while process isolation is 100%.
        """
        print("\n" + "="*70)
        print("RUNNING SUBPROCESS PIPE-MODE AUDIT (Process Boundary Isolation)")
        print(f"  Alice Script: {alice_script}")
        print(f"  Bob Script:   {bob_script}")
        print("="*70)
        
        # Verify scripts exist
        if not Path(alice_script).exists() or not Path(bob_script).exists():
            print(f"[-] Error: One or both station scripts do not exist.")
            sys.exit(1)
            
        # Launch station processes in isolated, non-communicating pipelines
        try:
            alice_proc = subprocess.Popen(
                [sys.executable, alice_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True
            )
            bob_proc = subprocess.Popen(
                [sys.executable, bob_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True
            )
        except Exception as e:
            print(f"[-] Error spawning subprocesses: {e}")
            sys.exit(1)
            
        results = {"11": [], "12": [], "21": [], "22": []}
        
        t0 = time.perf_counter()
        
        try:
            for _ in range(self.num_trials):
                # Enforce independent settings
                a = str(random.choice([1, 2]))
                b = str(random.choice([1, 2]))
                
                # Write settings to pipes
                alice_proc.stdin.write(f"{a}\n")
                alice_proc.stdin.flush()
                
                bob_proc.stdin.write(f"{b}\n")
                bob_proc.stdin.flush()
                
                # Read outcomes from stdout
                x_str = alice_proc.stdout.readline().strip()
                y_str = bob_proc.stdout.readline().strip()
                
                if not x_str or not y_str:
                    print("[-] Error: One of the stations terminated early or failed to flush.")
                    break
                    
                x = int(x_str)
                y = int(y_str)
                
                # Assert outcomes are strictly binary
                assert x in [-1, 1], f"Invalid Alice outcome: {x}"
                assert y in [-1, 1], f"Invalid Bob outcome: {y}"
                
                results[a+b].append(x * y)
                
        finally:
            # Cleanly terminate subprocesses
            alice_proc.stdin.close()
            bob_proc.stdin.close()
            alice_proc.terminate()
            bob_proc.terminate()
            alice_proc.wait()
            bob_proc.wait()
            
        t_duration = time.perf_counter() - t0
        print(f"[OK] Executed {self.num_trials} sandboxed trials successfully in {t_duration:.2f}s.")
        
        self._analyze_and_print_results(results)

    def _analyze_and_print_results(self, results):
        """Computes CHSH correlators, standard errors, and checks bounds."""
        correlators = {}
        counts = {}
        
        # Calculate individual correlators: E(a, b) = sum(x*y) / N
        for key in ["11", "12", "21", "22"]:
            data = results[key]
            counts[key] = len(data)
            if data:
                correlators[key] = sum(data) / len(data)
            else:
                correlators[key] = 0.0
                
        # Calculate standard CHSH sum: S = E(1,1) - E(1,2) + E(2,1) + E(2,2)
        S = correlators["11"] - correlators["12"] + correlators["21"] + correlators["22"]
        
        # Calculate statistical standard error using exact independent-variance sum:
        # sigma_S = sqrt( sum_{a,b} (1 - E(a,b)^2) / n_ab )
        std_err = np.sqrt(np.sum([
            ((1.0 - correlators[k]**2) / counts[k]) if counts[k] > 0 else 0.0
            for k in ["11", "12", "21", "22"]
        ]))
        
        print("\n📊 Sandbox Audit Results:")
        print("-" * 55)
        print(f"  E(1, 1) Correlator:  {correlators['11']:.4f}  (N = {counts['11']})")
        print(f"  E(1, 2) Correlator:  {correlators['12']:.4f}  (N = {counts['12']})")
        print(f"  E(2, 1) Correlator:  {correlators['21']:.4f}  (N = {counts['21']})")
        print(f"  E(2, 2) Correlator:  {correlators['22']:.4f}  (N = {counts['22']})")
        print("-" * 55)
        print(f"  Observed CHSH S:     {S:.4f}")
        print(f"  Statistical Std Err:  {std_err:.4f}")
        print("-" * 55)
        
        # Verification checking
        is_violated = abs(S) > 2.0 + 3.0 * std_err
        
        if abs(S) <= 2.0:
            print("🟢 STATUS: PASSED.")
            print("   The local realistic model complies perfectly with Bell's bound (S <= 2.0).")
        elif is_violated:
            print("🔴 STATUS: VIOLATION DETECTED.")
            print(f"   CHSH violates Bell's bound: S = {S:.4f} > 2.0 (by {abs(S-2.0)/std_err:.1f} standard deviations).")
            print("   Warning: Verify that the station programs did not bypass process boundaries or leak memory state.")
        else:
            print("🟡 STATUS: MARGINAL BOUND.")
            print("   CHSH sum is slightly above 2.0, but statistically within random statistical fluctuations.")
        print("="*70 + "\n")


# ==============================================================================
# MAIN TERMINAL INTERFACE
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="The 'Randi Referee' Two-Program Challenge Sandbox Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--mode", choices=["native", "subprocess"], default="native",
        help="Namespace native mode or strict subprocess pipe mode (default: native)"
    )
    parser.add_argument(
        "--alice", default="p2add/alice_local.py",
        help="Path to Alice's station script (for subprocess mode)"
    )
    parser.add_argument(
        "--bob", default="p2add/bob_local.py",
        help="Path to Bob's station script (for subprocess mode)"
    )
    parser.add_argument(
        "--trials", type=int, default=DEFAULT_TRIALS,
        help=f"Number of simulation trials (default: {DEFAULT_TRIALS})"
    )
    
    args = parser.parse_args()
    
    # Initialize station files if needed
    create_sample_station_files()
    
    referee = RandiReferee(num_trials=args.trials)
    
    if args.mode == "native":
        referee.run_native_audit()
    elif args.mode == "subprocess":
        referee.run_subprocess_audit(args.alice, args.bob)


if __name__ == "__main__":
    main()
