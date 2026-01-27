# Architecture Specifications

## Capacity/Organization
*   **Capacity**: 32 KB
*   **Line Size**: 64 Bytes
*   **Associativity**: 8-way set associative
*   **Sets Calculation**: `32KB / (64B * 8) = 64 sets`
*   **Implementation**: The implementation correctly calculates `num_sets = 64`.

## Associativity
*   Implemented as a list of lists (Sets -> Ways), simulating 8-way associativity correctly.

## Line Size
*   64 Bytes supported via `bytearray(64)`.

## Policies
*   **Write-back**: Implemented correctly. Dirty lines ('M') are written to main memory upon eviction. Clean lines ('E') are just dropped.
*   **MESI**: While restricted to a single core (making 'Shared' state unreachable), the implementation correctly manages 'Exclusive' (clean, owned) and 'Modified' (dirty, owned) states and transitions (E->M on write).
*   **Replacement Policy**: Uses LRU (Least Recently Used) via a logical timestamp (`last_accessed`).

## Functionality
*   **Core Cache Logic**: The `access`, `read`, and `write` methods correctly handle hit/miss logic, address decomposition (Tag, Index, Offset), and data retrieval.
*   **Split Accesses**: The `read` and `write` methods in `L1Cache` correctly handle unaligned memory accesses that straddle two cache lines (e.g., writing a 4-byte integer at the end of a cache line), which is a common occurrence in x86 architectures.
*   **SimulatedArray**: The wrapper class successfully bridges Python's high-level operations (`__getitem__`, `__setitem__`) to the low-level memory/cache addresses using `struct` for data packing/unpacking.

## Verification
The included `verify_cache.py` provides excellent coverage:
*   **Spatial Locality**: Verifies that accessing sequential data pulls in full blocks (causing hits for subsequent bytes).
*   **Associativity & Eviction**: Uses a stride pattern to purposefully fill a specific set and force an eviction, verifying the LRU policy and write-back mechanism.
*   **Integrity**: Ensures data read back is the same as data written.
