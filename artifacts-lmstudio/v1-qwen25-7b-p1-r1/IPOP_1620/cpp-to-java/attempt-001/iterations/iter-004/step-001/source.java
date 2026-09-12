import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int m = scanner.nextInt();
        scanner.nextLine(); // Consume newline

        Map<String, Integer> nameToId = new HashMap<>();
        String[] idToName = new String[n + 1];

        for (int i = 1; i <= n; i++) {
            String name = scanner.nextLine();
            nameToId.put(name, i);
            idToName[i] = name;
        }

        for (int i = 0; i < m; i++) {
            String q = scanner.nextLine();
            if (Character.isDigit(q.charAt(0))) {
                int id = Integer.parseInt(q);
                System.out.println(idToName[id]);
            } else {
                System.out.println(nameToId.get(q));
            }
        }

        scanner.close();
    }
}
