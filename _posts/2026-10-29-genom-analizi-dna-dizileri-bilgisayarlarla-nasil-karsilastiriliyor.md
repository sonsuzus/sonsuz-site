---
layout: post
title: "Genom Analizi: DNA Dizileri Bilgisayarlarla Nasıl Karşılaştırılıyor?"
math: true
categories: 
  - Bilgi
tags: 
  - genom
  - dna
  - biyoinformatik
  - algoritma
  - python
  - dizi-hizalama
toc: true
---

![genom-analizi-dna-72](/img/genom-analizi-dna-72.svg)


DNA, canlıların yapım talimatlarını taşıyan devasa bir metin gibi düşünülebilir. Ancak bu metnin alfabesinde yalnızca dört harf bulunur: adenin (`A`), sitozin (`C`), guanin (`G`) ve timin (`T`). İnsan genomu yaklaşık 3 milyar harften oluştuğu için iki DNA dizisini gözle karşılaştırmak pek gerçekçi değildir. İşte biyoinformatik algoritmaları burada devreye girer: Diziler arasındaki benzerlikleri, farklılıkları ve olası biyolojik ilişkileri bilgisayarlarla araştırır.

``

## DNA karşılaştırması neden yapılır?

Genom karşılaştırması; hastalıklarla ilişkili mutasyonları bulmak, türler arasındaki evrimsel yakınlığı ölçmek, virüs varyantlarını takip etmek ve kişiselleştirilmiş tedaviler geliştirmek için kullanılır. Temel amaç, iki dizide aynı kalan veya değişen bölgeleri belirlemektir.

Örneğin aşağıdaki dizileri ele alalım:

```text
Dizi 1: ACGTACG
Dizi 2: ACGTTCG
```

Burada beşinci karakter `A` yerine `T` olmuştur. Bu değişime **substitüsyon** denir. DNA'da ayrıca karakter eklenmesi anlamına gelen **insersiyon** ve karakter kaybı anlamına gelen **delesyon** görülebilir.

| Değişim | Örnek | Açıklama |
|---|---|---|
| Substitüsyon | `ACG` → `ATG` | Bir baz başka bir bazla değişir |
| İnsersiyon | `ACG` → `ACTG` | Diziye yeni bir baz eklenir |
| Delesyon | `ACG` → `AG` | Diziden bir baz silinir |

## Dizi hizalama mantığı

Bilgisayarlar DNA dizilerini karşılaştırırken karakterleri uygun konumlarda alt alta getirmeye çalışır. Bu işleme **dizi hizalama** denir. Her eşleşmeye pozitif, uyumsuzluğa veya boşluğa negatif puan verilerek en yüksek puanlı hizalama aranır.

Basit bir puan fonksiyonu şöyle tanımlanabilir:

$$
s(a,b)=
\begin{cases}
+2, & a=b \\
-1, & a\neq b
\end{cases}
$$

Diziye eklenen boşlukların puanı da örneğin $-2$ olabilir. Algoritma, toplam puanı

$$S=\sum_{i=1}^{n}s(x_i,y_i)$$

ifadesine göre en büyük yapan hizalamayı seçer. Böylece yalnızca kaç harfin aynı olduğuna değil, ekleme ve silmelerin diziyi nasıl kaydırdığına da dikkat edilir.

## Global ve lokal hizalama

İki temel yaklaşım bulunur:

| Yaklaşım | Algoritma | Kullanım amacı |
|---|---|---|
| Global hizalama | Needleman–Wunsch | Dizilerin tamamını karşılaştırır |
| Lokal hizalama | Smith–Waterman | En benzer alt bölgeleri bulur |

Global hizalama, uzunlukları ve kökenleri benzer diziler için uygundur. Lokal hizalama ise büyük bir genom içinde belirli bir gen bölgesini ararken daha kullanışlıdır. Her iki yöntem de **dinamik programlama** kullanır. Problem küçük alt problemlere ayrılır ve daha önce hesaplanan sonuçlar bir tabloda saklanır. Böylece aynı işlem tekrar tekrar yapılmaz.

## Python ile basit benzerlik hesabı

Aşağıdaki kod, eşit uzunluktaki iki DNA dizisinde aynı konumda bulunan bazların oranını hesaplar:

```python
def dna_benzerligi(dizi1, dizi2):
    if len(dizi1) != len(dizi2):
        raise ValueError("Diziler eşit uzunlukta olmalı")

    eslesme = sum(
        baz1 == baz2
        for baz1, baz2 in zip(dizi1, dizi2)
    )
    return eslesme / len(dizi1)

oran = dna_benzerligi("ACGTACG", "ACGTTCG")
print(f"Benzerlik: %{oran * 100:.2f}")
```

Bu örnek yaklaşık `%85.71` benzerlik verir. Ancak insersiyon ve delesyonları doğru değerlendiremez; çünkü boşluk ekleyerek hizalama yapmaz. Gerçek projelerde Biopython, BLAST ve minimap2 gibi araçlar tercih edilir.

## Milyarlarca harf nasıl aranıyor?

Klasik dinamik programlama algoritmalarının zaman karmaşıklığı genellikle $O(nm)$ düzeyindedir. Milyarlarca baz söz konusu olduğunda bu maliyet fazlasıyla büyür. BLAST gibi araçlar bu nedenle önce kısa ve umut vadeden eşleşmeleri bulur, ardından yalnızca bu bölgeleri ayrıntılı biçimde hizalar. Bu yaklaşım kesin sonucu garanti etmek yerine hız ile doğruluk arasında kullanışlı bir denge kurar.

Kısacası genom analizi, DNA'yı sıradan bir metin olarak görmekten çok daha fazlasıdır. Dizi algoritmaları, olasılık, dinamik programlama ve yüksek performanslı hesaplama birlikte çalışarak dört harfli biyolojik alfabenin içindeki yaşam hikâyesini okunabilir hâle getirir.
