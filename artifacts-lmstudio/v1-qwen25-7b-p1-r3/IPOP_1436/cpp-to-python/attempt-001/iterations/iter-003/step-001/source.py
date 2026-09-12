def find_nth_movie_title(n):
    count = 0
    value = 665
    while count < n:
        value += 1
        if '666' in str(value):
            count += 1
    return value

if __name__ == "__main__":
    n = int(input())
    print(find_nth_movie_title(n))
