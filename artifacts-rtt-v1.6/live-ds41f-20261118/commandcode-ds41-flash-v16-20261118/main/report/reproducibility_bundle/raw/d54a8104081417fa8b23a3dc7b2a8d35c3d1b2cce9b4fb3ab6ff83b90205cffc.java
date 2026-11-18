import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;

        int T = sc.nextInt();
        StringBuilder output = new StringBuilder();

        while (T-- > 0) {
            String s = sc.next();
            int bal = 0;
            boolean valid = true;

            for (int i = 0; i < s.length(); i++) {
                if (s.charAt(i) == '(') {
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

            output.append(valid ? "YES\n" : "NO\n");
        }

        System.out.print(output);
    }
}