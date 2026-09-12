#include <iostream>
#include <map>
#include <string>

int main() {
    int n, m;
    std::cin >> n >> m;
    std::cin.ignore(); // Consume newline

    std::map<std::string, int> nameToId;
    std::string idToName[n + 1];

    for (int i = 1; i <= n; i++) {
        std::string name;
        std::getline(std::cin, name);
        nameToId[name] = i;
        idToName[i] = name;
    }

    for (int i = 0; i < m; i++) {
        std::string q;
        std::getline(std::cin, q);
        if (isdigit(q[0])) {
            int id = std::stoi(q);
            std::cout << idToName[id] << std::endl;
        } else {
            std::cout << nameToId[q] << std::endl;
        }
    }

    return 0;
}
