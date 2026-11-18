import java.io.*;
import java.util.*;
public class Main {
static final BufferedInputStream input = new BufferedInputStream(System.in);
static String next() throws Exception {StringBuilder word=new StringBuilder();int c;do{c=input.read();}while(c<=32 && c!=-1);while(c>32 && c!=-1){word.append((char)c);c=input.read();}return word.toString();}
static int nextInt() throws Exception {return Integer.parseInt(next());}
public static void main(String[] args) throws Exception {solve();}
static StringBuilder output = new StringBuilder();
static void hanoi(int n, int from, int via, int to) {
    if (n == 0) return;
    hanoi(n-1, from, to, via);
    output.append(from).append(' ').append(to).append('\n');
    hanoi(n-1, via, from, to);
}
static void solve() throws Exception { int n=nextInt(); hanoi(n,1,2,3); System.out.println((1L<<n)-1); System.out.print(output); }
}
