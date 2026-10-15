---
layout: post
title: "Problemler Arası İndirgeme: Zor Soruları Tanıdık Problemlere Dönüştürmek"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - indirgeme
  - karmaşıklık
  - np-tamlık
  - bilgisayar-bilimi
toc: true
image: /img/problemler-arasi-indirgeme-42.png
---

Bir problemi çözerken her zaman sıfırdan algoritma tasarlamak zorunda değiliz. Bazen elimizdeki soruyu, çözümünü bildiğimiz başka bir problemin kılığına sokmak yeterlidir. Bilgisayar biliminde bu yönteme **indirgeme (reduction)** denir. İndirgeme, algoritma tasarımından NP-tamlık ispatlarına kadar pek çok alanda kullanılan güçlü bir düşünme aracıdır.
``

## İndirgeme nedir?

Bir $A$ problemini $B$ problemine indirgemek, $A$ probleminin girdilerini $B$ problemine ait girdilere dönüştüren bir yöntem oluşturmaktır. Dönüşümden sonra $B$ için elde edilen cevap, $A$ probleminin cevabını belirlemelidir.

Polinom zamanda gerçekleştirilen indirgeme genellikle şu şekilde gösterilir:

$$A \leq_p B$$

Bu ifade, “$A$, polinom zamanda $B$ problemine indirgenebilir” anlamına gelir. Süreç üç adımdan oluşur:

1. $A$ problemine ait $x$ girdisini al.
2. Polinom zamanda $f(x)$ dönüşümünü uygula.
3. $B$ problemini $f(x)$ üzerinde çözerek $A$ için sonucu yorumla.

Dönüşümün temel doğruluk koşulu şöyledir:

$$x \in A \iff f(x) \in B$$

Yani özgün örnek “evet” örneğiyse dönüştürülen örnek de “evet” olmalıdır; aynı ilişki “hayır” cevapları için de korunmalıdır.

| Kavram | Görevi | Kritik nokta |
|---|---|---|
| Kaynak problem $A$ | Çözmek istediğimiz problem | Bilinmeyen veya zor olabilir |
| Hedef problem $B$ | Çözümünden yararlandığımız problem | Algoritması ya da zorluğu bilinir |
| Dönüşüm $f$ | Girdiyi yeni biçime çevirir | Polinom zamanda çalışmalıdır |
| Cevap eşlemesi | Sonucu geri yorumlar | Evet/hayır yapısını korumalıdır |

![problemler-arasi-indirgeme-42](/img/problemler-arasi-indirgeme-42.svg)


## Basit bir örnek: yolculuk problemi

Bir şehir ağında iki nokta arasında yol bulunup bulunmadığını düşünelim. Şehirleri düğüm, yolları kenar olarak temsil edersek soru doğrudan **graf erişilebilirliği** problemine dönüşür. Harita ayrıntıları artık önemli değildir; elimizde yalnızca bir grafik vardır.

```python
from collections import deque

def ulasilabilir_mi(graf, baslangic, hedef):
    kuyruk = deque([baslangic])
    ziyaret = {baslangic}

    while kuyruk:
        dugum = kuyruk.popleft()
        if dugum == hedef:
            return True

        for komsu in graf.get(dugum, []):
            if komsu not in ziyaret:
                ziyaret.add(komsu)
                kuyruk.append(komsu)

    return False
```

Bu kod, dönüştürülmüş graf üzerinde **genişlik öncelikli arama** yapar. Karmaşıklığı $O(V+E)$ düzeyindedir; burada $V$ şehir sayısını, $E$ ise yol sayısını temsil eder. Asıl indirgeme, gerçek dünyadaki şehir-yol modelini graf yapısına çevirmektir.

## Yön neden önemlidir?

İndirgemelerde ok yönü sıkça karıştırılır. $A \leq_p B$ yazıyorsa $A$ problemini çözmek için $B$ kullanılır. Dolayısıyla $B$, en az $A$ kadar güçlü veya zor olabilir.

| Amaç | Kurulması gereken indirgeme | Çıkarım |
|---|---|---|
| $A$ için algoritma geliştirmek | $A \leq_p B$ | $B$ hızlıysa $A$ da hızlı çözülebilir |
| $B$'nin zor olduğunu göstermek | $A \leq_p B$ | Zor $A$, $B$'ye aktarılır |
| $A$'nın zor olduğunu göstermek | $B \leq_p A$ | Bilinen zorluk $A$'ya taşınır |

Örneğin SAT probleminin zor olduğu biliniyorsa ve $SAT \leq_p X$ gösterilebiliyorsa, $X$ probleminin de en az SAT kadar zor olduğu sonucuna ulaşılır. Ancak ters yönde indirgeme yapmak aynı sonucu vermez; matematiksel ok küçük görünse de bütün ispatı ters çevirebilir.

## İyi bir indirgeme nasıl kurulur?

Önce iki problemin yapısal ortaklıkları bulunmalıdır. Değişkenler düğümlere, kısıtlar kenarlara veya seçimler mantıksal ifadelere karşılık gelebilir. Ardından dönüşümün polinom zamanda çalıştığı ve cevapları iki yönde de koruduğu kanıtlanır.

Kısacası indirgeme, “Bu problemi başka hangi dilde ifade edebilirim?” sorusudur. Doğru hedef seçildiğinde karmaşık bir soru tanıdık bir algoritmayla çözülebilir; bazen de çözüm üretmek yerine problemin neden zor olduğu gösterilir. Bu nedenle indirgeme yalnızca teknik bir ispat yöntemi değil, algoritmik düşünmenin en kullanışlı süper güçlerinden biridir.
