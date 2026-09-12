#include <stdio.h>

int main() {
    int t;
    scanf("%d", &t);
    while (t--) {
        char s[51];
        scanf("%s", s);
        int bal = 0;
        for (int i = 0; s[i] != '\0'; i++) {
            if (s[i] == '(') bal++;
            else bal--;
            if (bal < 0) {
                printf("NO\n");
                goto next;
            }
        }
        if (bal != 0) {
            printf("NO\n");
        } else {
            printf("YES\n");
        }
        next:;
    }
    return 0;
}
