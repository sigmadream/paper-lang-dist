def count_subarrays_with_sum(n, m, a):
    ans = 0
    sum = 0
    end = 0
    
    for start in range(n):
        while sum < m and end < n:
            sum += a[end]
            end += 1
        if sum == m:
            ans += 1
        sum -= a[start]
    
    return ans

# Read input
n, m = map(int, input().split())
a = list(map(int, input().split()))

# Output result
print(count_subarrays_with_sum(n, m, a))
