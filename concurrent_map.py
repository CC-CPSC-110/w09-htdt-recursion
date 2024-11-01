from typing import List
import multiprocessing
import time

# Function to check if a number is prime
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Define custom mapping functions for comparison
def prime_list(lon: List[int]) -> List[bool]:
    return [is_prime(n) for n in lon]

def my_map(lon: List[int], fn_for_int) -> List[bool]:
    return [fn_for_int(n) for n in lon]

if __name__ == "__main__":
    # Generate a list of large numbers to test
    nums = list(range(10**7, 10**7 + 1000000))  # 10,000 numbers to check

    # 1. Timing the list comprehension
    start_time = time.time()
    primes_list_comp = [is_prime(n) for n in nums]
    end_time = time.time()
    print("List comprehension time:", end_time - start_time)

    # 2. Timing prime_list function (similar to doubleList)
    start_time = time.time()
    primes_fn = prime_list(nums)
    end_time = time.time()
    print("prime_list function time:", end_time - start_time)

    # 3. Timing my_map function
    start_time = time.time()
    primes_map = my_map(nums, is_prime)
    end_time = time.time()
    print("my_map function time:", end_time - start_time)

    # 4. Timing multiprocessing pool.map with chunking
    start_time = time.time()
    with multiprocessing.Pool() as pool:
        primes_parallel = pool.map(is_prime, nums, chunksize=1000)  # Adjust chunksize as needed
    end_time = time.time()
    print("Multiprocessing pool.map time:", end_time - start_time)
