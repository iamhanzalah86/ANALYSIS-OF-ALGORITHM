import time
import matplotlib.pyplot as plt

# Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

# Arrays (reverse order for worst-case)
Arr1 = list(reversed([1,2,3,4,5]))
Arr2 = list(reversed([1,2,3,4,5,6,7,8,9,10]))
Arr3 = list(reversed(list(range(1, 51))))
Arr4 = list(reversed(list(range(1, 101))))
arrays = [Arr1, Arr2, Arr3, Arr4]
array_sizes = [len(Arr1), len(Arr2), len(Arr3), len(Arr4)]

# Measure time
def measure_time(arr):
    runs = 5
    total_time = 0
    for _ in range(runs):
        copied_arr = arr.copy()
        start = time.perf_counter()
        bubble_sort(copied_arr)
        end = time.perf_counter()
        total_time += (end - start)
    return (total_time / runs) * 1e6  # microseconds

bubble_times = [measure_time(arr) for arr in arrays]

# Plot
plt.figure(figsize=(8,5))
plt.plot(array_sizes, bubble_times, marker='o', color='red', label='Bubble Sort')
plt.title('Bubble Sort Time Complexity')
plt.xlabel('Input Size (N)')
plt.ylabel('Average Execution Time (µs)')
plt.grid(True)
plt.legend()
plt.show()
