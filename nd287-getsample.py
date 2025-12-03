import nd287
import time

#IPを書き換えてご利用ください。ポートはオプション引数で変更も可能で、デフォルトは引数無しでかまいません。
enc = nd287.NdControl("192.168.67.160")


print(enc.get_value())
#time.sleep(1)


    