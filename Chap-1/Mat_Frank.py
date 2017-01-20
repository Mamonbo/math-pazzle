#coding=UTF-8

# Matthew Frank の漸化式
# gcdが1または素数になることが証明されている

import fractions

TRIAL=100
Ainit=7

for idx in range(1,TRIAL):
    if idx==1:
        a=Ainit
        print('a(1) = {}'.format(a))
    else:
        tmp_gcd=fractions.gcd(idx,a_prev)
        a=a_prev+tmp_gcd

        printmoji='a({0}) = {1} + gcd({gcd_a},{gcd_b}) = {1} + {gcd} = {res}'
        printmoji=printmoji.format(idx,a_prev,res=a,
        gcd_a=idx,gcd_b=a_prev,gcd=tmp_gcd)
        print(printmoji)

    a_prev=a



