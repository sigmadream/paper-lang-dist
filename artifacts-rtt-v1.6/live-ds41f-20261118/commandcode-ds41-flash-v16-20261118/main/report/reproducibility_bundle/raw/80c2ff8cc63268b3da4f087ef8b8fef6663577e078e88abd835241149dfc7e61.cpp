#include <iostream>
#include <string>
#include <vector>

int main() {
    std::string s, t;
    std::getline(std::cin, s);
    std::getline(std::cin, t);

    std::vector<int> counts(26, 0);

    for (char c : s) {
        if (c >= 'a' && c <= 'z') {
            counts[c - 'a']++;
        }
    }

    for (char c : t) {
        if (c >= 'a' && c <= 'z') {
            counts[c - 'a']--;
        }
    }

    bool valid = true;
    for (int count : counts) {
        if (count != 0) {
            valid = false;
            break;
        }
    }

    std::cout << (valid ? 1 : 0) << '\n';
    return 0;
}