import time
import matplotlib.pyplot as plt

# Merge Sort
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

# Arrays (reversed)
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
        merge_sort(copied_arr)
        end = time.perf_counter()
        total_time += (end - start)
    return (total_time / runs) * 1e6  # microseconds

merge_times = [measure_time(arr) for arr in arrays]

# Plot
plt.figure(figsize=(8,5))
plt.plot(array_sizes, merge_times, marker='o', color='purple', label='Merge Sort')
plt.title('Merge Sort Time Complexity')
plt.xlabel('Input Size (N)')
plt.ylabel('Average Execution Time (µs)')
plt.grid(True)
plt.legend()
plt.show()
