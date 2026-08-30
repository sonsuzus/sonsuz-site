---
layout: post
title: "Convex Hull Trick ile Dinamik Programlamayı Roketlemek"
math: true
categories: 
  - Bilgi
tags: 
  - dinamik programlama
  - convex hull trick
  - algoritmalar
toc: true
---

Bazı dinamik programlama problemleri ilk bakışta masum görünür: Her durum için önceki tüm durumları denersiniz, en iyisini seçersiniz. Ancak bu yaklaşım çoğu zaman $O(n^2)$ maliyet üretir. Convex Hull Trick (CHT), geçiş maliyetinin doğrusal fonksiyonlara ayrıştığı özel durumlarda bu taramayı akıllı bir geometrik sorguya dönüştürür. Doğru koşullarda karmaşıklığı $O(n \log n)$, hatta $O(n)$ seviyesine indirebilir.
``

Temel fikir şu DP biçiminden doğar:

$$dp[i] = \min_{j < i} \{dp[j] + m_j \cdot x_i + b_j\}$$

Burada her önceki $j$ durumu, $y = m_jx + b_j$ biçiminde bir doğru olarak düşünülebilir. Yeni $i$ durumu geldiğinde ise $x_i$ noktasında tüm doğruların en küçük değerini sorarız. Yani DP tablosunu doldurmak, aslında bir doğru koleksiyonunda minimum sorgusu yapmaya dönüşür. Maksimum arıyorsanız da aynı fikir çalışır; yalnızca karşılaştırma yönünü değiştirmeniz gerekir.

Örneğin maliyetiniz $C(j,i)=a_jx_i+b_j$ biçimine getirilebiliyorsa, $dp[j]+b_j$ sabit kısmını doğrunun kesişimine katarsınız. Her $j$, eğimi $a_j$, sabit terimi $dp[j]+b_j$ olan bir çizgi üretir. İşte geometrinin algoritmaya gizlice giriş yaptığı an budur.

| Yaklaşım | Her durumdaki işlem | Toplam karmaşıklık | Uygun senaryo |
|---|---:|---:|---|
| Kaba kuvvet DP | Tüm $j<i$ değerlerini dene | $O(n^2)$ | Küçük $n$ |
| Li Chao Tree | Doğru ekle ve nokta sorgula | $O(n\log X)$ | Sıralı olmayan eğim ve sorgular |
| Monoton CHT | Kuyrukta doğru tut | $O(n)$ | Eğimler ve sorgular sıralı |

### Geometrik sezgi: Neden bazı doğrular çöpe gider?

Minimum sorgularında yalnızca alt zarfı oluşturan doğrular önemlidir. Bir doğru, diğer iki doğru tarafından her bölgede geride bırakılıyorsa gelecekte hiçbir sorguda kazanamaz. Monoton CHT bu nedenle doğruları bir kuyrukta tutar ve gereksiz olanları siler.

Üç doğru için kesişim hesaplamak yerine kayan nokta hatalarından kaçınmak adına çapraz çarpım kullanılır. $l_1$, $l_2$, $l_3$ doğruları eğim sırasıyla ekleniyorsa, $l_2$ aşağıdaki koşulda gereksizdir:

$$\frac{b_3-b_1}{m_1-m_3} \leq \frac{b_2-b_1}{m_1-m_2}$$

Bölme yapmak yerine işaretlere dikkat ederek iki taraf çapraz çarpılır. Büyük sayılarda `long long` yetmeyebileceği için C++ tarafında `__int128` kullanmak oldukça güvenlidir.

### Monoton sorgulu CHT iskeleti

Aşağıdaki örnek, eğimlerin azalan; sorgu $x$ değerlerinin artan olduğu minimum problemi içindir. `query` sırasında artık avantajlı olmayan ön doğrular kuyruktan çıkarılır.

```cpp
struct Line {
    long long m, b;
    long long value(long long x) const { return m * x + b; }
};

bool useless(Line a, Line b, Line c) {
    return (__int128)(b.b - a.b) * (a.m - c.m)
         >= (__int128)(c.b - a.b) * (a.m - b.m);
}

deque<Line> hull;

void addLine(long long m, long long b) {
    Line current{m, b};
    while (hull.size() >= 2 &&
           useless(hull[hull.size()-2], hull.back(), current))
        hull.pop_back();
    hull.push_back(current);
}

long long query(long long x) {
    while (hull.size() >= 2 &&
           hull[0].value(x) >= hull[1].value(x))
        hull.pop_front();
    return hull.front().value(x);
}
```

Bu kodun sihri, her doğrunun kuyruğa bir kez girip en fazla bir kez çıkmasındadır. Böylece tüm ekleme ve sorguların amortize maliyeti $O(n)$ olur. Fakat sıralılık varsayımlarını bozarsanız bu yapı yanlış sonuç verebilir; o noktada Li Chao Tree daha esnek bir seçenektir.

Son olarak, her doğrusal görünen DP geçişi CHT adayı değildir. İfadeyi gerçekten $m_jx_i+b_j$ formuna ayırabilmeli, minimum/maksimum yönünü doğru kurmalı ve eşit eğimli doğruları özel ele almalısınız. Bu üç kontrol yapıldığında Convex Hull Trick, karekök değil ama kare karmaşıklığı ortadan kaldıran etkileyici bir optimizasyon silahına dönüşür.
