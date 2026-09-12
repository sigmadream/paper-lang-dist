import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String s = scanner.nextLine();
        String bomb = scanner.nextLine();
        scanner.close();
        
        StringBuilder res = new StringBuilder();
        int b_len = bomb.length();
        
        for (char c : s.toCharArray()) {
            res.append(c);
            if (res.length() >= b_len) {
                boolean match = true;
                for (int i = 0; i < b_len; i++) {
                    if (res.charAt(res.length() - b_len + i) != bomb.charAt(i)) {
                        match = false;
                        break;
                    }
                }
                if (match) {
                    res.setLength(res.length() - b_len);
                }
            }
        }
        
        if (res.length() == 0) System.out.println("FRULA");
        else System.out.println(res.toString());
    }
}
