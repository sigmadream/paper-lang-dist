import java.io.*;
import java.util.*;
public class Main {
static final BufferedInputStream input = new BufferedInputStream(System.in);
static String next() throws Exception {StringBuilder word=new StringBuilder();int c;do{c=input.read();}while(c<=32 && c!=-1);while(c>32 && c!=-1){word.append((char)c);c=input.read();}return word.toString();}
static int nextInt() throws Exception {return Integer.parseInt(next());}
public static void main(String[] args) throws Exception {solve();}
static void solve() throws Exception {int n=nextInt();int[] a=new int[n+1];StringBuilder out=new StringBuilder("0");for(int i=1;i<=n;i++){a[i]=a[i>>1]+(i&1);out.append(' ').append(a[i]);}System.out.println(out);}
}
