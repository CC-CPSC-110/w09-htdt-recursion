from typing import List


def doubleList(lon: List[int]) -> List[int]:
    acc = []
    for n in lon:
        acc.append(2 * n)
    return acc

def my_map(lon: List[int], fn_for_int) -> List[int]:
    acc = []
    for n in lon:
        acc.append(fn_for_int(n))
    return acc


def my_map_filter(lon: List[int], fn_for_int, filter_for_int) -> List[int]:
    acc = []
    for n in lon:
        if filter_for_int(n):
            acc.append(fn_for_int(n))
    return acc

def double(n: int) -> int:
    return 2 * n

nums = [1, 2, 3]
dbls_1 = [double(n) for n in nums]
dbls_2 = doubleList(nums)
dbls_3 = my_map(nums, double)

print(dbls_1)
print(dbls_2)
print(dbls_3)