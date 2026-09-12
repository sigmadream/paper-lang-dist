#include <stdio.h>
#include <string.h>

int main() {
    char s[101];
    if (scanf("%s", s) != 1) return 0;
    
    int len = strlen(s);
    bool valid = true;
    for (int i = 0; i < len / 2; i++) {
        if (s[i] != s[len - 1 - i]) {
            valid = false;
            break;
        }
    }
    printf("%d\n", valid ? 1 : 0);
    return 0;
}
