def main():
    import sys
    input = sys.stdin.read
    data = input().split()

    n = int(data[0])
    ropes = list(map(int, data[1:]))

    ropes.sort(reverse=True)

    max_weight = 0
    for i in range(n):
        current_weight = ropes[i] * (i + 1)
        if current_weight > max_weight:
            max_weight = current_weight

    print(max_weight)

if __name__ == "__main__":
    main()
