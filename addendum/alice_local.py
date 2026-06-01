import sys
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
