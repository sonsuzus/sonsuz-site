---
layout: post
title: "Python Dunder Metotları: Operatörlerin Görünmez Yönetmeni"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - dunder
  - operatör aşırı yükleme
  - nesne yönelimli programlama
  - özel metotlar
toc: true
image: /img/python-dunder-metotlari-20.png
---

Python’da `a + b` yazdığımızda masum görünen bir toplama işlemi gerçekleşir. Ancak perdenin arkasında Python, nesnelerin özel metotlarını çağırarak küçük bir tiyatro sahneler. Bu dunder metotları kodu doğal ve okunabilir hâle getirebilir; yanlış kullanıldıklarında ise `+` işaretinin toplama mı, birleştirme mi, yoksa bambaşka bir sihir mi yaptığı belirsizleşir.

``

## Dunder metotları nedir?

“Dunder”, **double underscore** ifadesinin kısaltmasıdır. `__add__`, `__len__` ve `__eq__` gibi başında ve sonunda çift alt çizgi bulunan metotlar, Python veri modelinin belirlediği protokolleri uygular. Bunlar normalde doğrudan çağrılmak yerine dilin sözdizimi tarafından örtük biçimde kullanılır.

Örneğin aşağıdaki iki ifade kavramsal olarak ilişkilidir:

```python
sonuc = a + b
sonuc = a.__add__(b)
```

Yine de ikinci biçimi doğrudan kullanmak önerilmez. Çünkü gerçek operatör çözümleme süreci, sağ taraftaki nesnenin yansıtılmış metodunu ve `NotImplemented` sonucunu da hesaba katar.

Bir ikili operatörü kabaca şu fonksiyonla düşünebiliriz:

$$
f(a,b)=a.__add__(b)
$$

İlk nesne işlemi desteklemiyorsa Python, uygun koşullarda `b.__radd__(a)` metodunu dener. Yani daha doğru zihinsel model şöyledir:

$$
a+b \rightarrow a.__add__(b) \;\text{ve gerekirse}\; b.__radd__(a)
$$

| Sözdizimi | İlk denenen metot | Alternatif metot |
|---|---|---|
| `a + b` | `a.__add__(b)` | `b.__radd__(a)` |
| `a - b` | `a.__sub__(b)` | `b.__rsub__(a)` |
| `a * b` | `a.__mul__(b)` | `b.__rmul__(a)` |
| `a == b` | `a.__eq__(b)` | `b.__eq__(a)` |
| `a < b` | `a.__lt__(b)` | `b.__gt__(a)` |

## Anlamlı bir aşırı yükleme örneği

Vektörlerde toplama, matematiksel beklentiyle uyumludur. Bu nedenle `+` operatörünü aşırı yüklemek burada şaşırtıcı değildir:

```python
class Vektor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, diger):
        if not isinstance(diger, Vektor):
            return NotImplemented
        return Vektor(self.x + diger.x, self.y + diger.y)

    def __repr__(self):
        return f"Vektor({self.x}, {self.y})"

v1 = Vektor(2, 3)
v2 = Vektor(4, 1)
print(v1 + v2)  # Vektor(6, 4)
```

Burada $\vec{v_1}+\vec{v_2}=(2+4,3+1)=(6,4)$ bağıntısı uygulanır. `NotImplemented` döndürmek özellikle önemlidir: Bu değer bir hata değildir; Python’a “Bu türü ben işleyemiyorum, diğer seçeneği dene” mesajını verir. Doğrudan `False` döndürmek veya alakasız bir istisna fırlatmak, operatör protokolünü bozabilir.

## Sihir ne zaman kara büyüye dönüşür?

Bir `Sepet` sınıfında `sepet + urun` ifadesinin ürünü sepete ekleyip mevcut nesneyi değiştirdiğini düşünelim. Kullanıcılar genellikle `+` işleminin yeni bir değer üretmesini bekler. Gizli mutasyon şu şaşırtıcı duruma yol açabilir:

```python
yedek = sepet
sonuc = sepet + urun
# Hem sepet hem de yedek değişmiş olabilir!
```

Bu davranış yerine `urun_ekle()` gibi açık bir metot veya yerinde değişikliği anlatan `__iadd__` tercih edilebilir. Operatörün görsel olarak kısa olması, etkisinin de basit olduğu anlamına gelmez.

Benzer riskler `__eq__` ve `__hash__` ilişkisinde görülür. Eşit kabul edilen iki nesnenin hash değerleri de eşit olmalıdır:

$$
a=b \Rightarrow hash(a)=hash(b)
$$

Bu kural bozulursa sözlük ve kümelerde hayalet kayıtlar ortaya çıkabilir. Ayrıca `__len__` sıfır döndürdüğünde nesne `False` kabul edilir; `__bool__` tanımlamak da koşulların anlamını değiştirebilir.

## Güvenli kullanım pusulası

Operatör aşırı yükleme, alanın doğal matematiğini veya yerleşik Python beklentilerini yansıtmalıdır. Tür uyumsuzluğunda `NotImplemented` kullanılmalı, yan etkiler açıkça belgelenmeli ve eşitlik-hash sözleşmesi korunmalıdır. Operatör önceliğinin dunder metotlarıyla değiştirilemeyeceği de unutulmamalıdır.

Kısacası dunder metotları görünmez yönetmenlerdir: İyi yönetildiklerinde kod akıcı bir filme dönüşür; her operatöre beklenmedik görevler verildiğinde ise izleyici senaryoyu takip edemez.

![python-dunder-metotlari-20](/img/python-dunder-metotlari-20.svg)

