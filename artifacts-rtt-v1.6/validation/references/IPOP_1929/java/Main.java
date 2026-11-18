import java.io.*;
import java.util.*;
public class Main {
static final BufferedInputStream input = new BufferedInputStream(System.in);
static String next() throws Exception {StringBuilder word=new StringBuilder();int c;do{c=input.read();}while(c<=32 && c!=-1);while(c>32 && c!=-1){word.append((char)c);c=input.read();}return word.toString();}
static int nextInt() throws Exception {return Integer.parseInt(next());}
public static void main(String[] args) throws Exception {solve();}
static void solve() throws Exception {int lo=nextInt(),hi=nextInt();boolean[] composite=new boolean[hi+1];composite[0]=composite[1]=true;
for(int d=2;d*d<=hi;d++)if(!composite[d])for(int j=d*d;j<=hi;j+=d)composite[j]=true;
StringBuilder out=new StringBuilder();for(int i=lo;i<=hi;i++)if(!composite[i])out.append(i).append('\n');System.out.print(out);}
}
