# How to Design Tasks: Recursion, Map and Reduce

Last time we learned about list, set, and dictionary comprehensions. Today we are going to learn about the more general concept of **map**, **reduce** and **recursion** that drives it all.

These are core computer science concepts that are involved in processing any data structure that is more complex than the ones we have seen in class so far. We've had a taste of classes that make reference to other classes, but recursion is the idea of **self-reference**.

This can be considered a very philosophical idea. Many computer scientists treat self-reference and recursion as a nearly spiritual concept. I won't go into great detail for this class, but we'll look at it a bit for the lecture on sorting and complexity, and then in CPSC 121 a great deal more. 

Suggested reading is *Gödel, Escher, Bach: An Eternal Golden Braid* by famous Computer Scientist Douglas Hofstadter. 

## List comprehensions and mapping

Last time, we talked about list comprehensions:
```python
>>> nums = [1, 2, 3]
dbls = [2 * n for n in nums]
print(dbls)
[2, 4, 6]
```
I said that we **mapped** the function `2 * n` to the list `nums`. That means the function `2 * n` was applied to each number in the list.


### Map-Comprehension accumulator pattern

```python
# This code
dbls = [2 * n for n in nums]

# Is equivalent to this code
def doubleList(lon: List[int]) -> List[int]:
    acc = []
    for n in lon:
        acc.append(2 * n)
    return acc
dbls = doubleList([1, 2, 3])        
```

We can see from the above code that a list comprehension is just an accumulator pattern. Mapping is functionally equivalent.

### Map generalized equivalent code

```python
dlbs = [double(n) for n in nums]

def my_map(lon: List[int], fn_for_int) -> List[Int]:
    acc = []
    for n in lon:
        acc.append(fn_for_int(n))
    return acc

def double(n: int) -> int:
    return 2 * n
    
dbls = my_map([1, 2, 3], double)
```

### Why Map?
If we have a list comprehension, why define `my_map`? Two reasons:
- There are cases where the comprehension doesn't make sense
- Map works really well on massive datasets
- It's a general approach rather than a specific function

A toy example is included in `concurrent_map.py`. It shoes the time difference for calculating primes for each method.

## Exercise: Filter
Extend `my_map` to include a filter function, just like the list comprehensions have.

## Solution:
```python
def my_map(lon: List[int], fn_for_int, filter_for_int) -> List[int]:
    acc = []
    for n in lon:
        if filter_for_int(n):
            acc.append(fn_for_int(n))
    return acc
```

## Lambda: anonymous functions
Sometimes we want to call a small function without defining it. Here's an example of how we could call `my_map` with a filter and a `lambda` function:

```python
def my_map(lon: List[int], fn_for_int, filter_for_int) -> List[int]:
    acc = []
    for n in lon:
        if filter_for_int(n):
            acc.append(fn_for_int(n))
    return acc
my_map([1,2,3], lambda x: x *2, lambda x: x % 2 == 0)
```

### Built-in `map`, `filter` and `lambda`
Python has a built-in version of `map` and `filter` that can use anonymous `lambda` functions:
```python
>>> list(map(lambda x: x * 2, [1,2,3]))
[2, 4, 6]

>>> list(filter(lambda x: x % 2 == 1, [1,2,3]))
[1, 3]
```

The point of talking extensively about `map` is to get us thinking about lists more extensively. As we talked about in the lecture on iteration, many of the jobs we want to use computers for involve processing large lists of data. The transit dataset is one example, but many interesting problems, including AI, Machine Learning, and every database (which means most of the websites you know) use much, much longer lists.

### Built-in `reduce`
Python has a built-in version of `reduce`:
```python
from functools import reduce
>>> reduce(lambda acc, e: acc + e, [1,2,3], 0)
6
```

## Practicing `map`, `filter` and `reduce`
This is a new way of thinking. We're going to do some very basic operations with `map`, `filter`, `lambda` and `reduce` to get us thinking differently.

### Exercise: `map` and list comprehensions
First use a list comprehension, then `map` to square each number in a list of numbers, e.g.:
```python
>>> lon = [1, 2, 3]
>>> # your code
[1, 4, 9]
```


### Solution: `map` and list comprehensions
First use a list comprehension, then `map` to square a list of numbers.
```python
lon = [1, 2, 3]
sqr = [ n ** 2 for n in lon ]
msq = list(map( lambda n: n ** 2, lon ))
```

### Exercise: `filter` and list comprehensions
First use a list comprehension, then `filter` to filter out numbers smaller than 10 in a list of numbers, e.g.:
```python
>>> lon = [48, 2, 3, 49]
>>> # your code
[48, 49]
```


### Solution: `filter` and list comprehensions
First use a list comprehension, then `filter` to filter out numbers smaller than 10 in a list of numbers, e.g.:
```python
lon = [48, 2, 3, 49]
com = [ n for n in lon if n > 10 ]
flt = list(filter(lambda n: n > 10, lon))
```


### Exercise: multiply a list with `reduce`
Multiply every element of a list using `reduce`, e.g.:

```python
>>> lon = [1, 2, 3, 4]
>>> # your code
24
```


### Solution: multiply a list with `reduce`
Multiply every element of a list using `reduce`, e.g.:

```python
lon = [1, 2, 3, 4]
reduce(lambda acc, n: acc * n, lon, 1)
```

## Shapes: Using `map`, `filter` and `reduce` with Classes
Looking at our Translink data again, we can model the data in `shapes.txt` by the following:
```python
@dataclass
class Shape:
    id: str
    lat: gtfs.Latitude
    lon: gtfs.Longitude
    sequence: int
    dist_traveled: float
```
Run the parser in `shape_parser.py` and make a query to remind yourself of how this works.



### `map` to unpack `lat`
We can use `map` to unpack values very easily:
```python
shapes = gtfs.parse(lines[1:10], parse_row_to_shape)
lats = list(map(lambda s: s.lat, shapes))
```

### `filter` to choose values from `lat`
We can use `filter` to choose values very easily. Let's filter by distance:
```python
def dist(self, other: Self) -> float:
    dlat = abs(self.lat - other.lat)
    dlon = abs(self.lon - other.lon)
    dist = math.sqrt(dlat ** 2 + dlon ** 2)
    return dist

shapes = gtfs.parse(lines[1:], parse_row_to_shape)
lats = list(filter(lambda s: s.dist(shapes[0]) < 0.001, shapes))
```

### Exercise: Use `filter` to shapes with specific `id`s
We can use `filter` to choose values very easily. Filter shapes by `id`:
```python
shapes = gtfs.parse(lines[1:], parse_row_to_shape)
filtered = list(filter( ... )
```

### Solution: Use `filter` to shapes with specific `id`s
We can use `filter` to choose values very easily. Filter shapes by `id`:
```python
shapes = gtfs.parse(lines[1:], parse_row_to_shape)
filtered = list(filter(lambda s: s.id == shapes[0].id, shapes))
```

### `reduce` to find `Shape` with `max(dist_traveled)`
We can use `reduce` to unpack and find values very easily:
```python
from functools import reduce
shapes = gtfs.parse(lines[1:], parse_row_to_shape)
max_dt = reduce(lambda acc, s: acc if acc.dist_traveled > s.dist_traveled else s, shapes, shapes[0])
```

## Linked Lists: When basic Lists aren't Enough
When we make a list, each element in the list doesn't "know" about the next element. That is, the `1`, `2`, and `3` in `[1, 2, 3]` don't have a reference to each other, the list has a reference to each of them.

For some data structures, it is useful to have references to others of the same data structure. For the transit data, we saw that with `stop_id`. Some `Stop`s could make explicit reference to other `Stop`s.

We are goign to do the same with `shapes.txt`. Each `Shape` is just a point that a bus drives along. Together they make the shape of a route. 

Let's see how we can accurately model the distance along a route.

### Shapes that buses travel along
If you look at `shapes.txt`, you'll see that each `shape` has a sequence number:

```python
...,shape_pt_sequence,shape_dist_traveled
```
But the actual data is partially out of order:

```python
...
292022,49.257645,-123.17228,1,0
292022,49.262254,-123.168244,10,0.8022
...
292022,49.269247,-123.168254,19,1.5818
292022,49.257617,-123.170389,2,0.1377
292022,49.270144,-123.16822,20,1.6816
```


### Parsing Shapes with `next`
When we parse `shape`s, we will want to define a concept of `next`. A simplified `shape` data definition could look like:
```python
class Shape:
    id: str
    lat: gtfs.Latitude
    lon: gtfs.Longitude
    sequence: int
    dist_traveled: float
    # Reference to next shape
    next: Self | None
```
This means that each `Shape` can have a reference to another `Shape`.

### Toy Shapes 
Let's see how we would make some `Shape`s like this.
```python
shape_1 = Shape("000", 49.0, -123.0, 1, 0, None)
shape_2 = Shape("001", 49.1, -123.1, 2, 0, shape_1)
shape_3 = Shape("002", 49.2, -123.2, 3, 0, shape_2)
```


### Distance to Next Shape
If we wanted to calculate the distance to the next shape, we could implement a distance function like this:

```python
    def dist_next(self) -> float:
        if self.next != None:
            return self.dist(self.next)
        return 0.0
```

### Distance to Last Shape
If we wanted to calculate the distance to the last shape, we could implement a distance function like this:

```python
    def dist_end(self) -> float:
        if self._next == None:
            return 0.0
        return self.dist_next() + self._next.dist_end()
```

### Recursion: Break it Down
Let's break down this function piece by piece:
```python
    def dist_end(self) -> float:  # signature
        if self._next == None:    # base case
            return 0.0
        return self.dist_next() + self._next.dist_end() # recursive step
```

The **signature** is normal, but note that it will operate on types of itself.

The **base case** is what happens when there's nothing **next**. Every recursive function should be getting closer to the end of a data structure on each call, just like list iteration.

The **recursive step** calculates a value for *this* object and combines it with the value for the *rest* of the objects.

## Generalizing Linked Lists
Linked Lists are a type general **data structure** that is used in many applications. The general form uses a **Node**:

```python
@dataclass
class Node:
    data: Any
    next: Self
```
We can store any type of data in the `data` field, and then store a reference to the next `Node` in the `next` field.

### Constructing Linked Nodes
Think of Linked Lists like a chain of nodes:

```python
n0 = Node(0, None)
n1 = Node(1, n0)
n2 = Node(2, n1)
n3 = Node(3, n2)
```

### Exercise: Define recursive `sum` for Nodes where `data: int`
1. Write a signature (+ purpose, examples, etc.) like normal.
2. *Base case*: figure out what happens at the end of the list, i.e., `n0`.
3. *Recursive step*: figure out what happens at each link.

```python
n0 = Node(0, None)
n1 = Node(1, n0)
n2 = Node(2, n1)
n3 = Node(3, n2)
```

### Solution: Define recursive `sum` for Nodes where `data: int`

```python
def sum(n: Node) -> int:
    """
    Purpose: Adds a linked list of nodes.
    Example: 
        n0 = Node(0, None)
        n1 = Node(1, n0)
        n2 = Node(2, n1)
        n3 = Node(3, n2)
        sum(n3) -> 3 + 2 + 1 + 0 == 6
    """
    # Base case
    if n.next == None:
        return n.data
    else: # Recursive step
        return n.data + sum(n.next)
```
