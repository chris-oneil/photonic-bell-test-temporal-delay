import sys
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
