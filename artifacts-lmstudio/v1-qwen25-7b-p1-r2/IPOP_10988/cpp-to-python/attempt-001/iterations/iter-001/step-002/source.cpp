#include <iostream>
#include <string>
#include <algorithm>

bool is_palindrome(const std::string& word) {
    int left = 0;
    int right = word.length() - 1;
    while (left < right) {
        if (word[left] != word[right]) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}

int main() {
    std::string word;
    std::cin >> word;
    std::cout << (is_palindrome(word) ? 1 : 0) << std::endl;
    return 0;
}
