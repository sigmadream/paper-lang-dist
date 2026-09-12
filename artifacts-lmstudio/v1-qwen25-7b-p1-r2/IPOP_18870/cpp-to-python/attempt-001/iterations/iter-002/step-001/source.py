def coordinate_compression(n, a):
    sorted_a = sorted(set(a))
    compressed = {x: i for i, x in enumerate(sorted_a)}
    result = [compressed[x] for x in a]
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))

    result = coordinate_compression(n, a)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()
