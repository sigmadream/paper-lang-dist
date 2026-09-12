def is_valid_parenthesis(s):
    stack = []
    for c in s:
        if c == '(':
            stack.append(c)
        else:
            if not stack:
                return False
            stack.pop()
    return not stack

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    t = int(data[0])
    for s in data[1:]:
        if is_valid_parenthesis(s):
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    main()
