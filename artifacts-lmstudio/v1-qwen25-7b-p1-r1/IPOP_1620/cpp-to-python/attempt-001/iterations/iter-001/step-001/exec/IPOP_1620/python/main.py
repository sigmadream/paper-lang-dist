def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    name_to_id = {}
    id_to_name = [None] * (n + 1)
    
    for i in range(1, n + 1):
        name = data[2 + i - 1]
        name_to_id[name] = i
        id_to_name[i] = name
    
    for i in range(m):
        q = data[2 + n + i]
        if q.isdigit():
            print(id_to_name[int(q)])
        else:
            print(name_to_id[q])

if __name__ == "__main__":
    main()
