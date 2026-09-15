---
layout: post
title: "Mo Algoritması: Çevrimdışı Aralık Sorgularını Akıllıca Gruplamak"
math: true
categories: 
  - Bilgi
tags: 
  - mo algoritması
  - çevrimdışı sorgular
  - algoritma
  - cpp
  - karekök ayrıştırma
  - veri yapıları
toc: true
---

Bir dizide yüzlerce kez “$[L,R]$ aralığında kaç farklı sayı var?” diye sorulduğunu düşünün. Her sorguyu baştan sona taramak doğru sonucu verir; fakat büyük verilerde işlemci kısa sürede maraton koşmuş gibi yorulur. Mo algoritması, sorguların sırasını değiştirerek mevcut aralığı küçük adımlarla günceller ve bu tekrarları ciddi ölçüde azaltır.

``

## Temel fikir: Cevapları değil, sorguları sırala

Mo algoritması, cevapları önceki sorgudan yararlanarak hesaplanabilen **çevrimdışı aralık sorguları** için kullanılır. Çevrimdışı sözcüğü, bütün sorguların önceden bilindiği ve sonuçların giriş sırasından farklı bir sırada hesaplanabildiği anlamına gelir. Sonuçlar daha sonra özgün sorgu kimlikleriyle doğru sıraya yerleştirilir.

Dizi uzunluğu $N$, sorgu sayısı $Q$ olsun. Saf yaklaşımda her sorgu en fazla $N$ eleman gezer:

$$T(N,Q)=O(NQ)$$

Mo algoritması diziyi yaklaşık $B=\sqrt{N}$ boyutlu bloklara ayırır. Sorgular önce sol uçlarının ait olduğu bloğa, ardından sağ uçlarına göre sıralanır. Böylece iki sorgu arasında geçiş yaparken $L$ ve $R$ işaretçileri çoğunlukla kısa mesafeler ilerler.

| Yaklaşım | Çalışma biçimi | Yaklaşık karmaşıklık | Uygun durum |
|---|---|---:|---|
| Saf tarama | Her aralığı yeniden gezer | $O(NQ)$ | Küçük veri |
| Prefix sum | Ön hesaplama yapar | $O(N+Q)$ | Toplam gibi terslenebilir işlemler |
| Segment tree | Çevrimiçi sorgulara cevap verir | $O((N+Q)\log N)$ | Güncelleme gereken problemler |
| Mo algoritması | Sorguları yeniden sıralar | $O((N+Q)\sqrt N)$ | Ekleme ve silmesi ucuz istatistikler |

## Aralık nasıl hareket eder?

Başlangıçta aktif aralık boştur. Yeni sorgu $[L,R]$ geldiğinde mevcut sol ve sağ sınırlar hedefe ulaşana kadar dört işlem uygulanır:

- Sol sınırı sola çek: yeni elemanı ekle.
- Sol sınırı sağa it: çıkan elemanı sil.
- Sağ sınırı sağa çek: yeni elemanı ekle.
- Sağ sınırı sola it: çıkan elemanı sil.

Örneğin aktif aralık $[3,7]$, sonraki sorgu $[5,9]$ ise 3 ve 4 silinir; 8 ve 9 eklenir. Aralık sıfırdan hesaplanmaz. Algoritmanın tasarrufu tam olarak buradan gelir.

## C++ ile farklı eleman sayısı

Aşağıdaki örnek, her sorgu aralığındaki farklı değerlerin sayısını hesaplar. `freq` dizisi değerlerin aktif aralıkta kaç kez bulunduğunu, `distinct` ise frekansı sıfırdan büyük değerlerin sayısını tutar.

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Query {
    int l, r, id, block;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (int &x : a) cin >> x;

    int blockSize = max(1, (int)sqrt(n));
    vector<Query> queries(q);
    for (int i = 0; i < q; ++i) {
        cin >> queries[i].l >> queries[i].r;
        --queries[i].l;
        --queries[i].r;
        queries[i].id = i;
        queries[i].block = queries[i].l / blockSize;
    }

    sort(queries.begin(), queries.end(), [](const Query& x, const Query& y) {
        if (x.block != y.block) return x.block < y.block;
        if (x.block & 1) return x.r > y.r;
        return x.r < y.r;
    });

    vector<int> freq(1000001, 0), answer(q);
    int left = 0, right = -1, distinct = 0;

    auto add = [&](int index) {
        if (freq[a[index]]++ == 0) ++distinct;
    };
    auto remove = [&](int index) {
        if (--freq[a[index]] == 0) --distinct;
    };

    for (const Query& query : queries) {
        while (left > query.l) add(--left);
        while (right < query.r) add(++right);
        while (left < query.l) remove(left++);
        while (right > query.r) remove(right--);
        answer[query.id] = distinct;
    }

    for (int value : answer) cout << value << endl;
}
```

Sağ uçların tek bloklarda azalan, çift bloklarda artan sıralanması küçük ama etkili bir optimizasyondur. Bu “yılan düzeni”, sağ işaretçinin blok geçişlerinde gereksiz yere başa dönmesini önler.

## Ne zaman tercih edilmeli?

Mo algoritması sihirli bir değnek değildir. Sorgular çevrimiçiyse, arada güncellemeler varsa veya `add/remove` işlemleri pahalıysa başka yapılar daha uygun olabilir. Ayrıca değerler çok büyükse doğrudan frekans dizisi yerine koordinat sıkıştırma kullanılmalıdır.

Özetle Mo algoritması, hesaplamayı hızlandırmak için veriyi değil **iş sırasını** düzenler. Bazen en iyi optimizasyon daha hızlı koşmak değil, ziyaret edilecek durakları daha akıllıca sıralamaktır.
