#include <iostream>
#include <vector>
#include <string>
#include <sstream>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    // trim
    size_t start = line.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) return 0;
    size_t end = line.find_last_not_of(" \t\r\n");
    line = line.substr(start, end - start + 1);
    if (line.empty()) return 0;

    int n = std::stoi(line);

    std::vector<long long> a(n);
    int idx = 0;
    while (idx < n) {
        if (!std::getline(std::cin, line)) break;
        std::istringstream iss(line);
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
        if (i > 0) out += ' ';
        out += std::to_string(a[i]);
    }
    out += '\n';
    std::cout << out;
    return 0;
}