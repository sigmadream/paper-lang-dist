import java.io.*;
import java.util.*;
public class Main {
static final BufferedInputStream input = new BufferedInputStream(System.in);
static String next() throws Exception {StringBuilder word=new StringBuilder();int c;do{c=input.read();}while(c<=32 && c!=-1);while(c>32 && c!=-1){word.append((char)c);c=input.read();}return word.toString();}
static int nextInt() throws Exception {return Integer.parseInt(next());}
public static void main(String[] args) throws Exception {solve();}
static void solve() throws Exception {int n=nextInt(),k=0;int[] a=new int[n];for(int i=0;i<n;i++){int v=nextInt();if(v!=0)a[k++]=v;}StringBuilder out=new StringBuilder();for(int i=0;i<n;i++){if(i>0)out.append(' ');out.append(a[i]);}System.out.println(out);}
}
