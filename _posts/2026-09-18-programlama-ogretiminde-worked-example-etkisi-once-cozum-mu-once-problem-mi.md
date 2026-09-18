---
layout: post
title: "Programlama Öğretiminde Worked Example Etkisi: Önce Çözüm mü, Önce Problem mi?"
math: true
categories: 
  - Bilgi
tags: 
  - programlama eğitimi
  - worked example
  - bilişsel yük
  - öğrenme bilimi
  - problem çözme
  - algoritma
toc: true
---

Programlama öğrenirken doğrudan boş bir editörle karşılaşmak bazen yüzme bilmeden havuza atılmaya benzer. Öğrenci problemi, sözdizimini, algoritmayı ve hata mesajlarını aynı anda yönetmeye çalışır. **Worked example**, yani adım adım açıklanmış çözülmüş örnek yaklaşımı, bu yükü azaltmayı amaçlar. Peki öğrenciye önce çözüm mü gösterilmeli, yoksa düşünmesi için önce problem mi verilmelidir?
``
## Worked example etkisi nedir?

Worked example, yalnızca çalışan kod göstermek değildir. Problem tanımını, çözüm adımlarını, kararların gerekçelerini ve nihai kodu birlikte sunar. Öğrenci “Kod ne?” sorusunun yanında “Neden böyle yazıldı?” sorusuna da cevap bulur.

Bu yaklaşımın temeli **bilişsel yük kuramına** dayanır. Çalışma belleğimiz sınırlıdır. Basitleştirilmiş biçimde toplam zihinsel yükü şöyle gösterebiliriz:

$$L_{toplam} = L_{içsel} + L_{dışsal} + L_{öğrenme}$$

Burada $L_{içsel}$ konunun doğal zorluğunu, $L_{dışsal}$ kötü sunumdan veya gereksiz işlemlerden doğan yükü, $L_{öğrenme}$ ise zihinsel şema oluşturmaya ayrılan çabayı temsil eder. Acemi bir öğrenci çözümü sıfırdan ararken dışsal yük büyüyebilir. Çözülmüş örnek, bu arama maliyetini azaltarak dikkati algoritmik örüntülere yönlendirir.

## Önce örnek ve önce problem karşılaştırması

| Yaklaşım | Güçlü yanı | Riski | Uygun olduğu durum |
|---|---|---|---|
| Önce çözülmüş örnek | Bilişsel yükü azaltır, doğru modeli görünür kılar | Pasif biçimde kopyalanabilir | Yeni başlayanlar ve yeni kavramlar |
| Önce problem | Merak, üretkenlik ve ön bilgiyi harekete geçirir | Öğrenci uzun süre verimsizce takılabilir | Orta ve ileri düzey öğrenciler |
| Problem–örnek–problem | Deneme ile rehberliği birleştirir | Süre yönetimi gerektirir | Karma seviyeli sınıflar |
| Eksik örnek | Öğrenciyi kontrollü biçimde çözüme dahil eder | Boşluklar yanlış ayarlanabilir | Temeli oluşmaya başlayan öğrenciler |

Örneğin listedeki çift sayıları toplama problemini ele alalım. Acemiye yalnızca görev verildiğinde döngü, koşul, değişken ve çıktı kavramlarını aynı anda keşfetmesi beklenir. Bunun yerine açıklamalı bir örnek sunulabilir:

```python
def ciftleri_topla(sayilar):
    toplam = 0  # Sonucu biriktiren değişken

    for sayi in sayilar:
        if sayi % 2 == 0:  # Kalan sıfırsa sayı çifttir
            toplam += sayi

    return toplam

print(ciftleri_topla([3, 8, 5, 12]))  # 20
```

Bu kodda öğrenciye yalnızca satırlar değil, çözüm planı da açıklanmalıdır: listeyi sırayla gez, her elemanı test et, koşulu sağlayanı biriktir. Böylece somut kod ile soyut algoritma arasında bağlantı kurulur.

## Her zaman önce örnek mi?

Hayır. Öğrencinin uzmanlığı arttıkça ayrıntılı örnekler gereksizleşebilir. Buna **uzmanlığın tersine dönmesi etkisi** denir. Acemi için yararlı olan satır satır açıklama, deneyimli öğrenci için dikkat dağıtıcı olabilir.

Bu nedenle destek kademeli azaltılmalıdır:

1. Tam çözülmüş ve açıklanmış örnek gösterilir.
2. Benzer bir örnekte bazı satırlar boş bırakılır.
3. Öğrenci çözümü değiştirerek yeni gereksinim ekler.
4. Son olarak bağımsız bir problem çözer.

Örneğin ikinci aşamada `if` koşulu öğrenciye tamamlatılabilir; üçüncü aşamada ise toplam yerine çift sayıların adedi istenebilir. Böylece öğrenci kopyalamak yerine çözüm şemasını dönüştürür.

## En dengeli öğretim modeli

Yeni bir programlama yapısı öğretilirken genellikle **önce kısa bir problem denemesi, ardından worked example ve sonra benzer bağımsız problem** dengeli sonuç verir. İlk deneme birkaç dakika ile sınırlandırılmalıdır; amaç öğrenciyi çaresiz bırakmak değil, mevcut bilgisini etkinleştirmektir.

Sonuç olarak “önce çözüm mü, önce problem mi?” sorusunun tek cevabı yoktur. Acemilerde çözülmüş örnekler, deneyimli öğrencilerde problem çözme daha etkilidir. İyi öğretim, desteği öğrencinin seviyesine göre ayarlayan bir iskele gibidir: önce taşır, sonra yavaşça geri çekilir.
