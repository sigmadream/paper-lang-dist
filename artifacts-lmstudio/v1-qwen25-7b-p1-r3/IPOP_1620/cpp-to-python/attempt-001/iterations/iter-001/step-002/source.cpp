#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <sstream>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::cout.tie(nullptr);

    std::string input;
    std::getline(std::cin, input);

    std::istringstream iss(input);
    std::string token;
    std::vector<std::string> tokens;
    while (iss >> token) {
        tokens.push_back(token);
    }

    int n = std::stoi(tokens[0]);
    int m = std::stoi(tokens[1]);

    std::unordered_map<std::string, int> name_to_id;
    std::vector<std::string> id_to_name(n + 1);

    for (int i = 1; i <= n; ++i) {
        name_to_id[tokens[2 + i - 1]] = i;
        id_to_name[i] = tokens[2 + i - 1];
    }

    for (int i = 0; i < m; ++i) {
        std::string q = tokens[2 + n + i];
        if (std::isdigit(q[0])) {
            int id = std::stoi(q);
            std::cout << id_to_name[id] << std::endl;
        } else {
            std::cout << name_to_id[q] << std::endl;
        }
    }

    return 0;
}
