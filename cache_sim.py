from collections import deque
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

    parser.add_argument("--sets", type=int, required=True)
    parser.add_argument("--blocks", type=int, required=True)
    parser.add_argument("--size", type=int, required=True)
    parser.add_argument("--trace", type=str, required=True)
    parser.add_argument("--prefetch", action='store_true')

    return parser.parse_args()

#https://www.geeksforgeeks.org/dsa/program-to-find-whether-a-given-number-is-power-of-2/
def is_power_of_two(n) -> bool:
    return (n > 0) and ((n & (n - 1)) == 0)

# Just checks if args are a power of two
def error_check(args: argparse.Namespace):
    power_two: bool = is_power_of_two(args.sets) & is_power_of_two(args.size) & is_power_of_two(args.blocks)
    if (not power_two):
        sys.exit("Error: Arguments are not a power of two.")

# A bit extractor, pass the indecies you want to extract and the address
# returns only the part of the address between those indecies
def bits(addr: int, start: int, stop: int) -> int:
    k = stop - start        # number of bits to grab
    mask = (1 << k) - 1     # e.g., 0b1111 for k=4
    return (addr >> start) & mask

# Prints out all of the address, and the way they break up into the cache
def address_log(fd,address_list, offset_bits, index_bits, tag_bits, sets, blocks, size, total_blocks, cache_size):
    print(sys.argv, file=fd)
    print(file=fd)
    print("-------------------Addresses------------------", file=fd)
    for addr in address_list:
        bin_offset = bits(addr,0,offset_bits)
        bin_index = bits(addr,offset_bits,offset_bits+index_bits)
        bin_tag = bits(addr,offset_bits+index_bits,32)

        print(f"{addr:#010x}  {addr:032b}", file=fd)
        print("offset:",f"{bin_offset:0{offset_bits}b}", file=fd)
        print("index:",f"{bin_index:0{index_bits}b}", file=fd)
        print("tag:",f"{bin_tag:0{tag_bits}b}", file=fd)
        print(file=fd)
    print("----------------------------------------------", file=fd)
    print("sets:", sets, "| blocks:",blocks, "| size:", size, "| total_blocks:", total_blocks, "| cache_size:", cache_size, file=fd)
    print("tag:",tag_bits, "bits | index:",index_bits,"bits | offset:", offset_bits, "bits", file=fd)

# Main execution
if (__name__ == "__main__"):
    args: argparse.Namespace = parse_args()
    error_check(args)

    # Set all of the parsed command line args
    sets:   int = args.sets
    blocks: int = args.blocks
    size:   int = args.size 
    trace:  str = args.trace
    prefetch: bool = args.prefetch
    total_blocks: int = sets * blocks
    cache_size: int = total_blocks * size

    # calculate the size of each part of the cache
    offset_bits = int(math.log2(size))
    index_bits = int(math.log2(sets))
    tag_bits = 32 - index_bits - offset_bits

    address_list: list = read_file(trace)

    # Generate log file for address,
    logging = open("temp.log", "w")
    address_log(logging, address_list, offset_bits, index_bits, tag_bits, sets, blocks, size, total_blocks, cache_size)
    logging.close()
    
    # cache[index] = [tag1, tag2, tag3 ... tagSize]
    cache = [deque(maxlen=blocks) for _ in range(sets) ]

    hits:   int = 0
    misses: int = 0

    #iterates through all addresses and caches them
    for i in address_list:
        offset: int = bits(i, 0, offset_bits)
        index:  int = bits(i, offset_bits, offset_bits + index_bits)
        tag:    int = bits(i, offset_bits + index_bits, 32)

        if (tag in cache[index]): # Hit
            hits += 1
            cache[index].remove(tag) # make it recently used
            cache[index].append(tag)

        else: # Miss
            misses += 1
            if len(cache[index]) >= blocks:
                cache[index].popleft()
            cache[index].append(tag)

        if(prefetch): # Adds prefetching
            next_addr = i + size
            next_index = bits(next_addr, offset_bits, offset_bits + index_bits)
            next_tag   = bits(next_addr, offset_bits + index_bits, 32)
            if next_tag not in cache[next_index]:
                if len(cache[next_index]) >= blocks:
                    cache[next_index].popleft()
                cache[next_index].append(next_tag)


    accesses = hits + misses
    misrate = (misses/accesses) * 100
    print(f"{'Accesses:':<12}{accesses:>10}")
    print(f"{'Hits:':<12}{hits:>10}")
    print(f"{'Misses:':<12}{misses:>10}")
    print(f"{'Miss Rate:':<12}{misrate:>10.3f}%")
