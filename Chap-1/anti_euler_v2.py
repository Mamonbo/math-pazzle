#coding=UTF-8

# x_1 ^n + x_2 ^n + .. + x_{n-1} ^n = y^n
# となるような n>=3 で存在するかの話
# GCD(x_1,x_2,...,x_{n-1}) = 1 これは実質的な解なだけ

# 今回は n=5 の話
# ここを変更しても別の例を求められる訳ではない
n=5

import sys
import time
import math
import bisect

# ハッシュテーブルをリストで記録し、探索に二分探索を用いる
# 辞書より速いかどうかは不明
# 辞書の方は平均 O(1) と書いてある(ほんまか)

# 探索範囲
SearchLimit=300

# n乗したものをメモしておく
powered=[]

# SearchLimitが300のときは750 MB位必要になる
# 3つの数のn乗の和を昇順でとっておくリスト
SumTable=[]

# もとの数3つの組のリストを持っておくリスト
MotoNums=[]

# 3つの数でのGCD
CurrentGCD=[]

if __name__ == '__main__':
    SystemClock=False
    CheckTime=True

    # コマンドライン引数の処理
    for argstr in sys.argv[1:]:
        if 's' in argstr:
            SystemClock=True
        elif 'nt' in argstr:
            CheckTime=False

    if CheckTime == False:
        JikanFunction=(lambda : 0) #ダミー
    else:
        if SystemClock:
            JikanFunction=time.time
        else:
            JikanFunction=time.clock

    # ハッシュテーブルの初期化
    HashInitTimeStart=JikanFunction()

    # 先ずpoweredを初期化する
    # yでも使うので、SearchLimitよりかなり多めにしてある
    for idx in range(0,2*SearchLimit+1,1):
        powered.append(pow(idx,n))

    # SumTableを初期化する
    # 多重ループの外で出来ることはやっておく
    MotoTriplette=[0,0,0]
    for idx in range(1,SearchLimit+1,1):
        MotoTriplette[0]=powered[idx]
        for idy in range(idx,SearchLimit+1,1):
            MotoTriplette[1]=powered[idy]
            TmpGCD=math.gcd(idx,idy)
            for idz in range(idy,SearchLimit+1,1):
                MotoTriplette[2]=powered[idz]
                ate=tuple(MotoTriplette)
                key=sum(ate)
                preGCD= 1 if TmpGCD == 1 else math.gcd(TmpGCD,idz)

                insert_position=bisect.bisect_left(SumTable,key)
                if insert_position < len(SumTable) and \
                SumTable[insert_position] == key:
                    #被っているとき
                    MotoNums[insert_position].append(ate)
                    CurrentGCD[insert_position].append(preGCD)
                else:
                    #被っていないとき
                    SumTable.insert(insert_position,key)
                    MotoNums.insert(insert_position,[ate])
                    CurrentGCD.insert(insert_position,[preGCD])

    #    print(MotoNums)
    #    print(len(MotoNums))
    SumEnd=powered[SearchLimit]*3
    HashInitTimeEnd=JikanFunction()
    HashInitElapsedTime= HashInitTimeEnd - HashInitTimeStart

    if CheckTime:
        print('ハッシュテーブル初期化完了')
        print('時間 {} sec'.format(HashInitElapsedTime))

    SearchTimeStart=JikanFunction()
    #探索
    for idx in range(1,SearchLimit+1,1):
        PoweredNum=powered[idx]
        for idy in range(idx+1,2*SearchLimit+1,1):
            RightValue = powered[idy] - PoweredNum
            if RightValue > SumEnd:
                break

            position=bisect.bisect_left(SumTable,RightValue)
            if SumTable[position]==RightValue :
                # その総和に至るものは複数あるかもしれない
                for CandicateIdx in range(0,len(MotoNums[position]),1):
                    LeftValues=MotoNums[position][CandicateIdx]
                    TmpGCD=CurrentGCD[pos][CandicateIdx]

                    #gcd check
                    TmpGCD=math.gcd(TmpGCD,idx)
                    FinalGCD=math.gcd(TmpGCD,idy)
                    if FinalGCD != 1:
                        continue

                    # 昇順になっているかチェック
                    if LeftValues[len(LeftValues)-1] <= idx:
                        demozi_moto=('{x_1}^{kata} + {x_2}^{kata}' +
                                     '{x_3}^{kata} + {x_4}^{kata}' +
                                     ' = {y}^{kata}')
                        demozi=demozi_moto.format(x_1=LeftValues[0],x_2=LeftValues[1],x_3=LeftValues[2],x_4=idx,y=idy,kata=n)
                        print(demozi)

                        
    SearchTimeEnd=JikanFunction()
    SearchElapsedTime= SearchTimeEnd - SearchTimeStart
    if CheckTime:
        print('時間 {} sec'.format(SearchElapsedTime))
