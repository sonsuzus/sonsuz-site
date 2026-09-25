---
layout: post
title: "Mo Algoritmasını Ağaçlara Uyarlamak: Euler Turu ile Çevrimdışı Sorgular"
math: true
categories: 
  - Bilgi
tags: 
  - mo algoritması
  - ağaç algoritmaları
  - euler turu
  - lca
  - çevrimdışı sorgu
  - c++
toc: true
image: /img/mo-algoritmasini-agaclara-19.png
---

Bir dizideki aralık sorgularını akıllıca sıralayıp tekrar kullanılabilir hesaplarla hızlandıran Mo algoritması, küçük bir Euler turu numarasıyla ağaçlarda da çalışabilir. Özellikle iki düğüm arasındaki yolda kaç farklı renk bulunduğu gibi sorgular, ağacı doğrusal bir yapıya dönüştürdüğümüzde bloklar hâlinde işlenebilir.


![mo-algoritmasini-agaclara-19](/img/mo-algoritmasini-agaclara-19.svg)

``

## Önce klasik Mo mantığı

Elimizde $Q$ adet $[L,R]$ sorgusu bulunan, uzunluğu $N$ olan bir dizi düşünelim. Her sorguyu bağımsız çözmek pahalıdır. Mo algoritması sorguları önce $L$ değerinin ait olduğu bloğa, ardından $R$ değerine göre sıralar. Blok boyutu genellikle $B \approx \sqrt{N}$ seçilir.

İki işaretçiyle güncel aralığı koruruz. Yeni sorguya geçerken elemanları yalnızca ekler veya çıkarırız. Ekleme ve çıkarma $O(1)$ ise yaklaşık karmaşıklık şöyledir:

$$O((N+Q)\sqrt{N})$$

| Yaklaşım | Sorgu sırası | Ara sonuç kullanımı | Yaklaşık maliyet |
|---|---|---|---|
| Bağımsız çözüm | Geliş sırası | Yok | $O(NQ)$ |
| Dizi üzerinde Mo | Blok sırası | Var | $O((N+Q)\sqrt N)$ |
| Ağaç üzerinde Mo | Euler aralıkları | Var | Genellikle $O((N+Q)\sqrt N)$ |

## Ağacı diziye çevirmek

Ağaçta iki düğüm arasındaki yol doğrudan tek bir dizi aralığı değildir. Çözüm, DFS sırasında oluşturulan **Euler turudur**. Her düğümü ağaca girerken ve düğümden çıkarken kaydederiz. Böylece $N$ düğümlü ağaç için $2N$ uzunluğunda bir dizi oluşur.

Bir düğümün Euler aralığında kaç kez göründüğüne dikkat ederiz:

- Bir kez görünüyorsa etkin kümededir.
- İki kez görünüyorsa iki ziyaret birbirini götürür.
- Hiç görünmüyorsa sorgunun yolunda değildir.

Bu nedenle işaretçi bir Euler konumuna geldiğinde düğümü doğrudan eklemek yerine durumunu **toggle**, yani aç/kapat yaparız. Bu yaklaşım biraz ışık anahtarına benzer: aynı düğmeye ikinci kez basınca oda eski hâline döner.

```cpp
vector<int> euler, color, freq;
vector<bool> active;
int distinctColors = 0;

void toggle(int position) {
    int node = euler[position];
    int c = color[node];

    if (active[node]) {
        if (--freq[c] == 0) distinctColors--;
    } else {
        if (freq[c]++ == 0) distinctColors++;
    }
    active[node] = !active[node];
}
```

Burada `freq[c]`, etkin düğümler arasında `c` renginin kaç defa bulunduğunu tutar. `distinctColors` ise güncel yol üzerindeki farklı renk sayısıdır. Renk değerleri büyükse önce koordinat sıkıştırma uygulanmalıdır.

## LCA neden gerekiyor?

$u$ ve $v$ düğümleri için önce giriş zamanlarına göre sıralama yapılır. Eğer $u$, $v$ düğümünün atasıysa yol uygun bir Euler aralığıyla temsil edilir. Değilse aralık, yolun büyük bölümünü kapsar fakat $LCA(u,v)$ düğümünü dışarıda bırakır.

Bu durumda sorgu cevaplanmadan hemen önce LCA geçici olarak etkinleştirilir, sonuç kaydedilir ve ardından tekrar kapatılır. İkili kaldırma kullanıldığında LCA hesabı $O(\log N)$ sürede yapılabilir.

| Durum | Mo aralığı | Ek işlem |
|---|---|---|
| $u$, $v$'nin atası | `tin[u]..tin[v]` | Yok |
| Ayrı dallardalar | `tout[u]..tin[v]` | LCA geçici eklenir |

## Sorguları sıralamak

Her yol sorgusu, hesaplanan sol ve sağ Euler sınırlarıyla saklanır. Sonra klasik blok karşılaştırması uygulanır:

```cpp
sort(queries.begin(), queries.end(), [&](const Query& a, const Query& b) {
    int blockA = a.left / blockSize;
    int blockB = b.left / blockSize;
    if (blockA != blockB) return blockA < blockB;

    // Zikzak sıralama sağ işaretçinin hareketini azaltır.
    if (blockA & 1) return a.right > b.right;
    return a.right < b.right;
});
```

Ağaç üzerinde Mo algoritması çevrimdışıdır; cevap vermeden önce bütün sorguları bilmek gerekir. Buna karşılık güncelleme bulunmayan, çok sayıda yol sorgusu içeren problemlerde oldukça güçlüdür. Özet tarif şudur: ağacı Euler turuyla düzleştir, sorguları bloklara ayır, düğümleri toggle et ve LCA’nın eksik kaldığı köşeleri dikkatle tamamla. Gerisi, iki işaretçinin ormanda düzenli bir yürüyüşünden ibarettir.
