#include <iostream>
#include <string>

std::string output;

void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        output.push_back(static_cast<char>('0' + start));
        output.push_back(' ');
        output.push_back(static_cast<char>('0' + end));
        output.push_back('\n');
        return;
    }

    hanoi(n - 1, start, end, mid);
    output.push_back(static_cast<char>('0' + start));
    output.push_back(' ');
    output.push_back(static_cast<char>('0' + end));
    output.push_back('\n');
    hanoi(n - 1, mid, start, end);
}

int main() {
    int n;
    if (!(std::cin >> n)) {
        return 0;
    }

    long long count = (1LL << n) - 1;

    output.reserve((1 << n) * 4 + 32);
    output += std::to_string(count);
    output.push_back('\n');

    hanoi(n, 1, 2, 3);

    std::cout << output;
    return 0;
}