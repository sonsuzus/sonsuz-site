---
layout: post
title: "Graf Renklendirme ve Welch-Powell Algoritması"
math: true
categories: 
  - Program
tags: 
  - graf
  - algoritma
  - welch-powell
  - python
  - ayrık-matematik
  - optimizasyon
toc: true
image: /img/graf-renklendirme-ve-10.png
---

Bir sınav programı hazırladığınızı, radyo frekanslarını dağıttığınızı veya birbirine komşu ülkeleri boyadığınızı düşünün. Çakışan öğelere aynı seçeneği vermemek gerekir. Graf renklendirme problemi, bu tür görevleri düğümler ve kenarlar üzerinden modelleyerek mümkün olduğunca az sayıda renk kullanmayı amaçlar. Welch-Powell algoritması ise hızlı ve anlaşılır bir sezgisel yaklaşım sunar.


![graf-renklendirme-ve-10](/img/graf-renklendirme-ve-10.svg)

``

## Graf renklendirme nedir?

Bir graf $G=(V,E)$ ile gösterilir. Burada $V$ düğüm kümesini, $E$ ise düğümler arasındaki kenarları temsil eder. Düğüm renklendirmede her $v \in V$ düğümüne bir renk atanır. Bir $(u,v) \in E$ kenarı varsa temel koşul şudur:

$$
c(u) \neq c(v)
$$

Buradaki $c(v)$, $v$ düğümünün rengidir. Grafı geçerli biçimde boyamak için gereken en küçük renk sayısına **kromatik sayı** denir ve $\chi(G)$ ile gösterilir.

| Graf türü | Kromatik sayı | Açıklama |
|---|---:|---|
| Kenarsız graf | $1$ | Hiçbir düğüm çatışmaz |
| İki parçalı graf | $2$ | Düğümler iki bağımsız kümeye ayrılır |
| Tek uzunluklu çevrim | $3$ | İki renk son kenarda çatışır |
| Tam graf $K_n$ | $n$ | Her düğüm diğerleriyle komşudur |

Genel bir grafın kromatik sayısını kesin olarak bulmak hesaplama açısından zordur. Welch-Powell çoğu zaman az renk kullanan bir çözüm üretir; ancak her graf için gerçek minimumu garanti etmez. Dolayısıyla elde ettiği renk sayısı $k$ ise genellikle

$$
\chi(G) \leq k
$$

ifadesini söyleyebiliriz.

## Welch-Powell nasıl çalışır?

Algoritmanın arkasındaki fikir, en fazla komşuya sahip düğümleri önce ele almaktır. Çünkü yüksek dereceli bir düğümü sona bırakmak, kullanılabilir renk seçeneklerini ciddi biçimde azaltabilir.

1. Düğümleri derecelerine göre azalan sırada diz.
2. İlk boyanmamış düğüme yeni bir renk ata.
3. Aynı renkle boyanmış düğümlere komşu olmayan diğer düğümlere de bu rengi ver.
4. Boyanmamış düğüm kalmayana kadar yeni renklerle işlemi tekrarla.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Welch-Powell | Hızlı ve kolay uygulanır | Minimum renk garantisi yoktur |
| Kaba kuvvet | Kesin sonucu bulabilir | Büyük graflarda çok yavaştır |
| Rastgele açgözlü | Basittir | Düğüm sırasına oldukça duyarlıdır |

## Python ile uygulama

Aşağıdaki fonksiyon, grafı komşuluk kümelerinden oluşan bir sözlük olarak alır. Sonuçta her düğümün hangi renk numarasını aldığını döndürür:

```python
def welch_powell(graph):
    # Düğümleri, komşu sayısına göre büyükten küçüğe sırala.
    ordered = sorted(graph, key=lambda node: len(graph[node]), reverse=True)
    colors = {}
    color_id = 0

    while len(colors) < len(graph):
        # Her tur yeni bir renk grubunu temsil eder.
        for node in ordered:
            if node in colors:
                continue

            conflict = any(
                colors.get(neighbor) == color_id
                for neighbor in graph[node]
            )

            if not conflict:
                colors[node] = color_id

        color_id += 1

    return colors


graph = {
    'A': {'B', 'C'},
    'B': {'A', 'C', 'D'},
    'C': {'A', 'B', 'D'},
    'D': {'B', 'C', 'E'},
    'E': {'D'}
}

result = welch_powell(graph)
print(result)
print('Kullanılan renk:', len(set(result.values())))
```

`conflict` kontrolü, incelenen düğümün komşularından herhangi birinin mevcut rengi kullanıp kullanmadığını belirler. Çakışma yoksa aynı renk güvenle atanır. Sıralama yaklaşık $O(\vert V\vert \log \vert V\vert )$ maliyetindedir; komşuluk kontrolleriyle toplam süre kullanılan veri yapısına ve grafın yoğunluğuna bağlıdır.

## Nerelerde kullanılır?

Graf renklendirme; sınavların aynı saate çakışmadan yerleştirilmesinde, işlemci yazmaçlarının dağıtılmasında, kablosuz ağ kanallarının atanmasında ve harita boyamada kullanılabilir. Welch-Powell özellikle hızlı, kabul edilebilir ve açıklanabilir bir çözüm gerektiğinde güçlü bir başlangıçtır. Daha iyi sonuç için farklı eşit derece sıralamaları denenebilir ve bulunan çözümler arasından en az renk kullanan seçilebilir.
