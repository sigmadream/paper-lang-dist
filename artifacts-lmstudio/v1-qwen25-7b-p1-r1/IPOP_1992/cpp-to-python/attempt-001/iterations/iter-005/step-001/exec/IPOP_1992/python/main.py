def solve(grid, r, c, size):
    first = grid[r][c]
    same = True
    for i in range(r, r + size):
        for j in range(c, c + size):
            if grid[i][j] != first:
                same = False
                break
        if not same: break
    
    if same: return first
    
    half = size // 2
    tl = solve(grid, r, c, half)
    tr = solve(grid, r, c + half, half)
    bl = solve(grid, r + half, c, half)
    br = solve(grid, r + half, c + half, half)
    
    return "(" + tl + tr + bl + br + ")"

def main():
    n = int(input())
    grid = [input() for _ in range(n)]
    
    print(solve(grid, 0, 0, n))

if __name__ == "__main__":
    main()
