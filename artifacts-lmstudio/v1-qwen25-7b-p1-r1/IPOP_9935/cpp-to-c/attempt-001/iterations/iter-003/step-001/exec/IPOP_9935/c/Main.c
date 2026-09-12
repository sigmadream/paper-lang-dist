#include <stdio.h>
#include <string.h>

int main() {
    char s[1000001], bomb[37];
    scanf("%s %s", s, bomb);
    
    char res[1000001] = "";
    int b_len = strlen(bomb);
    
    for (int i = 0; i < strlen(s); i++) {
        strncat(res, s + i, 1);
        if (strlen(res) >= b_len) {
            int match = 1;
            for (int j = 0; j < b_len; j++) {
                if (res[strlen(res) - b_len + j] != bomb[j]) {
                    match = 0;
                    break;
                }
            }
            if (match) {
                res[strlen(res) - b_len] = '\0';
            }
        }
    }
    
    if (strlen(res) == 0) printf("FRULA\n");
    else printf("%s\n", res);
    return 0;
}
