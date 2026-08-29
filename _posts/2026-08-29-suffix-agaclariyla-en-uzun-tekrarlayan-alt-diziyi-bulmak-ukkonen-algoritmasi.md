---
layout: post
title: "Suffix Ağaçlarıyla En Uzun Tekrarlayan Alt Diziyi Bulmak: Ukkonen Algoritması"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - veri yapıları
  - ukkonen
  - suffix tree
  - string algoritmaları
---

Bir DNA dizisindeki yinelenen gen parçalarını, kaynak koddaki kopyalanmış blokları ya da büyük bir metindeki en sık tekrar eden ifadeleri aradığınızı düşünün. Tüm alt dizileri üretip karşılaştırmak ilk anda cazip görünür; fakat uzunluğu $n$ olan bir dizide aday sayısı yaklaşık $O(n^2)$ seviyesine çıkar. Suffix ağacı (son ek ağacı), bu karmaşayı düzenli bir yapıya dönüştürür ve en uzun tekrarlayan alt diziyi etkileyici biçimde verimli bulmamızı sağlar.

``

Bir suffix ağacı, metnin bütün son eklerini sıkıştırılmış bir trie içinde saklar. Örneğin `banana$` metninin son ekleri `banana$`, `anana$`, `nana$`, `ana$`, `na$`, `a$` ve `$` olur. Buradaki `$`, metinde hiç geçmeyen benzersiz bir bitiş sembolüdür. Ortak başlangıçlara sahip son ekler aynı yolu paylaşır. Böylece bir düğümden köke kadar okunan karakterler, metin içinde birden fazla yerde bulunan bir alt diziyi temsil eder.

En uzun tekrarlayan alt dizi (Longest Repeated Substring, LRS), en az iki son ekin ortak ön eki olan en uzun metindir. Suffix ağacı açısından tanım daha da güzel hâle gelir: **En derin iç düğümün yol etiketi LRS'dir.** Düğüm derinliği, kökten o düğüme kadar biriken karakter sayısıdır. Eğer düğümün yol etiketi `ana` ise ve alt ağacında en az iki yaprak varsa, `ana` en az iki kez geçiyordur.

| Yaklaşım | İnşa maliyeti | LRS arama maliyeti | Not |
|---|---:|---:|---|
| Tüm alt dizileri karşılaştırma | $O(n^2)$ veya daha kötü | Yüksek | Küçük girdiler dışında pahalıdır. |
| Sıralı suffix array | $O(n \log n)$ | $O(n)$ | Pratikte bellek dostudur. |
| Ukkonen ile suffix ağacı | $O(n)$ | $O(n)$ | Uygun varsayımlarla çevrim içi çalışır. |

Buradaki lineer zaman iddiası, alfabe erişiminin sabit zamanda yapılabildiği yaygın model içindir. Ukkonen algoritmasının sihri, metni soldan sağa **fazlar** hâlinde eklemesidir. Her fazda yeni karakter eklenir; aktif nokta, suffix link ve gösterim (remainder) bilgileri sayesinde daha önce yapılmış iş tekrar edilmez. Suffix link, benzer bağlama sahip düğümler arasında kısa yol görevi görür: `xα` etiketli bir iç düğümden `α` düğümüne geçiş sağlar. Bu bağlantılar, her yeni son eki kökten yeniden yürümek yerine algoritmanın hızını korur.

Aşağıdaki örnek, tam bir Ukkonen inşası yerine ağacı oluşturulduktan sonra LRS'yi derinlik öncelikli aramayla çıkarma fikrini gösterir. Her iç düğümde en derin yol etiketi adaydır:

```python
def longest_repeated(node, path=""):
    best = ""

    for edge_label, child in node.children.items():
        candidate = longest_repeated(child, path + edge_label)
        if len(candidate) > len(best):
            best = candidate

    # Yaprak olmayan düğüm, en az iki son ekin ortak yoludur.
    if len(node.children) > 1 and len(path) > len(best):
        best = path

    return best
```

Gerçek uygulamada kenarlar çoğu zaman karakter dizisi kopyaları olarak saklanmaz. Bunun yerine kaynak metindeki başlangıç ve bitiş indisleri tutulur. Böylece `edge_label` üretmek gerektiğinde alınır; bellek tüketimi azaltılır. Ayrıca yukarıdaki `len(node.children) > 1` kontrolü basitleştirilmiştir: Sıkıştırılmış ağaçta tekrarı doğrulamak için bir düğüm altındaki yaprak sayısını hesaplamak daha güvenlidir.

| Kavram | Görevi | LRS ile ilişkisi |
|---|---|---|
| Yaprak | Bir son eki temsil eder | Aynı alt ağaçtaki yapraklar tekrar sayısını gösterir. |
| İç düğüm | Ortak ön eki temsil eder | En derin uygun iç düğüm cevaptır. |
| Suffix link | İnşada hızlı geçiş sağlar | Ukkonen'in $O(n)$ hedefini destekler. |
| Bitiş sembolü `$` | Son ekleri ayırt eder | Bir son ekin diğerinin gölgesinde kalmasını engeller. |

Sonuçta süreç iki parçaya ayrılır: Ukkonen ile ağacı $O(n)$ zamanda kurmak ve ağacı dolaşarak maksimum derinlikli tekrar düğümünü bulmak. Toplam maliyet teorik olarak $T(n)=O(n)+O(n)=O(n)$ olur. Çok büyük metinlerde uygulama karmaşıklığı nedeniyle suffix array veya suffix automaton tercih edilebilse de, suffix ağacı tekrar eden örüntülerin geometrisini anlamak için hâlâ mükemmel bir veri yapısıdır.
