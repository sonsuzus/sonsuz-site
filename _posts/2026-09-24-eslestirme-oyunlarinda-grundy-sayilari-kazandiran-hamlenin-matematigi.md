---
layout: post
title: "Eşleştirme Oyunlarında Grundy Sayıları: Kazandıran Hamlenin Matematiği"
math: true
categories: 
  - Bilgi
tags: 
  - grundy sayıları
  - nimber
  - kombinatoryal oyunlar
  - oyun teorisi
  - algoritma
  - dinamik programlama
toc: true
image: /img/eslestirme-oyunlarinda-grundy-83.png
---

Bir masanın üzerindeki çubukları, taşları veya eşleşebilen kartları sırayla kaldırdığınızı düşünün. Kurallar basit görünür: Hamle yapamayan kaybeder. Fakat hangi hamlenin kazandıracağını bulmak, özellikle bağımsız oyun parçaları birleştiğinde, sezgiden fazlasını gerektirir. Grundy sayıları ya da diğer adıyla **nimber**, her oyun durumunu tek bir sayıyla özetleyerek bu karmaşayı yönetilebilir bir matematik problemine dönüştürür.

``

## Önce oyun türünü tanıyalım

Sprague–Grundy teorisi, **tarafsız kombinatoryal oyunlar** için çalışır. Tarafsızlık, aynı konumda iki oyuncunun da aynı hamle seçeneklerine sahip olmasıdır. Ayrıca şans unsuru bulunmamalı, oyuncular bütün durumu görebilmeli ve oyun sonlu sayıda hamlede bitmelidir.

| Özellik | Uygun oyun | Uygun olmayan oyun |
|---|---|---|
| Hamle hakları | İki oyuncu için aynı | Oyuncuya göre değişiyor |
| Bilgi | Tamamen görünür | Gizli kartlar var |
| Rastlantı | Yok | Zar veya kura var |
| Bitiş | Sonlu | Sonsuza uzanabilir |

Klasik Nim bu şartları karşılar. Eşleştirme oyunları da durumları bağımsız bileşenlere ayrılabiliyorsa aynı matematiksel çerçevede incelenebilir.

## Grundy sayısı nasıl hesaplanır?

Bir durumun Grundy sayısı, o durumdan tek hamlede ulaşılabilen durumların Grundy sayılarında bulunmayan en küçük negatif olmayan tam sayıdır. Bu işlem **mex** yani “minimum excluded value” olarak adlandırılır:

$$
g(s)=\operatorname{mex}\{g(t)\mid t\text{, }s\text{ durumundan erişilebilir}\}
$$

Hamle yapılamayan bitiş durumunun değeri sıfırdır:

$$g(\text{bitiş})=0$$

Örneğin bir taş yığınından her turda 1 veya 2 taş alınabilsin. Sıfır taşın nimberi 0’dır. Bir taşlık durum yalnızca 0’a gidebildiği için $g(1)=\operatorname{mex}\{0\}=1$ olur. İki taşlık durum 0 ve 1’e ulaşır; dolayısıyla $g(2)=2$ bulunur. Üç taş ise Grundy değerleri 1 ve 2 olan durumlara gider. Bu kez eksik en küçük sayı 0’dır: $g(3)=0$.

| Taş sayısı | Ulaşılabilen nimberler | Grundy değeri |
|---:|---|---:|
| 0 | Yok | 0 |
| 1 | {0} | 1 |
| 2 | {0, 1} | 2 |
| 3 | {1, 2} | 0 |
| 4 | {2, 0} | 1 |

Sıfır değerli durum, sırası gelen oyuncu için kaybeden konumdur. Sıfırdan farklı değer ise doğru bir hamleyle rakibe sıfır değerli durum bırakılabileceğini gösterir.

## Bağımsız oyunları XOR ile birleştirmek

Asıl sihir, birden fazla bağımsız bileşen olduğunda ortaya çıkar. Toplam oyunun nimberi, bileşenlerin Grundy sayılarının normal toplamı değil, bitsel XOR işlemidir:

$$G=g_1\oplus g_2\oplus\cdots\oplus g_n$$

Eğer $G=0$ ise konum kaybedendir; $G\neq0$ ise en az bir hamle toplam XOR değerini sıfıra indirebilir. Kazanma stratejisi de tam olarak bu hamleyi aramaktır. Örneğin nimberleri 1, 2 ve 3 olan üç bileşen için $1\oplus2\oplus3=0$ çıkar. Kusursuz oynayan rakibe karşı bu durum pek iç açıcı değildir!

## Dinamik programlamayla hesaplama

Aşağıdaki Python kodu, bir yığından izin verilen miktarlarda taş alınan oyunun Grundy değerlerini hesaplar:

```python
def grundy_tablosu(n, hamleler):
    grundy = [0] * (n + 1)

    for tas in range(1, n + 1):
        erisilen = {
            grundy[tas - h]
            for h in hamleler
            if h <= tas
        }

        mex = 0
        while mex in erisilen:
            mex += 1
        grundy[tas] = mex

    return grundy

print(grundy_tablosu(12, [1, 2]))
```

Kod, küçük durumlardan başlayıp sonuçları saklar. Her konum için erişilebilir nimberler bir kümede toplanır ve ilk eksik sayı bulunur. Böylece aynı alt durum tekrar tekrar hesaplanmaz.

Bir eşleştirme oyunu grafik, kart grubu veya ayrı tahta bölgelerinden oluşuyorsa önce durumun bağımsız bileşenleri belirlenir. Ardından her bileşenin Grundy değeri hesaplanır ve XOR’lanır. Her olası hamle denenerek toplamı sıfır yapan seçenek seçilir.

Grundy sayıları geleceği tahmin eden sihirli bir küre değildir; bütün oyun ağacını zekice sıkıştıran bir etikettir. Kurallar tarafsız ve bileşenler bağımsız olduğunda “Bence bu hamle iyi” demek yerine, matematiksel olarak kazandıran hamleyi gösterebilirsiniz.

![eslestirme-oyunlarinda-grundy-83](/img/eslestirme-oyunlarinda-grundy-83.svg)

