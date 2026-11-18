import java.io.*;
import java.util.*;
public class Main {
static final BufferedInputStream input = new BufferedInputStream(System.in);
static String next() throws Exception {StringBuilder word=new StringBuilder();int c;do{c=input.read();}while(c<=32 && c!=-1);while(c>32 && c!=-1){word.append((char)c);c=input.read();}return word.toString();}
static int nextInt() throws Exception {return Integer.parseInt(next());}
public static void main(String[] args) throws Exception {solve();}
static void solve() throws Exception {
int n=nextInt(), c=nextInt(); int[] a=new int[n]; for(int i=0;i<n;i++) a[i]=nextInt(); Arrays.sort(a);
int lo=1,hi=a[n-1]-a[0],answer=0;
while(lo<=hi){int mid=lo+(hi-lo)/2,count=1,previous=a[0];for(int i=1;i<n;i++)if(a[i]-previous>=mid){count++;previous=a[i];}
if(count>=c){answer=mid;lo=mid+1;}else hi=mid-1;}
System.out.println(answer);
}
}
