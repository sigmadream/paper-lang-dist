#include <iostream>
#include <string>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int T;
    if (!(std::cin >> T)) return 0;

    std::vector<std::string> out;
    out.reserve(T);

    for (int i = 0; i < T; ++i) {
        std::string s;
        if (!(std::cin >> s)) s = "";

        int balance = 0;
        bool valid = true;

        for (char c : s) {
            if (c == '(') {
                ++balance;
            } else {
                --balance;
            }

            if (balance < 0) {
                valid = false;
                break;
            }
        }

        if (balance != 0) valid = false;

        out.push_back(valid ? "YES" : "NO");
    }

    for (const std::string& line : out) {
        std::cout << line << '\n';
    }

    return 0;
}