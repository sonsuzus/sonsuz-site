---
layout: post
title: "Slope Trick: Dışbükey Fonksiyonlarla Dinamik Programlamayı Hızlandırmak"
math: true
categories: 
  - Bilgi
tags: 
  - slope trick
  - dinamik programlama
  - dışbükey fonksiyonlar
  - algoritma
  - öncelik kuyruğu
  - c++
toc: true
---

Dinamik programlamada durum değişkeni bir sayı olduğunda, her olası değeri ayrı ayrı tutmak çoğu zaman pahalıdır. Slope trick, parçalı doğrusal dışbükey bir DP fonksiyonunu değerleriyle değil, eğiminin değiştiği noktalarla temsil eder. Böylece devasa bir koordinat aralığı, birkaç öncelik kuyruğu ve şaşırtıcı derecede az kodla yönetilebilir.
``

## Temel fikir: Değerleri değil, eğimleri sakla

Bir fonksiyon dışbükeyse eğimi soldan sağa giderken azalmaz. Örneğin

$$f(x)=\vert x-a\vert $$

fonksiyonunun eğimi $x<a$ bölgesinde $-1$, $x>a$ bölgesinde $+1$ olur. Eğimin değiştiği $a$ noktası bir **kırılma noktasıdır**. Fonksiyonun tamamını saklamak yerine minimum değerini ve bu kırılma noktalarını saklamak yeterlidir.

Slope trick çoğunlukla şu iki temel fonksiyonu kullanır:

- $(a-x)_+=max(0,a-x)$: soldan gelen ceza,
- $(x-a)_+=max(0,x-a)$: sağdan gelen ceza.

Mutlak değer de bunların toplamıdır:

$$\vert x-a\vert =(a-x)_+ + (x-a)_+$$

Bu küçük eşitlik, tekniğin İsviçre çakısıdır. Bir DP durumuna mutlak değer cezası eklemek, iki kırılma noktası eklemeye dönüşür.

| Klasik yaklaşım | Slope trick |
|---|---|
| Her $x$ için $DP[x]$ saklanır | Yalnızca kırılma noktaları saklanır |
| Koordinat aralığına bağlıdır | İşlem sayısına bağlıdır |
| Geçişler çoğu zaman $O(M)$ veya $O(M^2)$ | Tipik güncelleme $O(log N)$ |
| Ayrık tablolar için doğaldır | Dışbükey, parçalı doğrusal fonksiyonlar için doğaldır |

## İki heap ne anlatıyor?

Kırılma noktaları minimum bölgesinin iki tarafına ayrılır:

- `left`: maksimum heap; soldaki noktaların en büyüğünü verir.
- `right`: minimum heap; sağdaki noktaların en küçüğünü verir.
- `minimum`: fonksiyonun ulaşabildiği en küçük değer.

İdeal durumda minimum yapan değerler $[left.top(), right.top()]$ aralığındadır. Yeni bir kırılma noktası yanlış tarafa düşerse heap'ler dengelenir ve minimum değer, oluşan mesafe kadar artırılır. Başka bir deyişle veri yapısı, dışbükeyliği otomatik olarak korur.

Aşağıdaki C++ sınıfı temel güncellemeleri uygular:

```cpp
#include <bits/stdc++.h>
using namespace std;

struct SlopeTrick {
    using ll = long long;

    priority_queue<ll> left;
    priority_queue<ll, vector<ll>, greater<ll>> right;
    ll minimum = 0;

    // max(0, a - x) ekler: x, a'nın altında kalırsa ceza oluşur.
    void add_a_minus_x(ll a) {
        if (!left.empty() && left.top() > a) {
            ll p = left.top();
            left.pop();
            minimum += p - a;
            left.push(a);
            right.push(p);
        } else {
            right.push(a);
        }
    }

    // max(0, x - a) ekler: x, a'yı aşarsa ceza oluşur.
    void add_x_minus_a(ll a) {
        if (!right.empty() && right.top() < a) {
            ll p = right.top();
            right.pop();
            minimum += a - p;
            right.push(a);
            left.push(p);
        } else {
            left.push(a);
        }
    }

    // |x-a| ekler.
    void add_abs(ll a) {
        add_a_minus_x(a);
        add_x_minus_a(a);
    }

    ll get_minimum() const {
        return minimum;
    }
};
```

Örneğin $f(x)=sum_i \vert x-a_i\vert $ fonksiyonunu kurmak için her $a_i$ üzerinde `add_abs(a_i)` çağrılır. Sonuç, sayıların medyanında minimum olur; sınıf ise minimum toplam uzaklığı doğrudan hesaplar. Yani slope trick, medyan mantığının daha genel ve dinamik bir biçimi olarak da düşünülebilir.

## DP geçişlerinde nasıl görünür?

Genel bir durum şu biçimdedir:

$$DP_i(x)=c_i(x)+min_y(DP_{i-1}(y)+p(x,y))$$

Eğer $c_i$ ve geçiş cezası mutlak değerler, tek yönlü doğrusal cezalar veya bunların kaydırılmış biçimlerinden oluşuyorsa fonksiyon dışbükey kalır. Slope trick yapısına kırılma noktası ekleme, sabit ekleme, fonksiyonu yatay kaydırma ve prefix/suffix minimum alma işlemleri uygulanabilir.

Teknik her probleme uygun değildir. Kareli maliyetler, dışbükey olmayan geçişler veya minimum yerine karmaşık kombinasyonlar varsa farklı optimizasyonlar gerekebilir. Ancak DP fonksiyonunda sürekli `abs`, medyan, doğrusal ceza ve minimum ifadeleri görüyorsanız slope trick güçlü bir adaydır. Kısacası tabloyu büyütmek yerine fonksiyonun geometrisini saklar; DP de böylece matematikle küçük bir performans anlaşması imzalar.
