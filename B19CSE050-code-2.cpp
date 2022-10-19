#include<bits/stdc++.h>
#define f first
#define s second
using namespace std;

map<int,int> mapp;

string subkey_mix(string p,string k)
{
    string ans;
    for(int i=0;i<6;i++)
    {
        if(p[i]!=k[i]){ans+='1';}
        else{ans+='0';}
    }
    return ans;
}

string substitution(string p)
{
    string ans;
    int num=0;
    for(int i=3;i<6;i++)
    {
        num*=2;
        if(p[i]=='1'){num+=1;}
    }
    num=mapp[num];
    while(num>0)
    {
        if(num%2!=0){ans='1'+ans;}
        else{ans='0'+ans;}
        num/=2;
    }
    for(int i=0;i<3;i++)
    {
        num*=2;
        if(p[i]=='1'){num+=1;}
    }
    num=mapp[num];
    while(num>0)
    {
        if(num%2!=0){ans='1'+ans;}
        else{ans='0'+ans;}
        num/=2;
    }
    return ans;
}

string permuatation(string p)
{
    string ans="000000";
    ans[0]=p[0];
    ans[5]=p[5];
    ans[1]=p[3];
    ans[2]=p[4];
    ans[3]=p[1];
    ans[4]=p[2];
    return ans;
}


int main()
{
    string p="011010";
    string k1="010101",k2="001011",k3="111000",k4="111110";
    string a,b,c,d,e,f,g,h,j;
    mapp[0]=6;
    mapp[1]=5;
    mapp[2]=1;
    mapp[3]=0;
    mapp[4]=3;
    mapp[5]=2;
    mapp[6]=7;
    mapp[7]=4;
    a=subkey_mix(p,k1);
    b=substitution(a);
    d=permuatation(b);

    e=subkey_mix(d,k2);
    f=substitution(e);
    g=permuatation(f);

    h=subkey_mix(g,k3);
    j=substitution(h);
    c=subkey_mix(j,k4);
    cout<<"a "<<a<<"\n";
    cout<<"b "<<b<<"\n";
    cout<<"d "<<d<<"\n";
    cout<<"e "<<e<<"\n";
    cout<<"f "<<f<<"\n";
    cout<<"g "<<g<<"\n";
    cout<<"h "<<h<<"\n";
    cout<<"j "<<j<<"\n";
    cout<<"c "<<c<<"\n";
}
