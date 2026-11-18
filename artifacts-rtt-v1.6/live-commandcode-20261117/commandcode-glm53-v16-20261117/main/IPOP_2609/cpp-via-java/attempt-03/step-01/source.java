import java.io.*;
import java.util.*;

public class Main {
    static int gcd(int a, int b) {
        while (b != 0) {
            int r = a % b;
            a = b;
            b = r;
        }
        return a;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.ordinaryChars(0, 256);
        st.wordChars('0', '9');
        st.whitespaceChars(0, ' ');
        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int a = (int) st.nval;
        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int b = (int) st.nval;
        int g = gcd(a, b);
        StringBuilder sb = new StringBuilder();
        sb.append(g).append('\n').append((a / g) * b).append('\n');
        System.out.print(sb);
    }
}