def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    h = int(data[0])
    w = int(data[1])
    a = list(map(int, data[2:]))
    
    ans = 0
    for i in range(1, w - 1):
        left_max = max(a[:i + 1])
        right_max = max(a[i:])
        bound = min(left_max, right_max)
        if bound > a[i]:
            ans += bound - a[i]
    
    print(ans)

if __name__ == "__main__":
    main()
