import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt();
        StringBuilder sb = new StringBuilder();

        while (T-- > 0) {
            String s = sc.next();
            int bal = 0;
            boolean valid = true;

            for (int i = 0; i < s.length(); i++) {
                char c = s.charAt(i);
                if (c == '(') {
                    ++bal;
                } else {
                    --bal;
                }

                if (bal < 0) {
                    valid = false;
                    break;
                }
            }

            if (bal != 0) valid = false;

            sb.append(valid ? "YES\n" : "NO\n");
        }

        System.out.print(sb);
    }
}