#include <iostream>
#include <string>
#include <map>
#include <algorithm>

void frequencies(const std::string& s, std::map<char, int>& f) {
    for (char c : s) {
        f[c]++;
    }
}

int main() {
    std::string a, b;
    std::cin >> a >> b;

    std::map<char, int> fa, fb;
    frequencies(a, fa);
    frequencies(b, fb);

    if (fa == fb) {
        std::cout << 1 << std::endl;
    } else {
        std::cout << 0 << std::endl;
    }

    return 0;
}