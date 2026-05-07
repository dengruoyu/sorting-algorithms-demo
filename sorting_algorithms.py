"""
排序算法大全
包含：冒泡、选择、插入、希尔、归并、堆排序、计数、桶排序、基数排序等
"""

from typing import List
import random


# ==================== 交换类排序 ====================

def bubble_sort(arr: List[int]) -> None:
    """冒泡排序 - O(n²)"""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break


def bubble_sort_optimized(arr: List[int]) -> None:
    """优化版冒泡排序 - 添加提前终止"""
    n = len(arr)
    last_swap = n - 1
    
    while last_swap > 0:
        new_last_swap = 0
        for j in range(last_swap):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                new_last_swap = j
        last_swap = new_last_swap


def selection_sort(arr: List[int]) -> None:
    """选择排序 - O(n²)，不稳定"""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]


# ==================== 插入类排序 ====================

def insertion_sort(arr: List[int]) -> None:
    """插入排序 - O(n²)，对近乎有序的数据效率高"""
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def binary_insertion_sort(arr: List[int]) -> None:
    """二分插入排序 - 减少比较次数"""
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        left, right = 0, i - 1
        
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] > key:
                right = mid - 1
            else:
                left = mid + 1
        
        for j in range(i, left, -1):
            arr[j] = arr[j - 1]
        arr[left] = key


def shell_sort(arr: List[int]) -> None:
    """希尔排序 - O(n^1.3)~O(n²)，插入排序的改进版"""
    n = len(arr)
    gap = n // 2
    
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2


# ==================== 归并类排序 ====================

def merge_sort(arr: List[int]) -> None:
    """归并排序 - O(n log n)，稳定，需要额外空间"""
    if len(arr) <= 1:
        return
    
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    merge_sort(left)
    merge_sort(right)
    
    i = j = k = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1


def merge_sort_iterative(arr: List[int]) -> None:
    """迭代版归并排序"""
    n = len(arr)
    if n <= 1:
        return
    
    def merge(arr: List[int], left: int, mid: int, right: int) -> None:
        temp = []
        i, j = left, mid + 1
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp.append(arr[i])
                i += 1
            else:
                temp.append(arr[j])
                j += 1
        temp.extend(arr[i:mid + 1])
        temp.extend(arr[j:right + 1])
        arr[left:right + 1] = temp
    
    size = 1
    while size < n:
        left = 0
        while left < n:
            mid = min(left + size - 1, n - 1)
            right = min(left + 2 * size - 1, n - 1)
            if mid < right:
                merge(arr, left, mid, right)
            left += 2 * size
        size *= 2


# ==================== 堆排序 ====================

def heap_sort(arr: List[int]) -> None:
    """堆排序 - O(n log n)，不稳定"""
    n = len(arr)
    
    def heapify(size: int, root: int) -> None:
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2
        
        if left < size and arr[left] > arr[largest]:
            largest = left
        if right < size and arr[right] > arr[largest]:
            largest = right
        
        if largest != root:
            arr[root], arr[largest] = arr[largest], arr[root]
            heapify(size, largest)
    
    # 构建最大堆
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    
    # 逐个提取元素
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)


# ==================== 非比较排序 ====================

def counting_sort(arr: List[int]) -> None:
    """计数排序 - O(n + k)，适合范围较小的整数"""
    if not arr:
        return
    
    max_val = max(arr)
    min_val = min(arr)
    range_size = max_val - min_val + 1
    
    count = [0] * range_size
    for num in arr:
        count[num - min_val] += 1
    
    idx = 0
    for i, c in enumerate(count):
        while c > 0:
            arr[idx] = i + min_val
            idx += 1
            c -= 1


def bucket_sort(arr: List[float], num_buckets: int = 10) -> None:
    """桶排序 - O(n + k)，适合均匀分布的浮点数"""
    if not arr:
        return
    
    min_val, max_val = min(arr), max(arr)
    if min_val == max_val:
        return
    
    bucket_range = (max_val - min_val) / num_buckets
    buckets = [[] for _ in range(num_buckets)]
    
    for num in arr:
        idx = int((num - min_val) / bucket_range)
        if idx >= num_buckets:
            idx = num_buckets - 1
        buckets[idx].append(num)
    
    idx = 0
    for bucket in buckets:
        bucket.sort()
        for num in bucket:
            arr[idx] = num
            idx += 1


def radix_sort_lsd(arr: List[int]) -> None:
    """基数排序（最低位优先）- O(nk)，k为位数"""
    if not arr:
        return
    
    max_val = max(arr)
    if max_val < 0:
        negative = True
        max_val = abs(min(arr))
        arr[:] = [-x for x in arr]
    else:
        negative = False
    
    exp = 1
    while max_val // exp > 0:
        buckets = [[] for _ in range(10)]
        for num in arr:
            digit = (num // exp) % 10
            buckets[digit].append(num)
        
        idx = 0
        for bucket in buckets:
            for num in bucket:
                arr[idx] = num
                idx += 1
        
        exp *= 10
    
    if negative:
        arr[:] = [-x for x in arr]


# ==================== 其他排序 ====================

def tim_sort(arr: List[int]) -> None:
    """TimSort - Python内置排序算法思路，O(n log n)"""
    MIN_MERGE = 32
    n = len(arr)
    
    def insertion_sort(left: int, right: int) -> None:
        for i in range(left + 1, right + 1):
            temp = arr[i]
            j = i - 1
            while j >= left and arr[j] > temp:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = temp
    
    def merge(left: int, mid: int, right: int) -> None:
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]
        
        i = j = 0
        k = left
        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1
        
        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1
        
        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1
    
    if n < MIN_MERGE:
        insertion_sort(0, n - 1)
        return
    
    runs = []
    new_run_start = 0
    
    for i in range(1, n + 1):
        if i == n or arr[i] < arr[i - 1]:
            runs.append((new_run_start, i - 1))
            new_run_start = i
        elif arr[i] == arr[i - 1]:
            while i < n and arr[i] == arr[i - 1]:
                i += 1
            runs.append((new_run_start, i - 1))
            new_run_start = i
    
    size = MIN_MERGE
    while len(runs) > 1:
        merged = []
        for i in range(0, len(runs), 2):
            if i + 1 < len(runs):
                merge(runs[i][0], runs[i][1], runs[i + 1][1])
                merged.append((runs[i][0], runs[i + 1][1]))
            else:
                merged.append(runs[i])
        runs = merged
        size *= 2


def introsort(arr: List[int]) -> None:
    """内省排序 - 结合多种排序算法"""
    max_depth = 2 * (len(arr).bit_length() - 1)
    
    def _insertionsort(left: int, right: int) -> None:
        for i in range(left + 1, right + 1):
            temp = arr[i]
            j = i - 1
            while j >= left and arr[j] > temp:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = temp
    
    def _heapify(size: int, root: int) -> None:
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2
        
        if left < size and arr[left] > arr[largest]:
            largest = left
        if right < size and arr[right] > arr[largest]:
            largest = right
        
        if largest != root:
            arr[root], arr[largest] = arr[largest], arr[root]
            _heapify(size, largest)
    
    def _quicksort(left: int, right: int, depth_limit: int) -> None:
        if right - left <= 16:
            _insertionsort(left, right)
            return
        
        if depth_limit == 0:
            size = right - left + 1
            for i in range(size // 2 - 1, -1, -1):
                _heapify(size, i)
            for i in range(size - 1, 0, -1):
                arr[left], arr[left + i] = arr[left + i], arr[left]
                _heapify(i, 0)
            return
        
        pivot_idx = (left + right) // 2
        arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
        pivot = arr[right]
        
        i = left
        for j in range(left, right):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        
        arr[i], arr[right] = arr[right], arr[i]
        
        _quicksort(left, i - 1, depth_limit - 1)
        _quicksort(i + 1, right, depth_limit - 1)
    
    _quicksort(0, len(arr) - 1, max_depth)


# ==================== 测试与性能对比 ====================

def benchmark():
    """性能测试"""
    import time
    
    test_cases = {
        "随机数组": lambda size: [random.randint(1, size) for _ in range(size)],
        "近乎有序": lambda size: list(range(size // 10)) + list(range(size // 10)),
        "完全逆序": lambda size: list(range(size, 0, -1)),
        "大量重复": lambda size: [random.randint(1, 10) for _ in range(size)],
    }
    
    sizes = [1000, 5000, 10000]
    
    algorithms = [
        ("冒泡排序", bubble_sort),
        ("选择排序", selection_sort),
        ("插入排序", insertion_sort),
        ("二分插入排序", binary_insertion_sort),
        ("希尔排序", shell_sort),
        ("归并排序", merge_sort),
        ("堆排序", heap_sort),
        ("计数排序", counting_sort),
        ("基数排序", radix_sort_lsd),
        ("TimSort", tim_sort),
        ("内省排序", introsort),
    ]
    
    print("=" * 70)
    print("排序算法性能测试")
    print("=" * 70)
    
    for case_name, case_generator in test_cases.items():
        print(f"\n{'=' * 70}")
        print(f"测试用例: {case_name}")
        print("-" * 70)
        
        for size in sizes:
            arr = case_generator(size)
            expected = sorted(arr)
            
            print(f"\n数据规模: {size}")
            print("-" * 50)
            
            for name, sort_func in algorithms:
                try:
                    test_arr = arr.copy()
                    start = time.time()
                    sort_func(test_arr)
                    elapsed = time.time() - start
                    is_sorted = test_arr == expected
                    status = "✓" if is_sorted else "✗"
                    print(f"  {name:16s}: {elapsed:.4f}s {status}")
                except Exception as e:
                    print(f"  {name:16s}: 错误 - {str(e)[:30]}")


def demo():
    """演示"""
    print("=" * 70)
    print("排序算法演示")
    print("=" * 70)
    
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 1, 9, 3, 7, 4, 6],
        [3, 3, 3, 1, 1, 2, 2],
        [],
        [1],
    ]
    
    algorithms = [
        ("冒泡排序", bubble_sort),
        ("选择排序", selection_sort),
        ("插入排序", insertion_sort),
        ("希尔排序", shell_sort),
        ("归并排序", merge_sort),
        ("堆排序", heap_sort),
        ("计数排序", counting_sort),
        ("基数排序", radix_sort_lsd),
    ]
    
    for i, arr in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {arr}")
        print("-" * 50)
        for name, sort_func in algorithms:
            test_arr = arr.copy()
            if test_arr:  # 跳过空数组
                sort_func(test_arr)
            print(f"  {name}: {test_arr}")
    
    print("\n" + "=" * 70)
    print("运行完整性能测试（这可能需要一些时间）...")
    print("=" * 70)
    benchmark()


if __name__ == "__main__":
    demo()
