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
    int n, m;
    iss >> n >> m;

    std::unordered_map<std::string, int> name_to_id;
    std::vector<std::string> id_to_name(n + 1);

    for (int i = 1; i <= n; ++i) {
        std::string name;
        iss >> name;
        name_to_id[name] = i;
        id_to_name[i] = name;
    }

    for (int i = 0; i < m; ++i) {
        std::string q;
        iss >> q;
        if (q[0] >= '0' && q[0] <= '9') {
            int id = std::stoi(q);
            std::cout << id_to_name[id] << std::endl;
        } else {
            std::cout << name_to_id[q] << std::endl;
        }
    }

    return 0;
}
