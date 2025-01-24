This project generate a QR Code for any file for share with your friends in easy way like a book.



___________________Example : 

This software take file like jpeg - mp4 . zip and compress binary to something different till to have a QRcode.
Qrcode you can share with your friend in easy way.
After your friend need to convert this dictionary to binary for use it and software save to ".something" example ".jpg".



___________________Detail of this software :

1) Convert to binary  : 
    In your fiile you have a sequence like 010101010101011111101101010101010 .... etc.
2) create a dictionary for compress some binary.

SEQ or sequence contain this elements  Seq-1, Seq-2, Seq-3, Seq-4, Seq-5, Seq-6, Seq-7, Seq 8.


Seq 1 ) 01010101010 10 digit bin
Seq 2 ) 01010101010 10 digit bin 
Seq 3 ) 01010101010 10 digit bin 
Seq 4 ) 01010101010 10 digit bin 
Seq 5 ) 01010101010 10 digit bin 
Seq 6 ) 01010101010 10 digit bin 
Seq 7 ) 01010101010 10 digit bin 
Seq 8 ) 01010101010 10 digit bin 

Note: All sequence have total 80 digit binary and the progession are like ascii table.

This in an example of the table but for any sequence of binary (up) we associate our custom dictionary.
0000 -> A
0001 -> B
0010 -> C
0011 -> D
0100 -> E
0101 -> F
0111 -> G
1111 -> H


at least we have this file like :

01010101010
01010101010
01010101010
01010101010
01010101010
01010101010
01010101010
01010101010

This sequence we convert to QR code for easy to share your file.

#############################################################################################


Your friend need to encrypt this message with this sequence with the same dictionary.

Then at least you need to share 2 items. 
1) Qr Code file in jpg
2) Dictionary table of conversion.

Enjoy
