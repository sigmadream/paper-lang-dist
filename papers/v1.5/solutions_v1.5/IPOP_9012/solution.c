#include <stdio.h>
#include <stdbool.h>

int main(void) {
    int t;
    if (scanf("%d", &t) != 1) {
        return 0;
    }

    char s[128];
    while (t--) {
        if (scanf("%127s", s) != 1) {
            break;
        }
        int bal = 0;
        bool valid = true;
        for (int i = 0; s[i] != '\0'; ++i) {
            if (s[i] == '(') {
                bal++;
            } else if (s[i] == ')') {
                bal--;
            }
            if (bal < 0) {
                valid = false;
                break;
            }
        }
        if (bal != 0) {
            valid = false;
        }
        puts(valid ? "YES" : "NO");
    }

    return 0;
}
