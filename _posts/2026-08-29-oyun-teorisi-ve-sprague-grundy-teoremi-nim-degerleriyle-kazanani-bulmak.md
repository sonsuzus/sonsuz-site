---
layout: post
title: "Oyun Teorisi ve Sprague-Grundy Teoremi: Nim-Değerleriyle Kazananı Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - oyun teorisi
  - sprague-grundy
  - algoritmalar
---

Bir masa oyununun sonunu hamle hamle tahmin etmek bazen sezgiye, bazen de bolca şansa bırakılır. Ancak iki oyuncunun da kusursuz oynadığı, şans faktörü içermeyen ve her hamlenin oyunu bitişe yaklaştırdığı tarafsız kombinatoryal oyunlarda sonuç matematikle belirlenebilir. Sprague-Grundy teoremi, farklı görünen oyunları bile birer Nim yığınına dönüştürerek “kazanan kim?” sorusuna kesin bir yanıt verir.
``

## Önce oyun sınıfını tanıyalım

Teorem her oyun için geçerli değildir. Uygulanacak oyunun **iki oyunculu**, **sıra tabanlı**, **sonlu**, **şanssız** ve **tarafsız** olması gerekir. Tarafsızlık, iki oyuncunun da bulunduğu konumdan aynı yasal hamleleri yapabilmesi demektir. Ayrıca normal oyun kuralı kullanılır: Hamle yapamayan oyuncu kaybeder.

| Kavram | Anlamı | Örnek |
|---|---|---|
| Tarafsız oyun | Hamle seçenekleri oyuncuya göre değişmez | Nim, taş kaldırma oyunları |
| Partizan oyun | Oyuncuların hamleleri farklıdır | Satranç, dama |
| Normal oyun | Son hamleyi yapan kazanır | Klasik Nim |
| Misère oyun | Son hamleyi yapan kaybeder | Misère Nim |

Bir konum için iki temel durum vardır: **P-konumu** ve **N-konumu**. P, önceki oyuncunun kazandığı; yani sıradaki oyuncunun kusursuz savunmaya karşı kaybettiği konumdur. N ise sıradaki oyuncunun bir kazanç hamlesi bulunduğu konumdur. Sprague-Grundy yaklaşımı bu sınıflandırmayı yalnızca “kazanır/kaybeder” düzeyinde bırakmaz; her konuma sayısal bir değer verir.

## Grundy sayısı ve mex fikri

Bir konumun Grundy sayısı, ulaşılabilen tüm konumların Grundy sayılarının **mex**’idir. `mex` (minimum excluded), negatif olmayan sayılar içinde kümede bulunmayan en küçük değerdir:

$$\operatorname{mex}(\{0,1,3\})=2$$

Dolayısıyla bir konum $G$ için:

$$g(G)=\operatorname{mex}(\{g(H) \mid H \text{, } G\text{'den tek hamlede ulaşılabilir}\})$$

Hamle yapılamayan bitiş konumunda seçenek kümesi boştur. Bu yüzden $\operatorname{mex}(\varnothing)=0$ olur. Kritik yorum şudur: Grundy değeri sıfır olan konumlar P-konumlarıdır; sıfırdan farklı olanlar N-konumlarıdır.

Örneğin bir yığından her hamlede 1, 2 veya 3 taş alınabiliyorsa, yığın boyutu $n$ için değerler periyodik davranır:

| $n$ | Ulaşılabilen değerler | $g(n)$ |
|---:|---|---:|
| 0 | — | 0 |
| 1 | {0} | 1 |
| 2 | {1, 0} | 2 |
| 3 | {2, 1, 0} | 3 |
| 4 | {3, 2, 1} | 0 |

Burada desen $g(n)=n\bmod 4$ şeklindedir. Dört taş, ilk bakışta güçlü görünse de aslında rakibe dengeli bir cevap fırsatı veren kayıp konumudur.

## Ayrık oyunların sihirli birleşimi: XOR

Sprague-Grundy teoremi, bağımsız alt oyunların toplamında her alt oyunun Grundy değerinin hesaplanacağını söyler. Toplam konumun değeri bu sayıların bit düzeyinde özel veya işlemidir:

$$g(G_1+G_2+\cdots+G_k)=g(G_1)\oplus g(G_2)\oplus\cdots\oplus g(G_k)$$

Sonuç sıfırsa sıradaki oyuncu kaybeder; sıfır değilse, XOR sonucunu sıfıra indirecek bir hamle vardır. İşte Nim’in ünlü stratejisi, aslında bu çok daha genel teoremin özel hâlidir.

## Python ile Grundy hesabı

Aşağıdaki kod, izin verilen taş alma miktarları için $0$ ile `n` arasındaki tüm Grundy değerlerini dinamik programlama ile üretir:

```python
def grundy_values(n, moves):
    g = [0] * (n + 1)

    for pile in range(1, n + 1):
        reachable = {g[pile - move]
                     for move in moves if move <= pile}
        value = 0
        while value in reachable:
            value += 1
        g[pile] = value

    return g

moves = [1, 2, 3]
values = grundy_values(12, moves)
print(values)  # [0, 1, 2, 3, 0, 1, 2, 3, ...]
```

Kodda her `pile` için erişilebilir değerler kümesi kurulur; ardından kümede olmayan en küçük sayı aranır. Bu doğrudan mex tanımıdır. Birden fazla yığın varsa ilgili `values[yigin_boyutu]` değerlerini XOR’lamak yeterlidir.

Sprague-Grundy teoreminin güzelliği, oyun ağacını baştan sona gezmek yerine konumları Nim diliyle özetlemesidir. Bir bulmacayı bağımsız parçalara ayırabiliyorsanız, karmaşık strateji çoğu zaman tek bir XOR sonucunda saklanıyordur.
