---
layout: post
title: "Tartı Problemi ve Denge Algoritmaları: Ağırlıkların Gizli Matematiği"
math: true
categories: 
  - Bilgi
tags: 
  - matematik
  - algoritma
  - denge
  - python
  - kombinatorik
toc: true
image: /img/tarti-problemi-ve-80.png
---

Elinizde yalnızca birkaç ağırlık olduğunu düşünün. Buna rağmen 1 gramdan belirli bir üst sınıra kadar her tam sayı değerini tartabilir misiniz? İlk bakışta çok sayıda ağırlık gerekiyormuş gibi görünür. Oysa ağırlıkları doğru seçtiğimizde her parça, bir sayı sisteminin basamağına dönüşür. Tartı problemi; ikili sistem, dengeli üçlü sistem ve açgözlü algoritmaların fiziksel dünyadaki şaşırtıcı bir buluşma noktasıdır.

``

## Tek kefeye ağırlık koymak: İkili sistem

Nesne bir kefede, ağırlıkların tamamı diğer kefede olmak zorundaysa her ağırlık için iki seçeneğimiz vardır: **kullanmak** veya **kullanmamak**. Bu iki durum, ikili sayı sistemindeki 0 ve 1 rakamlarına karşılık gelir.

Bu nedenle en verimli ağırlık dizisi ikinin kuvvetlerinden oluşur:

$$1, 2, 4, 8, 16, \ldots, 2^{n-1}$$

Bu ağırlıkların toplamı şöyledir:

$$1+2+4+\cdots+2^{n-1}=2^n-1$$

Dolayısıyla $n$ adet ağırlıkla, tek kefeye yerleştirme kuralı altında 1 ile $2^n-1$ arasındaki bütün tam sayılar tartılabilir. Örneğin 13 gramın ikili gösterimi $1101_2$ olduğundan:

$$13=8+4+1$$

Yani 8, 4 ve 1 gramlık ağırlıkları kullanır, 2 gramlığı kenarda bırakırsınız.

## İki kefeyi de kullanmak: Dengeli üçlü sistem

Ağırlıkları terazinin iki kefesine de koyabiliyorsak seçenek sayısı üçe çıkar:

- Nesnenin karşı kefesine koymak: $+1$
- Hiç kullanmamak: $0$
- Nesneyle aynı kefeye koymak: $-1$

Bu kez doğal seçim üçün kuvvetleridir:

$$1, 3, 9, 27, \ldots, 3^{n-1}$$

Her ölçüm, katsayıları $-1$, $0$ veya $1$ olan bir toplam şeklinde yazılır:

$$m=a_0 3^0+a_1 3^1+\cdots+a_{n-1}3^{n-1}$$

Burada $a_i\in\{-1,0,1\}$ olur. Örneğin 8 gram:

$$8=9-1$$

Bu durumda 9 gram karşı kefeye, 1 gram ise tartılan nesneyle aynı kefeye konur. Terazi dengelendiğinde $8+1=9$ eşitliğini fiziksel olarak görürüz.

| Yöntem | Ağırlık dizisi | Her ağırlığın durumu | $n$ ağırlıkla üst sınır |
|---|---|---:|---:|
| Tek kefeli | $1,2,4,\ldots$ | 2 seçenek | $2^n-1$ |
| İki kefeli | $1,3,9,\ldots$ | 3 seçenek | $(3^n-1)/2$ |

Dengeli üçlü yöntemde erişilebilen en büyük pozitif değer:

$$1+3+9+\cdots+3^{n-1}=\frac{3^n-1}{2}$$

Örneğin dört ağırlıkla tek kefeli sistem en fazla 15 gramı, iki kefeli sistem ise 40 gramı ölçer. Terazinin iki tarafını kullanmak kapasiteyi ciddi biçimde artırır.

## Dengeyi bulan algoritma

Bir sayıyı dengeli üçlüye çevirmek için sayıyı sürekli 3'e böleriz. Kalan 0 veya 1 ise doğrudan kullanılabilir. Kalan 2 olduğunda bunu $-1$ olarak yorumlayıp sonraki basamağa 1 ekleriz; çünkü $2=3-1$ eşitliği geçerlidir.

```python
def tarti_plani(hedef):
    agirlik = 1
    nesne_tarafi = []
    karsi_taraf = []

    while hedef > 0:
        kalan = hedef % 3

        if kalan == 1:
            karsi_taraf.append(agirlik)
        elif kalan == 2:
            nesne_tarafi.append(agirlik)
            hedef += 1

        hedef //= 3
        agirlik *= 3

    return nesne_tarafi, karsi_taraf

sol, sag = tarti_plani(20)
print('Nesne tarafı:', sol)
print('Karşı taraf:', sag)
```

Bu algoritma her döngüde hedefi yaklaşık üçte bire indirdiği için zaman karmaşıklığı $O(\log_3 n)$ olur. Örneğin 20 için $20=27-9+3-1$ gösterimini üretir: 9 ve 1 gram nesne tarafına; 27 ve 3 gram karşı tarafa yerleştirilir.

## Genel seçim kuralı

Her değeri boşluksuz tartabilmek için yeni bir ağırlık, öncekilerin kapsayabildiği aralığın hemen sonrasını erişilebilir kılmalıdır. Tek kefede önceki toplam $S$ ise yeni ağırlık en fazla $S+1$ olmalıdır. İki kefede ise en verimli seçim $2S+1$ değeridir. Böylece sırasıyla ikinin ve üçün kuvvetleri ortaya çıkar.

Sonuç olarak tartı problemi yalnızca teraziyle ilgili değildir. Sayı sistemlerinin neden güçlü olduğunu, durum sayısının kapasiteyi nasıl belirlediğini ve doğru temsil seçiminin bir problemi nasıl küçülttüğünü gösteren zarif bir algoritma dersidir.

![tarti-problemi-ve-80](/img/tarti-problemi-ve-80.svg)

