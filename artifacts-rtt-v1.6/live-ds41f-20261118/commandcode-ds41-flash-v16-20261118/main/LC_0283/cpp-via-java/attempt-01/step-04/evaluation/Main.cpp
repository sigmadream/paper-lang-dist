#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    int n = 0;
    {
        std::istringstream iss(line);
        if (!(iss >> n)) return 0;
    }

    std::vector<long long> a(n);
    int idx = 0;
    while (idx < n) {
        std::string l;
        if (!std::getline(std::cin, l)) break;
        std::istringstream iss(l);
        long long v;
        while (idx < n && (iss >> v)) {
            a[idx++] = v;
        }
    }

    int write = 0;
    for (int read = 0; read < n; ++read) {
        if (a[read] != 0) {
            long long tmp = a[write];
            a[write] = a[read];
            a[read] = tmp;
            ++write;
        }
    }

    std::string out;
    for (int i = 0; i < n; ++i) {
        if (i > 0) out.push_back(' ');
        out += std::to_string(a[i]);
    }
    out.push_back('\n');
    std::cout << out;

    return 0;
}