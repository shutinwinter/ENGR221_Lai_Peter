"""
Author: Peter Lai
FileName: randomWalker.py
Description
Assignment adapted from HMC CS5
"""

import random
import time

def rs():
    """rs chooses a random step and returns it.
       Note that a call to rs() requires parentheses.
       Arguments: none at all!
    """
    return random.choice([-1, 1])

def rwpos(start, nsteps):
    """ rwpos models a random walker that
        * starts at the int argument, start
        * takes the int # of steps, nsteps
        
        rwpos returns the final position of the walker.
    """
    time.sleep(0.1)
    print('location is', start)
    if nsteps == 0:
        return start
    else:
        newpos = start + rs()  # make a single step
        return rwpos(newpos, nsteps - 1)

def rwsteps(start, low, hi):
    """ rwsteps models a random walker which
        * is currently at start
        * is in a walkway from low (usually 0) to hi (max location)
        
        rwsteps returns the # of steps taken
        when the walker reaches an edge
    """
    walkway = "_" * (hi - low)     # Build walkway
    S = (start - low)              # Walker's initial position
    
    walkway = walkway[:S] + "S" + walkway[S:]  # Put walker in place
    walkway = " " + walkway + " "              # Add padding with spaces
    
    print(walkway, "   ", start, low, hi)      # Show current state
    time.sleep(0.05)
    
    if start <= low or start >= hi:
        return 0
    else:
        newstart = start + rs()            # Random step forward/backward
        return 1 + rwsteps(newstart, low, hi)  # Add step to total count

def rwstepsLoop(start, low, hi):
    """ rwstepsLoop models a random walker like rwsteps but using a loop.
        * starts at 'start'
        * in a walkway from 'low' to 'hi'
        Returns the number of steps taken when walker reaches an edge.
    """
    if start <= low or start >= hi:
        # Boundary check
        walkway = "_" * (hi - low)
        S = max(min(start - low, hi - low), 0)  # Keep walker position valid
        walkway = walkway[:S] + "S" + walkway[S:]
        walkway = " " + walkway + " "
        print(walkway, "   ", start, low, hi)
        return 0
    
    steps = 0
    current = start
    
    while low < current < hi:
        walkway = "_" * (hi - low)
        S = current - low
        walkway = walkway[:S] + "S" + walkway[S:]
        walkway = " " + walkway + " "
        print(walkway, "   ", current, low, hi)
        time.sleep(0.05)
        current += rs()
        steps += 1
    
    # Display final position
    walkway = "_" * (hi - low)
    S = max(min(current - low, hi - low), 0)
    walkway = walkway[:S] + "S" + walkway[S:]
    walkway = " " + walkway + " "
    print(walkway, "   ", current, low, hi)
    
    return steps

if __name__ == "__main__":
    print(rs())