#include <iostream>
#include <string>
#include <vector>

static std::string javaTrim(const std::string& str) {
    std::size_t start = 0;
    std::size_t end = str.size();
    while (start < end && static_cast<unsigned char>(str[start]) <= 0x20) {
        ++start;
    }
    while (end > start && static_cast<unsigned char>(str[end - 1]) <= 0x20) {
        --end;
    }
    return str.substr(start, end - start);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s;
    if (!std::getline(std::cin, s)) {
        return 0;
    }

    std::string t;
    if (!std::getline(std::cin, t)) {
        return 0;
    }

    s = javaTrim(s);
    t = javaTrim(t);

    if (s.empty() || t.empty()) {
        return 0;
    }

    std::vector<int> counts(26, 0);

    for (char c : s) {
        counts[c - 'a']++;
    }
    for (char c : t) {
        counts[c - 'a']--;
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