import java.io.*;

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
        st.parseNumbers();
        if (st.nextToken() == StreamTokenizer.TT_NUMBER) {
            int a = (int) st.nval;
            if (st.nextToken() == StreamTokenizer.TT_NUMBER) {
                int b = (int) st.nval;
                int g = gcd(a, b);
                StringBuilder sb = new StringBuilder();
                sb.append(g).append('\n').append((a / g) * b).append('\n');
                System.out.print(sb);
            }
        }
    }
}