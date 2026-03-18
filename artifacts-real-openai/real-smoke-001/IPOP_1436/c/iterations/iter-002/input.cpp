#include <cstdio>
#include <cstring>

int main() {
    int n;
    if (std::scanf("%d", &n) != 1) return 0;

    int count = 0;
    int value = 665;
    char s[32];

    while (count < n) {
        ++value;
        std::sprintf(s, "%d", value);
        if (std::strstr(s, "666") != NULL) {
            ++count;
        }
    }

    std::printf("%d\n", value);
    return 0;
}
