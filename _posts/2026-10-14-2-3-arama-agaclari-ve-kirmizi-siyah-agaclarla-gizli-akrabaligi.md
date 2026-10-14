---
layout: post
title: "2-3 Arama Ağaçları ve Kırmızı-Siyah Ağaçlarla Gizli Akrabalığı"
math: true
categories: 
  - Bilgi
tags: 
  - 2-3 ağaçları
  - kırmızı-siyah ağaçlar
  - veri yapıları
  - algoritmalar
  - dengeli ağaçlar
toc: true
image: /img/2-3-arama-17.png
---

İkili arama ağaçları hızlı arama sunar; fakat anahtarlar sıralı geldiğinde ağaç bir çubuk gibi uzayabilir. 2-3 arama ağaçları bu sorunu, her düğümde bir yerine birden fazla anahtar saklayarak çözer. Daha da ilginci, kırmızı-siyah ağaçlar bu çok anahtarlı yapının ikili ağaç kılığına girmiş hâli olarak yorumlanabilir.


![2-3-arama-17](/img/2-3-arama-17.svg)

``

## 2-3 ağacı nedir?

Bir 2-3 ağacındaki iç düğüm iki biçimden birine sahiptir:

- **2-düğüm:** Bir anahtar ve iki çocuk taşır.
- **3-düğüm:** İki sıralı anahtar ve üç çocuk taşır.

Bir 3-düğümde anahtarlar $a < b$ ise sol alt ağaçtaki değerler $a$'dan küçük, ortadakiler $a$ ile $b$ arasında, sağdakiler ise $b$'den büyüktür. Böylece ikili arama ağacının sıralama mantığı korunurken tek seviyede daha fazla bilgi tutulur.

Asıl denge garantisi şu değişmezden gelir: **Bütün yapraklar aynı derinliktedir.** Ağacın yüksekliği $h$ ve anahtar sayısı $n$ olduğunda en seyrek durumda her düğüm iki çocukludur:

$$2^h - 1 \leq n$$

En yoğun durumda ise dallanma üçe yaklaşır. Dolayısıyla yükseklik kabaca

$$\log_3(n) \leq h \leq \log_2(n+1)$$

aralığındadır. Arama, ekleme ve silme işlemleri bu nedenle en kötü durumda $O(\log n)$ sürer.

## Arama nasıl ilerler?

Her düğümde bir veya iki anahtar karşılaştırılır. Aranan değer küçükse sola, iki anahtarın arasındaysa ortaya, büyükse sağa gidilir. Yani bir seviyede daha çok karşılaştırma yapılabilir; buna karşılık ağaç genellikle daha kısadır.

| Özellik | İkili arama ağacı | 2-3 ağacı | Kırmızı-siyah ağaç |
|---|---|---|---|
| Düğümdeki anahtar | 1 | 1 veya 2 | 1 |
| Çocuk sayısı | En fazla 2 | 2 veya 3 | En fazla 2 |
| Denge garantisi | Yok | Tam yükseklik dengesi | Siyah yükseklik dengesi |
| En kötü arama | $O(n)$ | $O(\log n)$ | $O(\log n)$ |
| Uygulama yaklaşımı | Basit | Çok yollu | Döndürme ve renk değiştirme |

## Ekleme ve düğüm bölme

Yeni anahtar uygun yaprağa eklenir. Yaprak bir 2-düğümse anahtarlar sıralanır ve düğüm 3-düğüme dönüşür. Zaten iki anahtarı varsa geçici olarak üç anahtarlı bir taşma oluşur. Ortadaki anahtar ebeveyne gönderilir; küçük ve büyük anahtarlar iki ayrı düğüme bölünür. Ebeveyn de taşarsa işlem köke kadar devam eder. Kökün bölünmesi ağacın yüksekliğini yalnızca bir artırır.

Aşağıdaki Python kodu bu bölmenin özünü gösterir:

```python
def split_keys(keys):
    """Üç sıralı anahtarı iki düğüm ve bir terfi anahtarına ayırır."""
    if len(keys) != 3:
        raise ValueError("Bölme için tam olarak üç anahtar gerekir")

    left = [keys[0]]
    promoted = keys[1]
    right = [keys[2]]
    return left, promoted, right

keys = sorted([40, 10, 25])
left, promoted, right = split_keys(keys)
print(left, promoted, right)  # [10] 25 [40]
```

Gerçek uygulamada çocuk işaretçileri de uygun yeni düğümlere dağıtılır. Kodun önemli fikri, ortanca anahtarın yukarı çıkarak sıralamayı ve eşit yaprak derinliğini korumasıdır.

## Kırmızı-siyah bağlantısı

Bir 2-3 ağacını sıradan ikili bağlantılarla temsil etmek için 3-düğümdeki iki anahtar birbirine **kırmızı bağlantıyla** bağlanabilir. Tek başına duran 2-düğüm ise siyah bir düğüm olur:

- Siyah düğüm, bir 2-düğümü temsil eder.
- Siyah düğüm ile kırmızı çocuğu birlikte, bir 3-düğümü temsil eder.
- Kökten yapraklara eşit siyah düğüm sayısı, 2-3 ağacındaki eşit derinliğe karşılık gelir.

Özellikle sola yatık kırmızı-siyah ağaçlarda kırmızı bağlantı yalnızca sola eğilir. Ekleme sırasında yapılan sola döndürme, sağa döndürme ve renk değiştirme işlemleri; 2-3 ağacındaki düğüm birleştirme, bölme ve anahtar terfisinin ikili ağaç üzerindeki karşılıklarıdır.

Sonuç olarak 2-3 ağaçları dengeyi kavramsal olarak zarif biçimde garanti ederken kırmızı-siyah ağaçlar aynı fikri tek anahtarlı düğümlerle, pratik programlama ortamlarına daha uygun şekilde uygular. Renkler süs değil; görünmez 3-düğümleri işaretleyen küçük trafik lambalarıdır.
