#include <cstdio>
#include <string>

int main() {
    int N;
    if (scanf("%d", &N) != 1) return 0;
    if (N >= 1) {
        long long c = (1LL << N) - 1;
        printf("%lld\n", c);
        std::string out;
        // iterative or recursive with buffer
        struct Frame { int n, s, m, e; };
        // use recursion with a lambda-like approach via explicit stack
        static Frame stack[64];
        int top = 0;
        stack[top++] = {N, 1, 2, 3};
        while (top > 0) {
            Frame f = stack[--top];
            if (f.n == 1) {
                out += char('0' + f.s);
                out += ' ';
                out += char('0' + f.e);
                out += '\n';
                if (out.size() > (1 << 20)) {
                    fwrite(out.data(), 1, out.size(), stdout);
                    out.clear();
                }
            } else {
                stack[top++] = {f.n - 1, f.m, f.s, f.e};
                stack[top++] = {1, f.s, f.m, f.e};
                stack[top++] = {f.n - 1, f.s, f.e, f.m};
            }
        }
        fwrite(out.data(), 1, out.size(), stdout);
    }
    return 0;
}