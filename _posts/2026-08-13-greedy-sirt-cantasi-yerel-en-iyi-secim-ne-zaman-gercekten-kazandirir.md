---
layout: post
title: "Greedy Sırt Çantası: Yerel En İyi Seçim Ne Zaman Gerçekten Kazandırır?"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - greedy
  - sırt-çantası
  - dinamik-programlama
---

Açgözlü algoritmalar, her adımda o an için en avantajlı görünen seçimi yapar ve geriye dönüp kararlarını değiştirmez. Bu yaklaşım kulağa biraz aceleci gelse de doğru problemde inanılmaz hızlı ve zariftir. Sırt çantası problemi ise bu stratejinin sınırlarını görmek için mükemmel bir laboratuvardır: Aynı fikir, kesirli eşyalar için optimum sonucu verirken 0/1 sürümünde bizi tuzağa düşürebilir.
``
Önce problemimizi tanımlayalım. Her nesnenin değeri $v_i$, ağırlığı $w_i$ ve çantanın kapasitesi $W$ olsun. Amaç, seçilen nesnelerin toplam değerini büyütürken kapasiteyi aşmamaktır:

$$\max \sum_{i=1}^{n} v_i x_i \quad \text{koşuluyla} \quad \sum_{i=1}^{n} w_i x_i \le W$$

Buradaki kritik ayrım $x_i$ değişkenindedir. Kesirli sırt çantasında $0 \le x_i \le 1$ olabilir; yani bir nesnenin parçasını alabiliriz. 0/1 sırt çantasında ise $x_i \in \{0,1\}$ olur: Nesne ya tamamen alınır ya da hiç alınmaz.

| Özellik | Kesirli sırt çantası | 0/1 sırt çantası |
|---|---:|---:|
| Nesne bölünebilir mi? | Evet | Hayır |
| Greedy oran sıralaması | Optimum | Her zaman değil |
| Tipik çözüm | Sıralama + seçim | Dinamik programlama |
| Zaman karmaşıklığı | $O(n \log n)$ | Genellikle $O(nW)$ |

Greedy fikri basittir: Her nesne için birim ağırlık başına değeri, yani yoğunluğu hesaplarız:

$$r_i = \frac{v_i}{w_i}$$

Sonra nesneleri $r_i$ değerine göre azalan biçimde sıralar, çantaya sığdığı kadarını koyarız. Neden kesirli sürümde bu doğrudur? Değiş-tokuş (exchange) argümanı sayesinde. Optimum olduğu varsayılan bir çözüm, daha düşük yoğunluklu bir parçayı içerirken daha yüksek yoğunluklu bir nesneden alınabilecek miktar bırakıyorsa, düşük yoğunluklu parçayı yüksek yoğunluklu olanla değiştirebiliriz. Ağırlık aynı kalır, değer artar. Dolayısıyla optimum çözüm yüksek oranlı nesneleri önce tüketmek zorundadır.

Şimdi klasik olimpiyat tuzağına bakalım. Kapasite $W=50$ olsun; nesnelerimiz $(w,v)$ biçiminde sırasıyla $(10,60)$, $(20,100)$ ve $(30,120)$ olsun. Yoğunluklar $6$, $5$ ve $4$ tür. Greedy önce ilk iki nesneyi seçer: toplam ağırlık $30$, toplam değer $160$. Kalan 20 birime üçüncü nesne sığmaz. Fakat 0/1 sürümünde ikinci ve üçüncü nesneleri almak mümkündür: ağırlık $20+30=50$, değer $100+120=220$. Yerel olarak en parlak görünen ilk nesne, küresel optimumu engellemiştir.

Kesirli sürümde ise greedy yine kazanır: İlk iki nesneden sonra üçüncü nesnenin 20/30'u alınabilir. Ek değer $120 \cdot \frac{20}{30}=80$ olur ve toplam $240$ elde edilir.

Aşağıdaki Python kodu kesirli problemi çözer. Kod, nesneleri yoğunluğa göre sıralar; son nesne gerekirse bölünerek alınır.

```python
def fractional_knapsack(capacity, items):
    # items: (agirlik, deger) çiftleri
    ordered = sorted(items, key=lambda x: x[1] / x[0], reverse=True)
    total_value = 0.0
    chosen = []

    for weight, value in ordered:
        if capacity == 0:
            break
        amount = min(weight, capacity)
        fraction = amount / weight
        total_value += value * fraction
        chosen.append((weight, value, fraction))
        capacity -= amount

    return total_value, chosen

print(fractional_knapsack(50, [(10, 60), (20, 100), (30, 120)]))
```

Peki greedy ne zaman güvenilirdir? Problemde **greedy-choice property** bulunmalıdır: Bir optimum çözümün, greedy'nin ilk seçimini içeren başka bir optimum çözümü mutlaka var olmalıdır. Buna ek olarak problem, seçimin ardından kalan kısmın aynı türden daha küçük bir alt problem olduğu **optimal alt yapı** özelliğini taşımalıdır. Kesirli çanta bu iki koşulu sağlar; 0/1 çanta ise ilk koşulda sınıfta kalır.

Özetle, “en yüksek değer”, “en hafif nesne” veya “en iyi oran” gibi sezgiler tek başına algoritma kanıtı değildir. Greedy kullanmadan önce bir değiş-tokuş kanıtı arayın. Bulamıyorsanız, sırt çantasındaki bu örneğin fısıltısını dinleyin: Belki de aradığınız araç dinamik programlamadır.
