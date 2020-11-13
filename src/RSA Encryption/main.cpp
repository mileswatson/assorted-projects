#include <iostream>
#include <cmath>
#include <string>

using namespace std;

long getPrime(long testNum){
  long limit, testFor;
  bool prime;
  testNum += (testNum+1) % 2;
  while(true){
    limit = round(pow(testNum,0.5));
    testFor = 3;
    prime = true;
    while(testFor<=limit){
      if (testNum % testFor == 0){
        prime = false;
        break;
      }
      testFor += 2;
    }
    if(prime){
      return testNum;
    }
    testNum += 2;
  }
}

long * getKeys(long p, long q){
  long n,tN,e,d;
  static long returnNums[3];
  p = getPrime(p);
  q = getPrime(q);
  n = p*q;
  tN = (p-1)*(q-1);
  e = getPrime(rand()%((long)round(n*0.8)));
  while(n%e==0){
    e = getPrime(e+1);
  }
  d = 1;
  while(true){
    if((e*d)%tN == 1){
      break;
    } else{
      d++;
    }
  }
  returnNums[0] = e;
  returnNums[1] = n;
  returnNums[2] = d;
  return returnNums;
  
}



int main(){
  long *keys;
  keys = getKeys(100000,15000);
  cout << *(keys)<< endl << *(keys+1) << endl << *(keys+2) << endl;
}
