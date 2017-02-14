#coding=UTF-8

# Miller-Rabin の素数判定法の実験
# 詳しい説明は本参照

import math
import random
import sys
import time

keisoku = False

def mod_mul(x,y,hou):
    # x * y (mod hou(p) ) を計算する
    # 適宜正規化(0 - (p-1)の範囲にする)ことでオーバーフローを防ぐ
    # とあるがpythonでも多倍長を使うと計算が多くなるのでそれを防ぐ
    # 法がある以外はいつもの掛け算の筆算を2進数でやっているイメージ
    # 但し最後に一気に足し上げるのではなく、適宜加えていく
    kaeshi=0

    #引数を正規化する
    x_normalized = x % hou
    y_normalized = y % hou

    itr=y_normalized
    zouka=x_normalized
    while itr > 0:
        if itr % 2 == 1:
            kaeshi = (kaeshi + zouka) % hou

        zouka=zouka*2
        itr=itr//2
        
    return kaeshi

def mod_pow(x,y,hou):
    # x * y (mod hou(p) ) を計算する
    # 大体はmod_mulと同じ方針
    # x^1 * x^10 = x^(1+10) = x^11 ということ
    kaeshi=1 #ここを0にすると 何時でも0を返してしまう

    x_normalized = x % hou
    y_normalized = y % hou

    itr = y_normalized
    zouka = x_normalized
    while itr > 0:
        if itr % 2 == 1:
            kaeshi = mod_mul(kaeshi,zouka,hou)

        zouka = mod_mul(zouka,zouka,hou)
        itr = itr // 2

    return kaeshi

def prime_p_p(num):
    # このプログラムの核
    # 確率的に素数を判定する

    global keisoku
    # 合成数であることを見つけてくれる かもしれない 「証人」たち
    # 確率的素数判定法では定番の言葉らしい
    eyes=(2,3,5,7,11,13,17,23)

    #コーナーケース
    if num < 2:
        return False

    #別に強く無い例
    for ojo in eyes:
        if num == ojo:
            return True
        elif num % ojo == 0:
            return False

    # ここからは a < n となる
    # num-1 = 2**s * d (dが整数かつsが最大)
    # dが奇数になる
    d= num-1
    s=0
    while d % 2 ==0:
        d = d // 2
        s = s + 1

    for ojo in eyes:
        # idy 0 のケース
        x = mod_pow(ojo,d,num)
        # a**d \equiv 1 (mod num) もしくは
        # a**(2**i * d) \equiv -1 (mod num)
        # の i = 0 のとき
        if (x == 1) or (x == num - 1):
            #この観測者では「シロ」
            continue

        # a**(2**i * d) \equiv -1 (mod num)
        # となる s-1 >= i > 0 が存在
        # すると koe が True に
        koe = False
        for idy in range(1,s,1):
            #二乗していく
            x = mod_mul(x, x, num)

            if x == 1:
                #これ以降はずっと1
                return False

            #hit
            if x == num - 1:
                koe = True
                if not keisoku:
                    print('3:x = {}'.format(x))
                break

        if not koe:
            return False

    return True


def prime_p_normal(num):
    # 普通の教科書に載っている 平方根分まで
    # 探索する素数判定アルゴリズム
    
    # 原作から手を加えて2以外は奇数のみを調べる
    # 何故なら2以降の素数は全て奇数だから

    # 以下のプログラムで捌けないコーナーケース
    if num < 2:
        return False
    elif num==2:
        return True
    elif num % 2 == 0:
        return False

    jogen=math.floor(math.sqrt(num))
    for idx in range(3,jogen+1,2):
        # for debugging
        #print('\t test {} divided by {}'.format(num,idx))
        
        if num % idx == 0:
            return False
    return True


if __name__ == '__main__' :

    #global keisoku
    verborse = False
    # -t 指定時は計時版にする
    # stdout 出力に引っ張られないように、デバッグ出力を切る
    for idx in range(1,len(sys.argv),1):
        if 't' in sys.argv[idx]:
            keisoku=True
        if 'v' in sys.argv[idx]:
            verborse=True
    
    # for debugging
    #print('prime_p_normal() test')
    #for idx in range(1,50+1,1):
    #    print('{} : {}'.format(idx,prime_p_normal(idx)))
    #print('')
    sys.stdout.flush()
    
    Trial_Times=10**5
    Rand_Range=(0,2**16-1)

    Trial_Nums=[]
    # Genate Random Numbers
    for idx in range(0,Trial_Times,1):
        Trial_Nums.append(random.randint(*Rand_Range))

    print('Normal Prime Test')
    Normal_Prime_Test_start=time.time()
    Normal_Prime_Test_Result=[]
    for n in Trial_Nums:
        Normal_Prime_Test_Result.append(prime_p_normal(n))
    Normal_Prime_Test_end=time.time()

    Normal_Prime_Test_Elapsed_Time=Normal_Prime_Test_end - Normal_Prime_Test_start

    print('{} sec'.format(Normal_Prime_Test_Elapsed_Time))
    sys.stdout.flush()
    
    print('Miller-Rabin Prime test')
    Miller_Rabin_Prime_Test_start=time.time()
    for idx in range(0,Trial_Times,1):
        if prime_p_p(Trial_Nums[idx]) != Normal_Prime_Test_Result[idx]:
            print('{}は誤判定'.format(Trial_Nums[idx]))
            if verborse:
                print('prime_p_p({}):      {}'.format(Trial_Nums[idx],prime_p_p(Trial_Nums[idx])))
                print('prime_p_normal({}): {}'.format(Trial_Nums[idx],Normal_Prime_Test_Result[idx]))
                sys.stdout.flush()

        if verborse or not keisoku:
            if idx % 100 == 99: #0 startのため
                print('{}回目'.format(idx+1))

    Miller_Rabin_Prime_Test_end=time.time()
    Miller_Rabin_Prime_Test_Elapsed_Time=Miller_Rabin_Prime_Test_end - Miller_Rabin_Prime_Test_start
    print('{} sec'.format(Miller_Rabin_Prime_Test_Elapsed_Time))
