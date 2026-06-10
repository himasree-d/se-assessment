"""
Data Structures & Systems Design — SE Intern Assignment
Author: Himasree Dintakurthy
"""

import threading
import heapq
from typing import Optional


# =============================================================================
# Problem 1: LRU Cache
# =============================================================================

class Node:
    """Doubly linked list node storing a key-value pair."""
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None


class LRUCache:
    """
    Least Recently Used Cache with O(1) get and put.

    Uses a hash map for O(1) key lookup and a doubly linked list to maintain
    usage order. The list is arranged most-recent → least-recent (head → tail).
    Sentinel head and tail nodes eliminate edge-case checks on empty lists.

    Args:
        capacity: Maximum number of items the cache can hold.

    Raises:
        ValueError: If capacity is not a positive integer.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Cache capacity must be a positive integer.")
        self.capacity = capacity
        self.cache: dict[int, Node] = {}

        # Sentinel nodes — never hold real data
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """Unlink a node from its current position in the list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_at_front(self, node: Node) -> None:
        """Insert a node immediately after the head sentinel (most recent)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        """
        Return the value for key, or -1 if not present.
        Marks the key as most recently used.

        Time: O(1)  Space: O(1)
        """
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._insert_at_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        """
        Insert or update key-value pair.
        Evicts the least recently used item if at capacity.

        Time: O(1)  Space: O(1) amortized
        """
        if key in self.cache:
            self._remove(self.cache[key])

        node = Node(key, value)
        self.cache[key] = node
        self._insert_at_front(node)

        if len(self.cache) > self.capacity:
            lru = self.tail.prev          # node just before tail sentinel
            self._remove(lru)
            del self.cache[lru.key]


class ThreadSafeLRUCache(LRUCache):
    """
    Thread-safe extension of LRUCache using a read-write aware lock strategy.

    A single threading.Lock is used here for correctness. In a higher-throughput
    system this could be replaced with a readers-writer lock (e.g. via
    threading.RLock + condition variables) since get() is logically read-only
    except for the usage-order update — but that update still mutates shared
    state, so a plain lock is correct and safe here.
    """

    def __init__(self, capacity: int):
        super().__init__(capacity)
        self._lock = threading.Lock()

    def get(self, key: int) -> int:
        with self._lock:
            return super().get(key)

    def put(self, key: int, value: int) -> None:
        with self._lock:
            super().put(key, value)


# =============================================================================
# Problem 2: Event Scheduler
# =============================================================================

def can_attend_all(events: list[tuple[int, int]]) -> bool:
    """
    Return True if a single person can attend all events without overlap.

    Adjacent events (end == start) are not considered overlapping per spec.
    Sorts by start time and tracks the furthest end time seen so far —
    this handles cases where an earlier event spans across multiple later ones.

    Time: O(n log n)  Space: O(1)
    """
    if not events:
        return True

    events_sorted = sorted(events, key=lambda x: x[0])
    max_end = events_sorted[0][1]

    for i in range(1, len(events_sorted)):
        start, end = events_sorted[i]
        if start < max_end:
            return False
        max_end = max(max_end, end)

    return True


def min_rooms_required(events: list[tuple[int, int]]) -> int:
    """
    Return the minimum number of rooms needed to host all events concurrently.

    Uses a two-pointer sweep over sorted start and end times.
    At each step: if the next meeting starts before any ongoing one ends,
    a new room is needed. Otherwise an existing room is freed.

    Time: O(n log n)  Space: O(n)
    """
    if not events:
        return 0

    starts = sorted(e[0] for e in events)
    ends = sorted(e[1] for e in events)

    rooms = max_rooms = 0
    s = e = 0

    while s < len(events):
        if starts[s] < ends[e]:
            rooms += 1
            max_rooms = max(max_rooms, rooms)
            s += 1
        else:
            rooms -= 1
            e += 1

    return max_rooms


def assign_rooms(events: list[tuple[int, int]]) -> list[tuple[tuple[int, int], str]]:
    """
    Assign named rooms (Room 1, Room 2, ...) to each event.

    Uses a min-heap keyed by event end time to always free the earliest-ending
    room first. A pool of available room names is maintained; when a room
    becomes free, its name is returned to the pool.

    Returns a list of (event, room_name) pairs in the order events were assigned.

    Time: O(n log n)  Space: O(n)

    Example:
        >>> assign_rooms([(9, 10), (9, 11), (10, 12)])
        [((9, 10), 'Room 1'), ((9, 11), 'Room 2'), ((10, 12), 'Room 1')]
    """
    if not events:
        return []

    # Sort events by start time; preserve original reference for output
    indexed = sorted(enumerate(events), key=lambda x: x[1][0])

    room_counter = 0
    available: list[str] = []          # pool of freed room names
    active: list[tuple[int, str]] = [] # min-heap of (end_time, room_name)
    assignment: list[tuple[tuple[int, int], str]] = [None] * len(events)  # type: ignore

    for orig_idx, (start, end) in indexed:
        # Free rooms whose meetings have ended before this one starts
        while active and active[0][0] <= start:
            freed_end, freed_room = heapq.heappop(active)
            available.append(freed_room)

        # Assign a room
        if available:
            room = available.pop()
        else:
            room_counter += 1
            room = f"Room {room_counter}"

        heapq.heappush(active, (end, room))
        assignment[orig_idx] = (events[orig_idx], room)

    return assignment


# =============================================================================
# Quick smoke tests
# =============================================================================

if __name__ == "__main__":
    # --- LRU Cache ---
    print("=== LRU Cache ===")
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))    # 1
    cache.put(3, 3)        # evicts key 2
    print(cache.get(2))    # -1
    cache.put(4, 4)        # evicts key 1
    print(cache.get(1))    # -1
    print(cache.get(3))    # 3
    print(cache.get(4))    # 4

    # --- Event Scheduler ---
    print("\n=== Event Scheduler ===")
    e1 = [(9, 10), (10, 11), (11, 12)]
    print(can_attend_all(e1))          # True — adjacent, not overlapping

    e2 = [(9, 11), (10, 12)]
    print(can_attend_all(e2))          # False

    e3 = [(9, 10), (9, 11), (10, 12)]
    print(min_rooms_required(e3))      # 2

    e4 = [(1, 10), (2, 3), (4, 12)]
    print(min_rooms_required(e4))      # 2 — (2,3) ends before (4,12) starts, so max concurrent is 2

    # --- Room Assignment ---
    print("\n=== Room Assignment ===")
    for event, room in assign_rooms(e3):
        print(f"  {event} → {room}")

    # --- Thread Safety (basic check) ---
    print("\n=== Thread Safety ===")
    ts_cache = ThreadSafeLRUCache(3)
    threads = []
    for i in range(10):
        t = threading.Thread(target=lambda i=i: ts_cache.put(i, i * 2))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("Thread-safe writes completed without error.")
