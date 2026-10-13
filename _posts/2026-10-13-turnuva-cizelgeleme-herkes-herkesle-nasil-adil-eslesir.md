---
layout: post
title: "Turnuva Çizelgeleme: Herkes Herkesle Nasıl Adil Eşleşir?"
math: true
categories: 
  - Program
tags: 
  - algoritma
  - python
  - çizelgeleme
  - turnuva
  - round-robin
  - optimizasyon
toc: true
image: /img/turnuva-cizelgeleme-herkes-84.png
---

Bir lig fikri ilk bakışta oldukça basittir: Her takım, diğer bütün takımlarla karşılaşsın. Ancak maçları haftalara dağıtmaya başladığımızda aynı takımın bir turda iki maça çıkması, bazı eşleşmelerin tekrarlanması veya bir takımın sürekli deplasmanda oynaması gibi sorunlar ortaya çıkar. Neyse ki **Round-Robin**, yani döner turnuva algoritması, bu organizasyon bilmecesini düzenli ve verimli biçimde çözer.
``

## Problemin matematiksel temeli

Turnuvada $n$ takım bulunduğunu ve her takım çiftinin yalnızca bir kez karşılaşacağını düşünelim. Toplam maç sayısı, takımlardan ikisini seçme problemiyle aynıdır:

$$M = \frac{n(n-1)}{2}$$

Örneğin 8 takımlı bir ligde $8 \times 7 / 2 = 28$ maç oynanır. Takım sayısı çiftse her turda $n/2$ maç yapılabilir ve sezon $n-1$ turda tamamlanır. Takım sayısı tekse her turda bir takım dinlenmek zorundadır. Bu durumda sisteme hayali bir **BAY** takımı eklenir; BAY ile eşleşen gerçek takım o turu maç yapmadan geçirir.

| Durum | Tur sayısı | Tur başına maç | Dinlenen takım |
|---|---:|---:|---|
| $n$ çift | $n-1$ | $n/2$ | Yok |
| $n$ tek | $n$ | $(n-1)/2$ | Her tur bir takım |
| Çift devreli lig | İlk devrenin iki katı | Aynı | Takım sayısına bağlı |

![turnuva-cizelgeleme-herkes-84](/img/turnuva-cizelgeleme-herkes-84.svg)


## Çember yöntemi nasıl çalışır?

Çember yönteminde takımlardan biri sabit tutulur, diğerleri her turun sonunda saat yönünde döndürülür. Listenin ilk yarısı ile ters çevrilmiş ikinci yarısı eşleştirilir. Böylece aynı eşleşme yeniden oluşmaz ve her takım, mümkün olan tüm rakiplerle tam bir kez karşılaşır.

Dört takım için turlar şöyle görünebilir:

| Tur | Maç 1 | Maç 2 |
|---:|---|---|
| 1 | A - D | B - C |
| 2 | A - C | D - B |
| 3 | A - B | C - D |

Buradaki dönüş rastgele değildir; algoritmanın tüm eşleşme uzayını sistematik biçimde dolaşmasını sağlar. Başka bir deyişle fikstür şapkadan tavşan çıkarmıyor, kombinatorikten takım çıkarıyor!

## Python ile fikstür üretimi

Aşağıdaki fonksiyon tek devreli bir lig çizelgesi oluşturur. Takım sayısı tek olduğunda BAY ekler, eşleşmeleri üretir ve her turdan sonra takımları döndürür:

```python
def fikstur_olustur(takimlar):
    takimlar = takimlar.copy()

    if len(takimlar) % 2 == 1:
        takimlar.append("BAY")

    takim_sayisi = len(takimlar)
    turlar = []

    for tur_no in range(takim_sayisi - 1):
        tur_maclari = []
        yarim = takim_sayisi // 2

        for i in range(yarim):
            ev_sahibi = takimlar[i]
            deplasman = takimlar[-(i + 1)]

            # Ev-deplasman dağılımını dengelemek için yönü değiştir.
            if (tur_no + i) % 2 == 1:
                ev_sahibi, deplasman = deplasman, ev_sahibi

            if "BAY" not in (ev_sahibi, deplasman):
                tur_maclari.append((ev_sahibi, deplasman))

        turlar.append(tur_maclari)

        # İlk takım sabit, diğer takımlar döner.
        takimlar = [takimlar[0], takimlar[-1]] + takimlar[1:-1]

    return turlar

lig = fikstur_olustur(["Kartallar", "Aslanlar", "Kaplanlar", "Şahinler"])

for tur, maclar in enumerate(lig, start=1):
    print(f"{tur}. Tur: {maclar}")
```

Listenin kopyalanması, fonksiyonun dışarıdan verilen özgün listeyi değiştirmesini engeller. Dönüş işleminin maliyeti maçların üretilmesiyle birlikte yaklaşık $O(n^2)$ olur. Zaten toplam eşleşme sayısı da karesel büyüdüğü için bu karmaşıklık kaçınılmaz ve uygundur.

## Adalet nasıl doğrulanır?

İyi bir fikstür yalnızca çalışmamalı, test de edilmelidir. Her takımın $n-1$ maç oynadığı, hiçbir takım çiftinin tekrarlanmadığı ve bir turda aynı takımın iki kez görünmediği kontrol edilmelidir. Ev sahibi ve deplasman sayıları arasındaki farkın mümkün olduğunca küçük tutulması da pratik adalet açısından önemlidir.

Çift devreli lig oluşturmak için ilk devredeki maçların tarafları değiştirilerek ikinci devre eklenebilir. Böylece `(A, B)` maçı daha sonra `(B, A)` olarak oynanır. Saha uygunluğu, yayın saati veya güvenlik gibi ek kısıtlar geldiğinde problem klasik Round-Robin çizelgelemeden çıkarak daha kapsamlı bir **kısıt tatmin** ve optimizasyon problemine dönüşür.
