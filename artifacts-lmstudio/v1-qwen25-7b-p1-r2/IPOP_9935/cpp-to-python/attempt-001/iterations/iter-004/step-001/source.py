def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    s = data[0]
    bomb = data[1]

    res = []
    b_len = len(bomb)

    for c in s:
        res.append(c)
        if len(res) >= b_len:
            match = True
            for i in range(b_len):
                if res[len(res) - b_len + i] != bomb[i]:
                    match = False
                    break
            if match:
                res = res[:-b_len]

    if not res:
        print("FRULA")
    else:
        print(''.join(res))

if __name__ == "__main__":
    main()
