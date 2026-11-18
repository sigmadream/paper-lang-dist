#include <iostream>
#include <string>
#include <cctype>

static std::string stripSpaces(const std::string& s) {
    std::string r;
    r.reserve(s.size());
    for (char c : s) {
        if (!std::isspace(static_cast<unsigned char>(c))) r += c;
    }
    return r;
}

int main() {
    std::string s, t;
    std::getline(std::cin, s);
    std::getline(std::cin, t);
    s = stripSpaces(s);
    t = stripSpaces(t);

    int cnt[26] = {0};
    for (char c : s) cnt[c - 'a']++;
    for (char c : t) cnt[c - 'a']--;

    bool ok = true;
    for (int i = 0; i < 26; ++i) {
        if (cnt[i] != 0) { ok = false; break; }
    }

    std::cout << (ok ? 1 : 0) << '\n';
    return 0;
}