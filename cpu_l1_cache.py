import struct
import math

class CacheLine:
    def __init__(self):
        self.tag = -1
        self.state = 'I'  # MESI: Modified, Exclusive, Shared, Invalid
        self.data = bytearray(64)  # 64 bytes
        self.last_accessed = 0
        self.dirty = False # Redundant with state='M', but kept for clarity

    def __repr__(self):
        return f"<CacheLine tag={self.tag} state={self.state} dirty={self.dirty}>"

class MainMemory:
    def __init__(self):
        self.storage = {}  # address (int) -> byte (int)

    def read(self, address, size):
        data = bytearray()
        for i in range(size):
            data.append(self.storage.get(address + i, 0))
        return data

    def write(self, address, data):
        for i, byte in enumerate(data):
            self.storage[address + i] = byte

    def __repr__(self):
        return f"<MainMemory bytes_used={len(self.storage)}>"

class L1Cache:
    def __init__(self):
        # Cache Specs
        self.cache_size = 32 * 1024  # 32 KB
        self.line_size = 64          # 64 Bytes
        self.associativity = 8       # 8-way
        self.num_sets = self.cache_size // (self.line_size * self.associativity) # 64 sets

        # Structure: List of Sets. Each Set is a list of CacheLines
        self.sets = [[CacheLine() for _ in range(self.associativity)] for _ in range(self.num_sets)]

        self.memory = MainMemory()

        # Time for LRU
        self.global_clock = 0

        # Statistics
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'write_backs': 0,
            'accesses': 0
        }

        # Visualization Data
        self.access_history = [] # List of boolean (True=Hit, False=Miss)
        self.access_counts = {} # Address -> Count

    def _get_addr_components(self, address):
        # Offset: log2(64) = 6 bits
        # Set Index: log2(64) = 6 bits
        # Tag: Remaining

        offset = address % self.line_size
        set_index = (address // self.line_size) % self.num_sets
        tag = address // (self.line_size * self.num_sets)
        return tag, set_index, offset

    def _find_line(self, set_index, tag):
        cache_set = self.sets[set_index]
        for i, line in enumerate(cache_set):
            if line.state != 'I' and line.tag == tag:
                return line
        return None

    def _get_victim(self, set_index):
        cache_set = self.sets[set_index]
        # First look for Invalid lines
        for line in cache_set:
            if line.state == 'I':
                return line

        # Use LRU
        victim = min(cache_set, key=lambda l: l.last_accessed)
        return victim

    def access(self, address, size, is_write, data=None):
        self.global_clock += 1
        self.stats['accesses'] += 1

        tag, set_index, offset = self._get_addr_components(address)

        # Track access count
        if address not in self.access_counts:
            self.access_counts[address] = 0
        self.access_counts[address] += 1

        # Check for Hit
        line = self._find_line(set_index, tag)

        if line:
            self.stats['hits'] += 1
            self.access_history.append(True) # Hit
            line.last_accessed = self.global_clock

            if is_write:
                # Write Hit
                # Update data in cache line
                for i, byte in enumerate(data):
                    line.data[offset + i] = byte

                # State transition
                if line.state == 'E':
                    line.state = 'M'
                    line.dirty = True
                elif line.state == 'M':
                    line.state = 'M' # Stays M
                    line.dirty = True
                # In single core, S state shouldn't happen essentially, but if it did: S->M
            else:
                # Read Hit
                # Return data
                return line.data[offset:offset+size]

        else:
            self.stats['misses'] += 1
            self.access_history.append(False) # Miss

            # Allocate a line (Evict if necessary)
            victim = self._get_victim(set_index)

            if victim.state == 'M':
                # Write Back
                self.stats['evictions'] += 1
                self.stats['write_backs'] += 1
                victim_addr = (victim.tag * self.num_sets * self.line_size) + (set_index * self.line_size)
                self.memory.write(victim_addr, victim.data)
            elif victim.state == 'E':
                 # Clean eviction
                 self.stats['evictions'] += 1

            # Load from Memory (RFO if write, Read if read)
            # In both cases we load the full 64B line
            block_start_addr = (address // self.line_size) * self.line_size
            block_data = self.memory.read(block_start_addr, self.line_size)

            # Install new line
            victim.tag = tag
            victim.data = block_data
            victim.last_accessed = self.global_clock

            if is_write:
                # Write Miss
                # Update the specific bytes
                for i, byte in enumerate(data):
                    victim.data[offset + i] = byte
                victim.state = 'M'
                victim.dirty = True
            else:
                # Read Miss
                victim.state = 'E' # Single core, exclusive
                victim.dirty = False
                return victim.data[offset:offset+size]

    def read_byte(self, address):
        res = self.access(address, 1, is_write=False)
        return res[0]

    def write_byte(self, address, val):
        self.access(address, 1, is_write=True, data=bytearray([val]))

    # Helper for SimulatedArray to read/write chunks
    def read(self, address, size):
        # We need to handle straddling cache lines?
        # For this MVP, assume aligned accesses or handle split
        # If access straddles, split it.
        result = bytearray()

        current_addr = address
        remaining_size = size

        while remaining_size > 0:
            offset = current_addr % self.line_size
            bytes_in_line = min(remaining_size, self.line_size - offset)

            chunk = self.access(current_addr, bytes_in_line, is_write=False)
            result.extend(chunk)

            current_addr += bytes_in_line
            remaining_size -= bytes_in_line

        return result

    def write(self, address, data):
        current_addr = address
        data_idx = 0
        remaining_size = len(data)

        while remaining_size > 0:
            offset = current_addr % self.line_size
            bytes_in_line = min(remaining_size, self.line_size - offset)

            chunk = data[data_idx : data_idx + bytes_in_line]
            self.access(current_addr, bytes_in_line, is_write=True, data=chunk)

            current_addr += bytes_in_line
            data_idx += bytes_in_line
            remaining_size -= bytes_in_line

class SimulatedArray:
    def __init__(self, cache_system: L1Cache, length, dtype='i', base_addr=None):
        self.cache = cache_system
        self.length = length
        self.dtype = dtype
        self.item_size = struct.calcsize(dtype)

        # Simple allocation strategy: If base_addr not provided, pick a random high one or increment
        # Ideally the cache system or memory should manage allocation.
        # Here we just assume a default if not given.
        if base_addr is None:
            # Check if cache has an allocator, otherwise use a static global counter on class or something
            # For now, start at 0x1000 and increment?
            # Let's just default to 0x1000 if user doesn't specify, but warn.
            # Ideally the user manages layout.
            self.base_addr = 0x1000
        else:
            self.base_addr = base_addr

    def _get_addr(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("SimulatedArray index out of range")
        return self.base_addr + (index * self.item_size)

    def __getitem__(self, index):
        addr = self._get_addr(index)
        data_bytes = self.cache.read(addr, self.item_size)
        return struct.unpack(self.dtype, data_bytes)[0]

    def __setitem__(self, index, value):
        addr = self._get_addr(index)
        data_bytes = struct.pack(self.dtype, value)
        self.cache.write(addr, data_bytes)

    def __len__(self):
        return self.length

    def __repr__(self):
        return f"<SimulatedArray size={self.length} type={self.dtype} base=0x{self.base_addr:x}>"
