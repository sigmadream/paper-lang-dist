#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int N;
    std::cin >> N;
    std::vector<int> scores(N);
    for (int i = 0; i < N; ++i) {
        std::cin >> scores[i];
    }

    if (N == 1) {
        std::cout << scores[0] << std::endl;
        return 0;
    }

    int prevBest = 0, prevScore = 0, one = scores[0], two = scores[1];
    for (int i = 2; i < N; ++i) {
        int newOne = prevBest + scores[i];
        int newTwo = one + scores[i];
        int current = std::max(one, two);
        prevBest = current;
        prevScore = one;
        one = newOne;
        two = newTwo;
    }

    std::cout << std::max(one, two) << std::endl;
    return 0;
}