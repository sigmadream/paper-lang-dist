#include <iostream>
#include <string>
#include <vector>

static bool readLine(std::string& out) {
    if (!std::getline(std::cin, out)) return false;
    if (!out.empty() && out.back() == '\r') out.pop_back();
    return true;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    if (!readLine(s) || !readLine(t)) {
        std::cout << 0 << "\n";
        return 0;
    }
    if (s.size() != t.size()) {
        std::cout << 0 << "\n";
        return 0;
    }
    std::vector<int> counts(26, 0);
    for (std::size_t i = 0; i < s.size(); ++i) {
        counts[s[i] - 'a']++;
        counts[t[i] - 'a']--;
    }
    for (int c : counts) {
        if (c != 0) {
            std::cout << 0 << "\n";
            return 0;
        }
    }
    std::cout << 1 << "\n";
    return 0;
}