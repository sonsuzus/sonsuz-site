---
layout: post
title: "Amortize Analiz: Pahalı İşlemleri Uzun Vadede Ucuzlatmak"
math: true
categories: 
  - Bilgi
tags: 
  - amortize analiz
  - algoritma
  - veri yapıları
  - zaman karmaşıklığı
  - dinamik dizi
toc: true
image: /img/amortize-analiz-pahali-93.png
---

Bir algoritmadaki tek bir işlemin pahalı olması, algoritmanın genel olarak verimsiz olduğu anlamına gelmez. Bazen nadiren gerçekleşen maliyetli işlemler, çok sayıdaki ucuz işlem arasında kaybolur. Amortize analiz, tam da bu tabloya bakarak bir işlem dizisinin uzun vadeli ortalama maliyetini hesaplamamızı sağlar.

``

## Amortize analiz nedir?

Amortize analiz, bir işlemin olasılıksal ortalamasını değil, **en kötü durumda oluşabilecek işlem dizisinin ortalama maliyetini** inceler. Bu nedenle ortalama durum analizinden farklıdır: Kullanıcı davranışı veya rastgele veri dağılımı hakkında varsayım yapmaz.

$n$ işlemden oluşan bir dizinin toplam maliyeti $T(n)$ ise işlem başına amortize maliyet şöyle hesaplanır:

$$
A(n) = \frac{T(n)}{n}
$$

Örneğin toplam maliyet $T(n)=3n+10$ ise amortize maliyet:

$$
A(n)=\frac{3n+10}{n}=3+\frac{10}{n}=O(1)
$$

Burada bazı işlemler tek başına pahalı olsa bile uzun vadede her işlem sabit maliyetli kabul edilebilir.

| Analiz türü | İncelenen durum | Varsayım gerekir mi? | Sonuç örneği |
|---|---|---:|---:|
| En iyi durum | En avantajlı girdi | Hayır | $\Omega(1)$ |
| En kötü durum | En maliyetli tek işlem | Hayır | $O(n)$ |
| Ortalama durum | Olası girdilerin ortalaması | Evet | Beklenen maliyet |
| Amortize analiz | En kötü işlem dizisinin ortalaması | Hayır | İşlem başına $O(1)$ |

## Klasik örnek: Dinamik dizi

Dinamik bir dizinin kapasitesi dolduğunda daha büyük bir alan ayrılır ve eski elemanlar yeni alana kopyalanır. Normal bir ekleme $O(1)$ sürerken yeniden boyutlandırma işlemi $O(n)$ maliyetli olabilir.

```python
class DynamicArray:
    def __init__(self):
        self.capacity = 1
        self.size = 0
        self.data = [None] * self.capacity

    def append(self, value):
        if self.size == self.capacity:
            self._resize()

        self.data[self.size] = value
        self.size += 1

    def _resize(self):
        self.capacity *= 2
        new_data = [None] * self.capacity

        for i in range(self.size):
            new_data[i] = self.data[i]

        self.data = new_data
```

Bu kodda `_resize`, mevcut elemanları kopyalayarak kapasiteyi iki katına çıkarır. Boyutlandırmalar $1,2,4,8,\ldots$ elemanda gerçekleşir. $n$ ekleme boyunca yapılan toplam kopyalama sayısı:

$$
1+2+4+\cdots+\frac{n}{2}<n
$$

Normal eklemelerin maliyeti de $n$ olduğundan toplam maliyet $2n$ civarındadır. Böylece işlem başına maliyet:

$$
\frac{2n}{n}=O(1)
$$

Tek bir ekleme $O(n)$ sürebilir; ancak `append` işleminin amortize maliyeti $O(1)$ olur. Pahalı taşınma masrafı, önceki ucuz eklemelere dağıtılmıştır.

## Üç temel amortize analiz yöntemi

### 1. Toplam maliyet yöntemi

Tüm işlem dizisinin gerçek maliyeti hesaplanır ve işlem sayısına bölünür. Dinamik dizi örneğinde kullandığımız yaklaşım budur.

### 2. Muhasebe yöntemi

Ucuz işlemlerden gerçek maliyetlerinden biraz daha fazla ücret alınır. Aradaki kredi, gelecekteki pahalı işlemleri karşılamak üzere saklanır. Bir eklemenin gerçek maliyeti $1$ olsa da ona $3$ kredi biçtiğimizi düşünebiliriz. Fazladan kalan krediler yeniden boyutlandırmayı öder; algoritma adeta kendi kumbarasını taşır.

### 3. Potansiyel yöntemi

Veri yapısında biriken gelecekteki işi matematiksel bir potansiyel fonksiyonuyla gösteririz. Amortize maliyet:

$$
\hat{c_i}=c_i+\Phi(D_i)-\Phi(D_{i-1})
$$

Burada $c_i$ gerçek maliyet, $\Phi(D_i)$ ise işlemden sonraki potansiyeldir. Potansiyel artıyorsa geleceğe kredi bırakılır; azalıyorsa biriktirilen kredi pahalı işlemi karşılar.

| Yöntem | Temel fikir | Kullanışlı olduğu durum |
|---|---|---|
| Toplam | Bütün maliyeti işlemlere böl | Düzenli işlem dizileri |
| Muhasebe | Fazla ücretle kredi biriktir | Sezgisel açıklamalar |
| Potansiyel | Veri yapısındaki enerjiyi ölç | Karmaşık yapılar ve ispatlar |

Amortize analiz, tek bir kötü ana bakıp paniğe kapılmak yerine filmin tamamını izler. Dinamik diziler, hash tabloları, yığıt işlemleri ve birleşim-bulma yapıları bu yöntemle daha doğru değerlendirilir. Kısacası soru yalnızca “Bu işlem ne kadar pahalı?” değil, “Bu maliyet uzun bir yolculuk boyunca kaç işleme paylaşılıyor?” olmalıdır.

![amortize-analiz-pahali-93](/img/amortize-analiz-pahali-93.svg)

