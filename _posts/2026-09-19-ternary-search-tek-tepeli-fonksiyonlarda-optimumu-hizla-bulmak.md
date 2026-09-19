---
layout: post
title: "Ternary Search: Tek Tepeli Fonksiyonlarda Optimumu Hızla Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - ternary search
  - algoritma
  - optimizasyon
  - python
  - arama algoritmaları
toc: true
---

Bir dağın zirvesini bulmak istediğinizi düşünün; ancak sis yüzünden yalnızca bulunduğunuz noktaların yüksekliğini ölçebiliyorsunuz. Her yeri adım adım dolaşmak yerine dağı düzenli biçimde daraltabilirsiniz. Ternary Search, yani üçlü arama, tam olarak bu fikri kullanarak tek tepeli fonksiyonların minimum veya maksimum noktasını bulur.

``

## Tek tepeli fonksiyon nedir?

Bir fonksiyon belirli bir noktaya kadar sürekli artıyor, ardından sürekli azalıyorsa **tek tepeli** veya *unimodal* kabul edilir. Maksimum aradığımız durumda bir $x^*$ noktası için davranış şöyledir:

- $x < x^*$ bölgesinde fonksiyon artar.
- $x > x^*$ bölgesinde fonksiyon azalır.
- Zirve yaklaşık olarak $x^*$ noktasındadır.

Minimum ararken bunun tersi geçerlidir: Fonksiyon önce azalır, sonra artar. Örneğin $f(x)=-(x-4)^2+10$ fonksiyonunun tek maksimumu $x=4$ noktasındadır. Buna karşılık sinüs gibi çok sayıda tepe içeren fonksiyonlarda Ternary Search, tüm aralık için güvenilir değildir.

| Özellik | Binary Search | Ternary Search |
|---|---|---|
| Temel amaç | Sıralı yapıda değer bulmak | Tek tepeli fonksiyonda optimum bulmak |
| Karşılaştırılan nokta | Bir orta nokta | İki iç nokta |
| Gerekli yapı | Monotonluk veya sıralılık | Unimodallik |
| Her adımda kalan aralık | Yaklaşık $1/2$ | Yaklaşık $2/3$ |

## Aralık nasıl daraltılır?

Başlangıç aralığımız $[l,r]$ olsun. Aralığın içinde iki nokta seçeriz:

$$m_1=l+(r-l)/3$$

$$m_2=r-(r-l)/3$$

Maksimum arıyorsak $f(m_1)$ ile $f(m_2)$ karşılaştırılır. Eğer $f(m_1)<f(m_2)$ ise fonksiyon sağ tarafa doğru yükseliyor demektir; optimum $m_1$ noktasının solunda olamaz ve $l=m_1$ yapılır. Aksi durumda sağ bölüm elenir ve $r=m_2$ olur.

Her turda aralık küçülür. $k$ iterasyon sonunda yaklaşık uzunluk:

$$L_k=L_0(2/3)^k$$

olur. Sürekli değerlerde çoğunlukla belirli bir iterasyon sayısı veya hata toleransı kullanılır. Zaman karmaşıklığı hedeflenen hassasiyete bağlı olarak $O(\log(L/\varepsilon))$ biçiminde ifade edilir.

## Python ile sürekli aralıkta maksimum

Aşağıdaki kod, verilen fonksiyonun $[left,right]$ aralığındaki yaklaşık maksimum konumunu hesaplar:

```python
def ternary_search_max(func, left, right, iterations=100):
    for _ in range(iterations):
        m1 = left + (right - left) / 3
        m2 = right - (right - left) / 3

        if func(m1) < func(m2):
            left = m1
        else:
            right = m2

    x = (left + right) / 2
    return x, func(x)


def score(x):
    return -(x - 4) ** 2 + 10

position, value = ternary_search_max(score, -20, 20)
print(position, value)
```

Kodda 100 iterasyon, çoğu kayan noktalı sayı uygulaması için fazlasıyla yeterli hassasiyet sağlar. Son aralığın orta noktası optimumun yaklaşık konumu olarak döndürülür. Minimum bulmak için karşılaştırma yönünü ters çevirmek yeterlidir.

## Ayrık dizilerde kullanım

Ternary Search, önce artıp sonra azalan dizilerde de uygulanabilir. Ancak indisler tam sayı olduğu için aralık yeterince küçüldüğünde kalan birkaç elemanı doğrudan kontrol etmek daha güvenlidir. Yuvarlama nedeniyle aynı noktaların tekrar seçilmesi aksi hâlde sonsuz döngüye yol açabilir.

| Durum | Önerilen bitiş koşulu |
|---|---|
| Gerçek sayılı aralık | $r-l<\varepsilon$ veya sabit iterasyon |
| Tam sayılı aralık | Küçük aralıkta doğrusal kontrol |
| Pahalı fonksiyon hesabı | Sonuçları önbelleğe alma |

Ternary Search güçlüdür ama sihirli değildir: Başarı için aralığın gerçekten tek tepeli olması gerekir. Bu varsayım sağlandığında kaba kuvvetle binlerce noktayı denemek yerine, optimuma hızlı ve kontrollü biçimde yaklaşır; sisli dağın zirvesi de artık o kadar gizemli görünmez.
