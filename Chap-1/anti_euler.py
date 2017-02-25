#coding=UTF-8

# x_1 ^n + x_2 ^n + .. + x_{n-1} ^n = y^n
# となるような n>=3 で存在するかの話
# GCD(x_1,x_2,...,x_{n-1}) = 1 これは実質的な解なだけ

# 今回は n=5 の話
n=5

import sys
import time
import fractions

# ハッシュに関しては、python標準の辞書にて実装する
#HashSize=39916801 # is a prime number
SearchLimit=300

# 総和をキーにして元の3数を返す辞書
HashTable={}

if __name__ == '__main__' :
    SystemClock=False
    # コマンドライン引数の処理
    for idx in range(1,len(sys.argv),1):
        if 's' in sys.argv[idx]:
            SystemClock=True


    JikanFunction= time.time if SystemClock else time.clock
            
    HashInitTimeStart= JikanFunction()
    # ハッシュテーブルの初期化
    # SeachLimtが300のときは750 MBぐらいは覚悟しておいて

    for idx in range(1,SearchLimit+1,1):
        for idy in range(idx,SearchLimit+1,1):
            prepreGCD=fractions.gcd(idx,idy)
            for idz in range(idy,SearchLimit+1,1):
                # idx <= idy <= idz にして対称性で潰す
                #備え付けのpow関数を使う 実際速いのかは不明
                key = sum([ pow(suu,n) for suu in [idx,idy,idz] ])
                preGCD= 1 if prepreGCD==1 else fractions.gcd(prepreGCD,idz)
                HashTable[key]=(idx,idy,idz,preGCD)
            
    HashInitTimeEnd=JikanFunction()
    HashInitElapsedTime= HashInitTimeEnd - HashInitTimeStart
    print('ハッシュテーブル初期化完了')
    print('時間 {} sec'.format(HashInitElapsedTime))

    SearchTimeStart=JikanFunction()
    #探索
    for idx in range(1,SearchLimit+1,1):
        for idy in range(idx+1,3*SearchLimit+1,1):
            RightValue= pow(idy,n) - pow(idx,n)
            if RightValue in HashTable:
                LeftValues= HashTable[RightValue]
                if all([ LeftValues[len(LeftValues)-2] <= idx,
                         fractions.gcd(LeftValues[3],idx) == 1 ]):
                    demozi=('{x_1}^{kata} + {x_2}^{kata} ' +
                            '+{x_3}^{kata} + {x_4}^{kata}' +
                            ' = {y}^{kata}').format(x_1=LeftValues[0],x_2=LeftValues[1],x_3=LeftValues[2],x_4=idx,y=idy,kata=n)
                    
    SearchTimeEnd=JikanFunction()
    SearchElapsedTime= SearchTimeEnd - SearchTimeStart
    print('時間 {} sec'.format(SearchElapsedTime))
