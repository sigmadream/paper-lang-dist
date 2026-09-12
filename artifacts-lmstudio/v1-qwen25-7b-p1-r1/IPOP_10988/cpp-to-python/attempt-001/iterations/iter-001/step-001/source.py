def is_palindrome(word):
    return word == word[::-1]

word = input().strip()
print(1 if is_palindrome(word) else 0)
