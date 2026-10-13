---
layout: post
title: "Domino Kaplama Problemi: Satranç Tahtasında Kombinatoriğin Gücü"
math: true
categories: 
  - Bilgi
tags: 
  - kombinatorik
  - domino
  - satranç tahtası
  - graf teorisi
  - algoritma
  - python
toc: true
image: /img/domino-kaplama-problemi-91.png
---

Bir satranç tahtasını boşluk bırakmadan domino taşlarıyla kaplamak ilk bakışta basit bir yapboz gibi görünür. Ancak tahtadan bazı kareler çıkarıldığında problem, kombinatoriğin en zarif sorularından birine dönüşür. Üstelik çözüm için her olasılığı denemek yerine boyama, değişmez ve graf teorisi gibi güçlü fikirlerden yararlanabiliriz.
``
## Problemin temel modeli

Standart bir satranç tahtası $8 \times 8 = 64$ kareden oluşur. Bir domino taşı yan yana bulunan tam iki kareyi örter. Dolayısıyla tahtanın tamamını kaplamak için

$$\frac{64}{2}=32$$

domino gerekir. Bu hesap bize gerekli bir koşul verir: Kaplanacak kare sayısı çift olmalıdır. Fakat çift olması, tek başına kaplanabilirlik garantisi değildir.

Örneğin tahtadan iki kare çıkarırsak geriye 62 kare kalır ve sayı hâlâ çifttir. Yine de çıkarılan karelerin konumu, kaplamayı imkânsız hâle getirebilir. İşin eğlenceli kısmı tam olarak burada başlar.

## Siyah-beyaz boyama ve değişmez fikri

Satranç tahtasında her yatay veya dikey komşu kare farklı renktedir. Bu nedenle yerleştirilen her domino mutlaka bir siyah ve bir beyaz kare kaplar. Başlangıçta tahtada 32 siyah ve 32 beyaz kare bulunur.

Karşılıklı iki köşe çıkarılsın. Bu köşeler aynı renktedir; örneğin ikisi de beyaz olsun. Geriye 32 siyah ve 30 beyaz kare kalır. Her domino renklerden birer tane tükettiği için bütün kareleri kaplamak mümkün değildir.

Bu argümanda korunan özelliğe **değişmez** denir. Domino hangi konuma yerleştirilirse yerleştirilsin kaplanan siyah ve beyaz kare sayıları eşittir.

| Tahta durumu | Siyah kare | Beyaz kare | Sonuç |
|---|---:|---:|---|
| Tam $8 \times 8$ tahta | 32 | 32 | Kaplanabilir |
| Zıt renkli iki kare çıkarılmış | 31 | 31 | Renk testi engel oluşturmaz |
| Aynı renkli iki köşe çıkarılmış | 32 | 30 | Kaplanamaz |

![domino-kaplama-problemi-91](/img/domino-kaplama-problemi-91.svg)


Burada önemli bir ayrıntı vardır: Renk sayılarının eşitliği gerekli koşuldur, fakat her zaman yeterli değildir. Bazı düzensiz bölgelerde renkler dengeli olsa bile geometrik sıkışmalar kaplamayı engelleyebilir.

## Problem bir grafa nasıl dönüşür?

Her kareyi bir düğüm, kenar paylaşan iki kareyi de bir bağlantı olarak düşünelim. Siyah kareler bir grubu, beyaz kareler diğer grubu oluşturur. Böylece **iki parçalı graf** elde edilir.

Bir domino, bağlı bir siyah-beyaz düğüm çiftini seçer. Tüm tahtayı kaplamak ise her düğümün tam bir kez kullanıldığı **mükemmel eşleşme** bulmakla aynıdır.

| Kaplama kavramı | Graf teorisindeki karşılığı |
|---|---|
| Kare | Düğüm |
| Komşu iki kare | Kenar |
| Bir domino | Eşleşme kenarı |
| Tam kaplama | Mükemmel eşleşme |

Bu bakış açısı sayesinde problem yalnızca satranç tahtaları için değil, delikli ve düzensiz bölgeler için de algoritmik olarak incelenebilir. Hopcroft–Karp algoritması iki parçalı graflarda eşleşmeyi yaklaşık $O(E\sqrt{V})$ zamanda bulur.

## Küçük tahtalarda Python ile arama

Aşağıdaki geri izleme kodu, verilen bölgenin kaplanabilir olup olmadığını sınar. Kod ilk boş kareyi seçer, sağa veya aşağıya domino koymayı dener ve çıkmazda önceki seçime döner.

```python
def kaplanabilir(kareler):
    kareler = set(kareler)

    def ara(kalan):
        if not kalan:
            return True

        r, c = min(kalan)
        for komsu in [(r + 1, c), (r, c + 1)]:
            if komsu in kalan:
                yeni = kalan - {(r, c), komsu}
                if ara(yeni):
                    return True
        return False

    return ara(kareler)

bolge = {(r, c) for r in range(4) for c in range(4)}
print(kaplanabilir(bolge))  # True
```

Bu yöntem öğreticidir ancak olası yerleşimlerin sayısı hızla büyüdüğü için büyük tahtalarda pahalıdır. Önce renk dengesi gibi ucuz testleri uygulamak, ardından eşleşme algoritmasına geçmek daha akıllıcadır.

## Sonuç

Domino kaplama problemi, basit görünen bir sorunun nasıl sayma, boyama ve graf teorisine açıldığını gösterir. En değerli ders şudur: Bazen çözümü inşa etmekten önce, çözümün neden var olamayacağını kanıtlamak çok daha kolaydır. Birkaç renk ve doğru seçilmiş bir değişmez, milyarlarca denemenin yerini tutabilir.
