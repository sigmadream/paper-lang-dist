#include <stdio.h>
#include <string.h>

int main() {
    int t;
    scanf("%d", &t);
    while (t--) {
        char s[51];
        scanf("%s", s);
        int bal = 0;
        int valid = 1;
        for (int i = 0; s[i] != '\0'; i++) {
            if (s[i] == '(') bal++;
            else bal--;
            if (bal < 0) {
                valid = 0;
                break;
            }
        }
        if (bal != 0) valid = 0;
        if (valid) printf("YES\n");
        else printf("NO\n");
    }
    return 0;
}
