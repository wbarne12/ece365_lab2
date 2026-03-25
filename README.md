# ece365_lab2
To run: "python3 cache_sim.py --sets SETS --blocks BLOCKS --size SIZE --trace TRACE"

## Arg description
Sets        (int): Number of sets in the cache.  
Size        (int): Block size in bytes.  
Trace (file name): File with memory addresses in hex.  
Blocks      (int): Number of blocks per set  (associativity).  
    *If blocks=1, the cache will be direct mapped*  

## File requirements
For the program to properly run, each memory address must be in hex format ie 0x1234ABCD.  
Each address must be seperated by a new line character. Look at test.txt for an example.
