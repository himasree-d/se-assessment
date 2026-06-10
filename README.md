# SE Intern Assessment — Data Structures & Systems Design

Solutions for the Software Engineering Intern take-home assessment covering LRU Cache implementation and an Event Scheduler.

## Contents

| File | Description |
|---|---|
| `solution.py` | All implementations — LRU Cache, Thread-Safe Cache, Event Scheduler, Room Assigner |
| `submission.pdf` | Full written submission with approach explanations, complexity analysis, and discussion |

## Problems Solved

**Problem 1 — LRU Cache**
- `LRUCache` — O(1) get and put via hash map + doubly linked list with sentinel nodes
- `ThreadSafeLRUCache` — extends LRUCache with a threading.Lock; includes notes on lock-striping for higher throughput

**Problem 2 — Event Scheduler**
- `can_attend_all(events)` — returns True if a single attendee can attend all events without overlap
- `min_rooms_required(events)` — two-pointer sweep over sorted start/end times to find peak concurrency
- `assign_rooms(events)` — bonus: assigns named rooms (Room 1, Room 2, ...) to each event using a min-heap

## How to Run

Python 3.10 or higher required. No external dependencies.

```bash
python3 solution.py
```

Expected output:

```
=== LRU Cache ===
1
-1
-1
3
4

=== Event Scheduler ===
True
False
2
2

=== Room Assignment ===
  (9, 10) → Room 1
  (9, 11) → Room 2
  (10, 12) → Room 1

=== Thread Safety ===
Thread-safe writes completed without error.
```

## Complexity Summary

| Function | Time | Space |
|---|---|---|
| `LRUCache.get()` | O(1) | O(1) |
| `LRUCache.put()` | O(1) | O(1) |
| `can_attend_all()` | O(n log n) | O(1) |
| `min_rooms_required()` | O(n log n) | O(n) |
| `assign_rooms()` | O(n log n) | O(n) |
