def is_valid_parenthesis(s):
    bal = 0
    for c in s:
        if c == '(':
            bal += 1
        else:
            bal -= 1
        if bal < 0:
            return False
    return bal == 0

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    t = int(data[0])
    for i in range(1, t + 1):
        s = data[i]
        if is_valid_parenthesis(s):
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    main()
