#include <stdio.h>
#include <string.h>

int main() {
    int t;
    scanf("%d", &t);
    while (t--) {
        char s[51];
        scanf("%s", s);
        int bal = 0;
        int len = strlen(s);
        for (int i = 0; i < len; i++) {
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
