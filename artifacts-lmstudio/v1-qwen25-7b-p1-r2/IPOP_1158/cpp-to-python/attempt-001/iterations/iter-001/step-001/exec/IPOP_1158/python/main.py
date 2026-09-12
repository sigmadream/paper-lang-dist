def josephus(n, k):
    q = list(range(1, n + 1))
    idx = 0
    result = []
    
    while q:
        idx = (idx + k - 1) % len(q)
        result.append(q.pop(idx))
    
    return result

def main():
    n, k = map(int, input().split())
    result = josephus(n, k)
    print(f"<{', '.join(map(str, result))}>")

if __name__ == "__main__":
    main()
