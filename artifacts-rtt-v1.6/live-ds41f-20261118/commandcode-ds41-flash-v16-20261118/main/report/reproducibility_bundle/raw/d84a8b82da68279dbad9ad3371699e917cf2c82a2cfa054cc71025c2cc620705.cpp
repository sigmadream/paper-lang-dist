#include <iostream>
#include <string>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int t;
    if (!(std::cin >> t)) return 0;

    std::vector<std::string> answers;
    for (int i = 0; i < t; ++i) {
        std::string s;
        std::cin >> s;

        int bal = 0;
        bool valid = true;

        for (char ch : s) {
            if (ch == '(') {
                ++bal;
            } else {
                --bal;
            }

            if (bal < 0) {
                valid = false;
                break;
            }
        }

        if (bal != 0) valid = false;

        answers.push_back(valid ? "YES" : "NO");
    }

    for (size_t i = 0; i < answers.size(); ++i) {
        if (i > 0) std::cout << '\n';
        std::cout << answers[i];
    }

    return 0;
}