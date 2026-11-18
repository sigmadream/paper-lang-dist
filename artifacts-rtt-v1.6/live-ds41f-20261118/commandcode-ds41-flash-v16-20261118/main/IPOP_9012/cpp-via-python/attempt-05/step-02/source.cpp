#include <iostream>
#include <string>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int T;
    if (!(std::cin >> T)) return 0;

    std::vector<std::string> output;
    output.reserve(T);

    for (int i = 0; i < T; ++i) {
        std::string s;
        std::cin >> s;

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

        output.push_back(valid ? "YES" : "NO");
    }

    for (int i = 0; i < static_cast<int>(output.size()); ++i) {
        if (i > 0) std::cout << '\n';
        std::cout << output[i];
    }

    return 0;
}