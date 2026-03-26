#!/usr/bin/env bash

set -u  # Exit on unbound variables

PYTHON="python3"
SIM="./cache_sim.py"
LINEAR_TRACE="linear.trace"
RANDOM_TRACE="random.trace"  # Renamed to avoid $RANDOM conflict
BLOCK_SIZE=64
CACHE_SIZE_BYTES=32768
TOTAL_BLOCKS=$((CACHE_SIZE_BYTES / BLOCK_SIZE))  # 512

# Verify files exist
echo "Checking trace files..."
[[ -f "$LINEAR_TRACE" ]] || { echo "ERROR: $LINEAR_TRACE not found!"; exit 1; }
[[ -f "$RANDOM_TRACE" ]] || { echo "ERROR: $RANDOM_TRACE not found!"; exit 1; }

echo "Files OK. Starting experiments..."

echo "=== Experiment A: Associativity Sensitivity ($RANDOM_TRACE) ==="

# Associativities: 1 (DM), 2-way, 4-way, 8-way, Fully Associative (512-way)
for ASSOC in 1 2 4 8 512; do
    SETS=$((TOTAL_BLOCKS / ASSOC))
    
    echo
    echo "=== A${ASSOC}: $RANDOM_TRACE | 32KB | 64B | ${ASSOC}-way | ${SETS} sets | NO prefetch ==="
    $PYTHON "$SIM" \
        --sets "$SETS" \
        --blocks "$ASSOC" \
        --size "$BLOCK_SIZE" \
        --trace "$RANDOM_TRACE"
done

echo
echo "=== Experiment B: Baseline vs Prefetch (32KB, 4-way) ==="

ASSOC=4
SETS=$((TOTAL_BLOCKS / ASSOC))  # 128 sets

for TRACE in "$LINEAR_TRACE" "$RANDOM_TRACE"; do
    echo
    echo "=== B1: $TRACE | Baseline LRU (NO prefetch) | 32KB | 4-way | ${SETS} sets ==="
    $PYTHON "$SIM" \
        --sets "$SETS" \
        --blocks "$ASSOC" \
        --size "$BLOCK_SIZE" \
        --trace "$TRACE"
    
    echo
    echo "=== B2: $TRACE | Prefetch ON | 32KB | 4-way | ${SETS} sets ==="
    $PYTHON "$SIM" \
        --sets "$SETS" \
        --blocks "$ASSOC" \
        --size "$BLOCK_SIZE" \
        --trace "$TRACE" \
        --prefetch
done

echo "=== Experiments complete! ==="

