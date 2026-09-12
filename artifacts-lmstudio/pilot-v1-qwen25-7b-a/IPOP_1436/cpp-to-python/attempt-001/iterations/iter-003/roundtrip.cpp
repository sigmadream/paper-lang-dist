#include <iostream>
#include <string>

int find_nth_movie_title(int n) {
    int count = 0;
    int value = 665;
    while (count < n) {
        value += 1;
        if (std::to_string(value).find("666") != std::string::npos) {
            count += 1;
        }
    }
    return value;
}

int main() {
    int n;
    std::cin >> n;
    std::cout << find_nth_movie_title(n) << std::endl;
    return 0;
}
