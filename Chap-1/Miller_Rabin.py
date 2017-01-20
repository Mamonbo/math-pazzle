#coding=UTF-8

# Miller-Rabin の素数判定法の実験
# 詳しい説明は本参照

import math

a=(2,3,5,7,11,13,17,23)
#後で良い感じの名前にする

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
    pass

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
        print('\t test {} divided by {}'.format(num,idx))
        
        if num % idx == 0:
            return False
    return True


if __name__ == '__main__' :
    # for debugging
    print('prime_p_normal test')
    for idx in range(1,50+1,1):
        print('{} : {}'.format(idx,prime_p_normal(idx)))
    print('')
