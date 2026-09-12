#include <stdio.h>
#include <string.h>

int main() {
    char s[1000001], bomb[37];
    if (scanf("%s %s", s, bomb) != 2) return 0;
    
    char res[1000001] = "";
    int b_len = strlen(bomb);
    
    for (int i = 0; s[i] != '\0'; i++) {
        res[strlen(res)] = s[i];
        if (strlen(res) >= b_len) {
            bool match = 1;
            for (int j = 0; j < b_len; j++) {
                if (res[strlen(res) - b_len + j] != bomb[j]) {
                    match = 0;
                    break;
                }
            }
            if (match) {
                for (int j = 0; j < b_len; j++) res[strlen(res) - 1] = '\0';
            }
        }
    }
    
    if (strlen(res) == 0) printf("FRULA\n");
    else printf("%s\n", res);
    return 0;
}
