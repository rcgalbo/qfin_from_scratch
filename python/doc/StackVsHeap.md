# Stack vs Heap in Python: The Complete Guide

A deep dive into Python's memory model, explaining what actually goes on the stack vs heap, and how it differs from languages like C++.

---

## Table of Contents

1. [The Fundamental Concepts](#the-fundamental-concepts)
2. [Python's Memory Model (CPython)](#pythons-memory-model-cpython)
3. [What Goes on the Stack in Python](#what-goes-on-the-stack-in-python)
4. [What Goes on the Heap in Python](#what-goes-on-the-heap-in-python)
5. [Frame Objects: Python's Call Stack](#frame-objects-pythons-call-stack)
6. [Python vs C++ Memory Comparison](#python-vs-c-memory-comparison)
7. [Memory Allocation Performance](#memory-allocation-performance)
8. [Common Misconceptions](#common-misconceptions)
9. [Advanced Topics](#advanced-topics)
10. [Interview Questions](#interview-questions)

---

## The Fundamental Concepts

### What is the Stack?

The **stack** is a region of memory that stores:
- Local variables (in C++)
- Function call information
- Return addresses
- Function parameters

**Key characteristics**:
- **Fast**: Allocation is just moving a pointer
- **Automatic**: Memory freed when function returns
- **Limited size**: Typically 1-8 MB
- **LIFO**: Last-In-First-Out (like a stack of plates)

```
Stack Layout (grows downward):
┌─────────────────┐  ← High memory
│  Function A     │
│  - local vars   │
│  - return addr  │
├─────────────────┤
│  Function B     │
│  - local vars   │
│  - return addr  │
├─────────────────┤
│  Function C     │
│  - local vars   │
│  - return addr  │
└─────────────────┘  ← Stack pointer (current top)
```

---

### What is the Heap?

The **heap** is a region of memory for dynamic allocation:
- Objects with unpredictable lifetime
- Data structures of variable size
- Anything that needs to outlive a function call

**Key characteristics**:
- **Slower**: Allocation requires finding free space
- **Manual/Managed**: Needs explicit management (or GC)
- **Large size**: Limited only by system RAM
- **Fragmented**: Can have holes/gaps

```
Heap Layout (conceptual):
┌─────────────────────────────┐
│ [Object A]  [Free]  [Obj B] │
│ [Free] [Object C] [Free]    │
│ [Object D] [Free] [Obj E]   │
└─────────────────────────────┘
  ↑ Managed by allocator/GC
```

---

## Python's Memory Model (CPython)

### The Big Surprise: Almost Everything is on the Heap!

**In Python, unlike C++:**
- The stack stores **references** (pointers), not actual objects
- Almost all objects live on the **heap**
- Even integers and small strings are heap-allocated

```python
def function():
    x = 42              # Integer object on HEAP
    name = "Alice"      # String object on HEAP
    items = [1, 2, 3]   # List object on HEAP
    
    # The STACK only stores:
    # - Reference to the integer
    # - Reference to the string
    # - Reference to the list
```

### Memory Layout Visualization

```
STACK (C Call Stack):           HEAP (Python Objects):
┌─────────────────────┐         ┌──────────────────────────┐
│ function() frame    │         │                          │
│ ┌─────────────────┐ │         │ PyLongObject(42)         │
│ │ x → 0x1000  ────┼─┼─────────┼→ ob_refcnt: 1           │
│ │ name → 0x2000 ──┼─┼─────────┼→ ob_type: &PyLong_Type  │
│ │ items → 0x3000 ─┼─┼─────────┼→ ob_digit: [42]         │
│ └─────────────────┘ │         │                          │
└─────────────────────┘         │ PyUnicodeObject("Alice") │
                                │ ob_refcnt: 1             │
                                │ ob_type: &PyUnicode_Type │
                                │ data: "Alice"            │
                                │                          │
                                │ PyListObject([1,2,3])    │
                                │ ob_refcnt: 1             │
                                │ ob_type: &PyList_Type    │
                                │ ob_item: [...]           │
                                └──────────────────────────┘
```

**Key Insight**: The stack holds **pointers**, the heap holds **objects**.

---

## What Goes on the Stack in Python

### 1. Function Call Frames

```python
import sys

def function_a():
    frame = sys._getframe()
    print(f"Frame: {frame}")
    print(f"Function name: {frame.f_code.co_name}")
    function_b()

def function_b():
    frame = sys._getframe()
    print(f"Frame: {frame}")
    print(f"Function name: {frame.f_code.co_name}")

function_a()
```

**Output**:
```
Frame: <frame at 0x..., file '...', line 4, code function_a>
Function name: function_a
Frame: <frame at 0x..., file '...', line 10, code function_b>
Function name: function_b
```

**What's on the stack**:
- Frame object pointers
- Return addresses
- Instruction pointers

---

### 2. Local Variable References (Pointers Only)

```python
def demo():
    # These are just POINTERS on the stack
    x = 42           # Stack: x → heap address
    y = "hello"      # Stack: y → heap address
    z = [1, 2, 3]    # Stack: z → heap address
    
    # The actual INTEGER, STRING, and LIST are on the heap!
```

**Stack contents**:
```
┌──────────────────┐
│ x: 0x7f9a12340  │ → Points to heap
│ y: 0x7f9a12400  │ → Points to heap
│ z: 0x7f9a12500  │ → Points to heap
└──────────────────┘
```

---

### 3. Function Parameters (References)

```python
def process(value, items):
    # 'value' and 'items' are references on the stack
    # pointing to heap objects
    pass

x = 42
lst = [1, 2, 3]
process(x, lst)  # Passes references, not copies
```

---

### 4. C-Level Data (CPython Internals)

Under the hood, CPython uses the C stack for:
- C function call frames
- C local variables
- Return addresses
- Register saves

```c
// CPython C code (simplified)
PyObject* PyNumber_Add(PyObject *v, PyObject *w) {
    // 'v' and 'w' are C pointers on the C stack
    PyObject *result;  // C local variable on C stack
    
    // But the objects they point to are on the heap
    result = do_add(v, w);  // Creates heap object
    return result;
}
```

---

## What Goes on the Heap in Python

### 1. All Python Objects

**Every Python object is heap-allocated**, including:

#### Integers (even small ones!)

```python
x = 42  # PyLongObject on heap

# Object structure (simplified):
struct PyLongObject {
    Py_ssize_t ob_refcnt;    // Reference count
    PyTypeObject *ob_type;    // Type pointer
    size_t ob_size;           // Number of digits
    digit ob_digit[1];        // Actual digits
};
```

#### Strings

```python
name = "Alice"  # PyUnicodeObject on heap

# Object structure (simplified):
struct PyUnicodeObject {
    Py_ssize_t ob_refcnt;
    PyTypeObject *ob_type;
    Py_ssize_t length;
    Py_hash_t hash;
    void *data;  // Actual string data
};
```

#### Lists, Tuples, Dicts

```python
items = [1, 2, 3]     # PyListObject on heap
coords = (10, 20)     # PyTupleObject on heap
mapping = {'a': 1}    # PyDictObject on heap
```

#### Functions and Classes

```python
def my_function():
    pass
# PyFunctionObject on heap!

class MyClass:
    pass
# PyTypeObject on heap!
```

---

### 2. Object Content and Buffers

```python
# Large list
large_list = [i for i in range(10000)]
# PyListObject header on heap
# Array of references on heap
# Each integer object on heap

# Large string
large_string = "x" * 10000
# PyUnicodeObject header on heap
# String buffer on heap
```

---

### 3. PyObject Headers

Every Python object starts with a header:

```c
typedef struct _object {
    Py_ssize_t ob_refcnt;      // 8 bytes on 64-bit
    struct _typeobject *ob_type;  // 8 bytes
    // ... then the actual data
} PyObject;
```

**Memory overhead example**:
```python
import sys

x = 42
print(sys.getsizeof(x))  # 28 bytes! (just for the integer 42)

# Breakdown:
# - ob_refcnt: 8 bytes
# - ob_type: 8 bytes
# - ob_size: 8 bytes
# - ob_digit: 4 bytes
# = 28 bytes total

# In C++: int x = 42;  // 4 bytes total!
```

---

## Frame Objects: Python's Call Stack

### Frame Object Structure

```python
import sys

def show_frame():
    frame = sys._getframe()
    
    print(f"Function: {frame.f_code.co_name}")
    print(f"Filename: {frame.f_code.co_filename}")
    print(f"Line number: {frame.f_lineno}")
    print(f"Local variables: {frame.f_locals}")
    print(f"Global variables: {list(frame.f_globals.keys())[:5]}")
    
show_frame()
```

**Output**:
```
Function: show_frame
Filename: script.py
Line number: 5
Local variables: {'frame': <frame object at 0x...>}
Global variables: ['__name__', '__doc__', '__package__', ...]
```

### Frame Objects are Heap-Allocated!

```python
def get_frame():
    return sys._getframe()

frame = get_frame()
# Frame object persists even after function returns!
# It's on the HEAP, not the stack

print(frame.f_code.co_name)  # 'get_frame'
```

**This is different from C++** where stack frames are destroyed on return.

---

### Call Stack Visualization

```python
def func_a():
    print("In func_a")
    func_b()

def func_b():
    print("In func_b")
    func_c()

def func_c():
    print("In func_c")
    import traceback
    traceback.print_stack()

func_a()
```

**Output**:
```
In func_a
In func_b
In func_c
  File "script.py", line 15, in <module>
    func_a()
  File "script.py", line 3, in func_a
    func_b()
  File "script.py", line 7, in func_b
    func_c()
  File "script.py", line 11, in func_c
    traceback.print_stack()
```

**Stack structure**:
```
┌────────────────────┐
│ <module> frame     │
├────────────────────┤
│ func_a() frame     │
├────────────────────┤
│ func_b() frame     │
├────────────────────┤
│ func_c() frame     │ ← Current
└────────────────────┘
```

---

## Python vs C++ Memory Comparison

### Example 1: Simple Variables

**Python**:
```python
def python_function():
    x = 42           # Integer OBJECT on heap (28 bytes)
    y = 3.14         # Float OBJECT on heap (24 bytes)
    z = "hello"      # String OBJECT on heap (54+ bytes)
    # Stack only holds 3 pointers (24 bytes total)
```

**Memory**:
```
Stack: 24 bytes (3 pointers)
Heap: 106+ bytes (objects)
Total: 130+ bytes
```

---

**C++**:
```cpp
void cpp_function() {
    int x = 42;           // On stack (4 bytes)
    double y = 3.14;      // On stack (8 bytes)
    std::string z = "hello";  // Object on stack (32 bytes)
                              // Small string optimization!
    // Total: 44 bytes on stack, 0 on heap
}
```

**Memory**:
```
Stack: 44 bytes
Heap: 0 bytes
Total: 44 bytes
```

**Difference**: C++ is 3x more memory efficient for simple values!

---

### Example 2: Arrays/Lists

**Python**:
```python
def python_array():
    arr = [1, 2, 3, 4, 5]
    # List object on heap
    # Each integer object on heap
    # Total: ~200+ bytes
```

**Memory breakdown**:
```
List object header: 64 bytes
Array of 5 pointers: 40 bytes
5 integer objects: 5 × 28 = 140 bytes
Total: 244 bytes
```

---

**C++**:
```cpp
void cpp_array() {
    std::array<int, 5> arr = {1, 2, 3, 4, 5};
    // Entire array on stack
    // Total: 20 bytes (5 × 4 bytes)
}
```

**Memory breakdown**:
```
5 integers contiguous: 20 bytes
Total: 20 bytes
```

**Difference**: Python uses 12x more memory!

---

### Example 3: Dynamic Allocation

**Python** (everything is dynamic):
```python
def python_dynamic():
    lst = []
    for i in range(1000):
        lst.append(i)  # All on heap
```

---

**C++** (explicit control):
```cpp
void cpp_dynamic() {
    // Stack allocation
    std::array<int, 1000> stack_arr;  // 4000 bytes on stack
    
    // Heap allocation
    std::vector<int> heap_vec;
    heap_vec.reserve(1000);  // Heap allocation
    for (int i = 0; i < 1000; i++) {
        heap_vec.push_back(i);
    }
}
```

**Key difference**: C++ lets you choose stack vs heap. Python doesn't.

---

## Memory Allocation Performance

### Benchmark: Stack vs Heap Allocation

**Python** (everything is heap):
```python
import time

def benchmark_allocation():
    start = time.perf_counter()
    for i in range(1000000):
        x = 42  # Heap allocation (but cached by CPython!)
    end = time.perf_counter()
    print(f"Python: {(end - start) * 1000:.2f} ms")

benchmark_allocation()
```

**Output**: ~50-100 ms

---

**C++** (stack vs heap):
```cpp
#include <chrono>
#include <iostream>
#include <memory>

void benchmark_stack() {
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 1000000; i++) {
        int x = 42;  // Stack allocation
    }
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "C++ stack: " 
              << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() 
              << " μs\n";
}

void benchmark_heap() {
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 1000000; i++) {
        auto x = std::make_unique<int>(42);  // Heap allocation
    }
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "C++ heap: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() 
              << " ms\n";
}
```

**Output**:
```
C++ stack: 2 μs
C++ heap: 50 ms
```

**Performance comparison**:
- C++ stack: **2 microseconds** (fastest)
- C++ heap: **50 milliseconds** (25,000x slower than stack!)
- Python: **50-100 milliseconds** (everything is heap)

---

### Why Stack is Faster

```
Stack allocation:
    mov rsp, -8      // Just move stack pointer (1 instruction)
    // Done!

Heap allocation:
    call malloc      // Find free block
    update metadata  // Bookkeeping
    check alignment  // Ensure alignment
    return pointer   // Return to caller
    // Many instructions + potential system call
```

**Stack**: O(1) - Just increment pointer  
**Heap**: O(log n) or worse - Search for free block

---

## Common Misconceptions

### Misconception 1: "Small integers are on the stack"

```python
x = 42  # Is this on the stack?

# Answer: NO!
# Even small integers are heap-allocated PyLongObjects
# The REFERENCE to the object is on the stack
```

**Proof**:
```python
import sys

x = 42
print(f"Size: {sys.getsizeof(x)} bytes")  # 28 bytes
print(f"ID: {id(x)}")  # Memory address (on heap)
print(f"Type: {type(x)}")  # <class 'int'>
```

---

### Misconception 2: "Python has no stack"

```python
# Python DOES have a stack!
# But it stores references, not objects

def recursive(n):
    if n == 0:
        return
    recursive(n - 1)

recursive(10000)  # RecursionError: maximum recursion depth exceeded
# This is a STACK overflow!
```

Python's stack is used for:
- Function call frames
- Return addresses
- Local variable references

---

### Misconception 3: "del frees memory immediately"

```python
x = [1, 2, 3] * 1000000  # Large list on heap
del x  # Does this free memory?

# Answer: MAYBE!
# If refcount = 0, yes (immediate)
# If refcount > 0, no (still referenced)
```

**Example**:
```python
x = [1, 2, 3]
y = x
del x  # Doesn't free memory (y still references it)
del y  # NOW memory is freed
```

---

### Misconception 4: "Stack size doesn't matter in Python"

```python
def deep_recursion(n):
    if n == 0:
        return
    deep_recursion(n - 1)

deep_recursion(1000)    # OK
deep_recursion(10000)   # RecursionError!

# Each call adds a frame to the stack
# Python's default recursion limit: 1000
```

**Check/modify limit**:
```python
import sys
print(sys.getrecursionlimit())  # 1000
sys.setrecursionlimit(10000)    # Increase (careful!)
```

---

## Advanced Topics

### 1. Small Integer Caching

Python caches integers from -5 to 256:

```python
a = 100
b = 100
print(a is b)  # True - same object!
print(id(a) == id(b))  # True - same memory address

a = 1000
b = 1000
print(a is b)  # False - different objects
print(id(a) == id(b))  # False - different addresses
```

**Why?** Performance optimization - small integers used frequently.

---

### 2. String Interning

Python interns some strings:

```python
a = "hello"
b = "hello"
print(a is b)  # True - interned

a = "hello world!"
b = "hello world!"
print(a is b)  # False - not interned (contains space)

# Force interning
import sys
a = sys.intern("hello world!")
b = sys.intern("hello world!")
print(a is b)  # True - now interned
```

---

### 3. Memory Pools (pymalloc)

Python uses **memory pools** for small objects (< 512 bytes):

```
Arena (256 KB)
├── Pool 1 (4 KB) - for 8-byte blocks
│   ├── Block (8 bytes)
│   ├── Block (8 bytes)
│   └── ...
├── Pool 2 (4 KB) - for 16-byte blocks
│   ├── Block (16 bytes)
│   ├── Block (16 bytes)
│   └── ...
└── ...
```

**Benefits**:
- Fast allocation (no malloc call)
- Reduced fragmentation
- Better cache locality

---

### 4. Stack Overflow vs Out of Memory

**Stack Overflow** (too much recursion):
```python
def infinite():
    infinite()

infinite()  # RecursionError: maximum recursion depth exceeded
```

**Out of Memory** (too many heap objects):
```python
huge_list = []
for i in range(10**10):
    huge_list.append([0] * 1000000)
# MemoryError: (eventually)
```

---

### 5. Viewing Memory Usage

```python
import sys
import tracemalloc

# Start tracking
tracemalloc.start()

# Allocate some memory
x = [i for i in range(100000)]
y = {i: i**2 for i in range(10000)}

# Get current memory usage
current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024:.2f} MB")
print(f"Peak: {peak / 1024 / 1024:.2f} MB")

# Get top allocations
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("\nTop 3 allocations:")
for stat in top_stats[:3]:
    print(stat)

tracemalloc.stop()
```

---

## Interview Questions

### Q1: What's stored on the stack vs heap in Python?

**Answer**:
"In Python, the stack stores function call frames and local variable **references** (pointers), while almost all actual objects live on the heap. This is different from languages like C++ where you can allocate simple types directly on the stack.

For example:
```python
def function():
    x = 42  # Reference on stack, PyLongObject on heap
```

The stack holds a pointer to the heap-allocated integer object. This design allows Python's dynamic typing and reference counting to work consistently. The trade-off is more memory overhead compared to stack allocation, but it provides flexibility for Python's dynamic features."

---

### Q2: Why is stack allocation faster than heap allocation?

**Answer**:
"Stack allocation is faster because it's just a pointer increment/decrement operation - O(1) with a single CPU instruction. The stack pointer always points to the next free space.

Heap allocation is slower because it requires:
1. Searching for a free block of appropriate size
2. Updating metadata (free lists, size information)
3. Potentially merging/splitting blocks
4. Possibly calling the OS for more memory

In C++, I've measured stack allocation being 25,000x faster than heap allocation in tight loops. Python doesn't give you the choice - everything goes on the heap - but it uses memory pools (pymalloc) to make small object allocation faster."

---

### Q3: Can you cause a stack overflow in Python?

**Answer**:
"Yes! Python maintains a call stack for function frames, and you can overflow it with deep recursion:

```python
def recursive(n):
    return recursive(n - 1)

recursive(1000000)  # RecursionError
```

Python's default recursion limit is 1000 (configurable with `sys.setrecursionlimit()`). Each function call adds a frame to the stack, and too many nested calls exhaust the stack space. This is why Python has a recursion limit - to prevent actual C stack overflow crashes.

However, you can't overflow the stack by creating too many objects - those go on the heap and would cause a MemoryError instead."

---

### Q4: How does Python's integer caching work?

**Answer**:
"CPython caches integer objects from -5 to 256 because they're used frequently. Instead of creating new PyLongObject instances every time, it reuses pre-allocated ones:

```python
a = 100
b = 100
print(a is b)  # True - same object

a = 1000
b = 1000
print(a is b)  # False - different objects
```

This optimization saves memory and allocation time. The cached integers are created at interpreter startup and persist for the entire program. It's similar to string interning but automatic for this specific range."

---

### Q5: What's the memory overhead of Python objects?

**Answer**:
"Every Python object has significant overhead due to the PyObject header. For example:

```python
import sys
x = 42
print(sys.getsizeof(x))  # 28 bytes
```

That's 28 bytes just to store the integer 42! The breakdown:
- ob_refcnt: 8 bytes (reference count)
- ob_type: 8 bytes (type pointer)
- ob_size: 8 bytes (variable size)
- ob_digit: 4+ bytes (actual integer data)

In C++, `int x = 42;` would be just 4 bytes. This overhead is the price Python pays for dynamic typing, reference counting, and object-oriented features. For numerical computing, this is why NumPy stores arrays of primitive types without the PyObject wrapper."

---

### Q6: Explain Python's memory pools (pymalloc)

**Answer**:
"Python uses a custom memory allocator called pymalloc for objects smaller than 512 bytes. It organizes memory into:

1. **Arenas**: 256 KB chunks from the OS
2. **Pools**: 4 KB chunks from arenas
3. **Blocks**: Fixed-size chunks from pools

When you create a small object, Python:
1. Finds a pool with the right block size
2. Returns a block from that pool (fast!)
3. No need to call malloc/free repeatedly

Benefits:
- Faster allocation than malloc
- Reduced memory fragmentation
- Better cache locality

For objects ≥ 512 bytes, Python uses the system allocator directly. This two-tier approach balances performance for small objects (common) with simplicity for large objects."

---

### Q7: How do closures affect memory?

**Answer**:
"Closures keep objects alive on the heap even after their defining scope exits:

```python
def make_counter():
    count = 0  # Would normally be freed when function returns
    
    def increment():
        nonlocal count
        count += 1
        return count
    
    return increment  # Returns closure

counter = make_counter()
# 'count' object still alive! Captured by closure
```

The closure maintains a reference to `count`, preventing it from being garbage collected. You can inspect this:

```python
print(counter.__closure__)  # (<cell at 0x...>,)
print(counter.__closure__[0].cell_contents)  # 0
```

This is why closures can cause memory leaks if you're not careful - they keep all captured variables alive indefinitely."

---

### Q8: Compare memory usage: Python vs C++

**Answer**:
"Python uses significantly more memory than C++ for several reasons:

**Example - storing 1 million integers:**

Python:
```python
arr = [i for i in range(1000000)]
# List object: 64 bytes
# Pointer array: 8 MB
# Integer objects: 28 MB (28 bytes each)
# Total: ~36 MB
```

C++:
```cpp
std::vector<int> arr(1000000);
// Vector object: 24 bytes
// Integer array: 4 MB (4 bytes each)
// Total: ~4 MB
```

Python uses 9x more memory! This is because:
1. Every integer is a PyObject with overhead
2. Lists store pointers, not values
3. Everything is heap-allocated

For numerical computing, use NumPy which stores primitive types without PyObject wrappers, matching C++ efficiency."

---

## Summary: Key Takeaways

### Python's Memory Model

1. **Stack**: Stores references (pointers) and call frames
2. **Heap**: Stores all Python objects
3. **Everything is an object**: Even integers are heap-allocated
4. **Reference counting**: Controls object lifetime
5. **Garbage collection**: Handles circular references

### Performance Implications

- **Memory overhead**: ~28 bytes minimum per object
- **Allocation speed**: All heap (slower than stack)
- **Memory pools**: Optimize small object allocation
- **Caching**: Small integers and strings optimized

### Compared to C++

| Aspect | Python | C++ |
|--------|--------|-----|
| **Stack** | References only | Values or references |
| **Heap** | All objects | Explicit (new/delete) |
| **Control** | Automatic | Manual (RAII) |
| **Overhead** | High (~28+ bytes) | Low (0-8 bytes) |
| **Speed** | Slower | Faster |
| **Flexibility** | High (dynamic) | Lower (static) |

---

## Visual Summary

```
PYTHON MEMORY MODEL:

╔══════════════════════╗     ╔═══════════════════════════╗
║   STACK (Small)      ║     ║   HEAP (Large)            ║
╠══════════════════════╣     ╠═══════════════════════════╣
║ Function Frames      ║     ║ PyLongObject(42)          ║
║ ┌──────────────────┐ ║     ║   ob_refcnt: 1            ║
║ │ x → 0x1000 ──────┼─╬─────╬→ ob_type: <int>           ║
║ │ y → 0x2000 ──────┼─╬───┐ ║   ob_digit: [42]          ║
║ │ z → 0x3000 ──────┼─╬─┐ │ ║                           ║
║ └──────────────────┘ ║ │ │ ║ PyUnicodeObject("hi")     ║
║                      ║ │ └─╬→ ob_refcnt: 1             ║
║ Return Addresses     ║ │   ║   data: "hi"              ║
║ Instruction Pointers ║ │   ║                           ║
║                      ║ └───╬→ PyListObject([...])      ║
╚══════════════════════╝     ║   ob_refcnt: 1            ║
                             ║   ob_items: [...]         ║
                             ╚═══════════════════════════╝

C++ MEMORY MODEL (for comparison):

╔══════════════════════╗     ╔═══════════════════════════╗
║   STACK (Larger)     ║     ║   HEAP (Only if needed)   ║
╠══════════════════════╣     ╠═══════════════════════════╣
║ int x = 42           ║     ║ new int(42) ──┐           ║
║ [42] (4 bytes)       ║     ║   [42]        │           ║
║                      ║     ║               │           ║
║ double y = 3.14      ║     ║ (Only explicit)           ║
║ [3.14] (8 bytes)     ║     ║  allocations)             ║
║                      ║     ╚═══════════════════════════╝
║ std::string z = "hi" ║
║ [ptr to data]        ║
║ [size: 2]            ║
║ [capacity: 15]       ║
║ ["hi\0..."] (SSO)    ║
╚══════════════════════╝
```

---

## Additional Resources

- [CPython Memory Management](https://docs.python.org/3/c-api/memory.html)
- [Python Memory Model](https://realpython.com/python-memory-management/)
- [Understanding Python Bytecode](https://docs.python.org/3/library/dis.html)
- [CPython Internals](https://github.com/python/cpython)

---

**Bottom Line**: In Python, the stack is for **references** (pointers), and the heap is for **objects** (everything else). This design enables Python's dynamic features but comes with memory and performance costs compared to languages with stack allocation like C++.