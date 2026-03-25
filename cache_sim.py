import argparse
import sys
import math

# Returns a list with all values formatted as ints
# Conversion from hex to int performed
def read_file(trace: str) -> list:
    with open(trace, "r") as file:
        return [int(line.strip(), 16) for line in file]

# Reads the command line and puts args into respective data section.
# Will handle all the wacky stuff that goes on with arg parsing.
def parse_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description ="A program to simulate a cache.")

    # TODO: Add --policy or --prefetch. Will depend on what we choose to implement.
    parser.add_argument("--sets", type=int, required=True)
    parser.add_argument("--blocks", type=int, required=True)
    parser.add_argument("--size", type=int, required=True)
    parser.add_argument("--trace", type=str, required=True)

    return parser.parse_args()

#https://www.geeksforgeeks.org/dsa/program-to-find-whether-a-given-number-is-power-of-2/
def is_power_of_two(n) -> bool:
    return (n > 0) and ((n & (n - 1)) == 0)

# Just checks if args are a power of two
def error_check(args: argparse.Namespace):
    power_two: bool = is_power_of_two(args.sets) & is_power_of_two(args.size) & is_power_of_two(args.blocks)
    if (not power_two):
        sys.exit("Error: Arguments are not a power of two.")

# A bit extractor, pass the indecies you want to excract and the address
# returns only the part of the address between those indecies
def bits(addr: int, start: int, stop: int) -> int:
    #"""Extract bits [start:stop] from addr (stop exclusive, 0 = LSB)."""
    k = stop - start        # number of bits to grab
    mask = (1 << k) - 1     # e.g., 0b1111 for k=4
    return (addr >> start) & mask


# Main execution
if (__name__ == "__main__"):
    args: argparse.Namespace = parse_args()
    error_check(args)

    sets:   int = args.sets
    blocks: int = args.blocks
    size:   int = args.size 
    trace:  str = args.trace
    total_blocks: int = sets * blocks
    cache_size: int = total_blocks * size

    offset_bits = int(math.log2(size))
    index_bits = int(math.log2(sets))
    tag_bits = 32 - index_bits - offset_bits

    address_list: list = read_file(trace)


    print("-------------------Addresses------------------")
    for addr in address_list:
        index_pos = offset_bits + index_bits
        tag_pos = index_pos + tag_bits

        bin_offset = bits(addr,0,offset_bits)
        bin_index = bits(addr,offset_bits,index_pos)
        bin_tag = bits(addr,index_pos,tag_pos)

        print(f"{addr:#010x}  {addr:032b}")
        print("offset:",f"{bin_offset:0{offset_bits}b}")
        print("index:",f"{bin_index:0{index_bits}b}")
        print("tag:",f"{bin_tag:0{tag_bits}b}")
        print()
    print("----------------------------------------------")


    print("sets,blocks,size,trace,total_blocks,cache_size");
    print(sets,blocks,size,trace,total_blocks,cache_size);

    print("tag,index,offset");
    print(tag_bits,index_bits,offset_bits);
    
    

    # cache[index] = [tag1, tag2, tag3 ... ]
    # Not storing actual data since it's just a sim
    cache = [ [] for _ in range(sets) ]




    accesses = 5
    hits = 4
    misses = 3
    misrate = 2
    print(f"{'Accesses:':<12}{accesses:>10}")
    print(f"{'Hits:':<12}{hits:>10}")
    print(f"{'Misses:':<12}{misses:>10}")
    print(f"{'Miss Rate:':<12}{misrate:>10}%")
