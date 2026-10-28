---
layout: post
title: "Her Tohumda Yeni Bir Macera: Oyunlarda Prosedürel Üretim"
math: true
categories: 
  - Bilgi
tags: 
  - prosedürel üretim
  - oyun geliştirme
  - algoritma
  - python
  - zindan üretimi
  - rastgelelik
toc: true
image: /img/her-tohumda-yeni-50.png
---

![her-tohumda-yeni-50](/img/her-tohumda-yeni-50.svg)


Bir oyuna her başladığınızda dağların yer değiştirdiğini, koridorların başka yönlere uzandığını ve hazinelerin hiç beklemediğiniz köşelerde belirdiğini düşünün. Prosedürel üretim, içerikleri geliştiricinin tek tek tasarlaması yerine belirli kurallar ve algoritmalar yardımıyla oluşturan tekniktir. Böylece küçük bir kod parçası, keşfedilecek binlerce farklı dünya üretebilir.

``

## Rastgelelik Aslında Ne Kadar Rastgele?

Bilgisayarlar çoğunlukla gerçek anlamda rastgele davranmaz. Bunun yerine **sözde rastgele sayı üreteci** (PRNG) kullanırlar. Üretece verilen başlangıç değerine **seed**, yani tohum denir. Aynı algoritma ve aynı tohum kullanıldığında aynı sayı dizisi, dolayısıyla aynı dünya ortaya çıkar.

Bunu basitçe şöyle ifade edebiliriz:

$$x_{n+1} = (a x_n + c) \bmod m$$

Bu doğrusal eşlik üreteci formülünde $x_n$ mevcut sayı, $a$ çarpan, $c$ artış ve $m$ mod değeridir. İlk $x_0$ değeri ise tohumdur. Bir oyuncu arkadaşına yalnızca `4271` tohumunu göndererek aynı zindanı ziyaret etmesini sağlayabilir. Kısacası seed, koskoca dünyanın sıkıştırılmış adresi gibidir.

## Zindanlar Nasıl Kurulur?

En temel yaklaşım, haritayı duvarlarla doldurup rastgele odalar açmak ve bu odaları koridorlarla bağlamaktır. Ancak tamamen rastgele seçim yapmak; ulaşılamayan odalar, anlamsız geçitler veya kapının arkasında duvar gibi komik sonuçlar doğurabilir. Bu nedenle üretim, doğrulama kurallarıyla birlikte çalışmalıdır.

| Yöntem | Güçlü yanı | Zayıf yanı | Uygun kullanım |
|---|---|---|---|
| Rastgele odalar | Basit ve hızlıdır | Çakışma oluşturabilir | Klasik zindanlar |
| BSP | Düzenli oda dağılımı sağlar | Fazla geometrik görünebilir | Bina ve tesisler |
| Hücresel otomat | Doğal mağaralar üretir | Bağlantı kontrolü gerekir | Mağara sistemleri |
| Gürültü fonksiyonları | Akıcı arazi geçişleri sağlar | İnce ayar ister | Açık dünyalar |
| Wave Function Collapse | Yerel kurallara uyar | Çelişkiler pahalı olabilir | Şehir ve desenler |

**BSP** yönteminde harita dikdörtgen bölgelere tekrar tekrar ayrılır. Her yaprak bölgeye bir oda yerleştirilir ve kardeş bölgeler koridorlarla bağlanır. Hücresel otomatta ise her karo, komşularının durumuna göre duvar veya zemin olur. Örneğin bir karonun çevresinde beşten fazla duvar varsa sonraki adımda onun da duvara dönüşmesi mağara benzeri kümeler üretir.

## Küçük Bir Oda Üreticisi

Aşağıdaki Python örneği, sabit bir tohumla çakışmayan dikdörtgen odalar yerleştirir:

```python
import random

WIDTH, HEIGHT = 40, 20
random.seed(4271)
rooms = []

def overlaps(candidate):
    x, y, w, h = candidate
    for rx, ry, rw, rh in rooms:
        separated = (x + w < rx or rx + rw < x or
                     y + h < ry or ry + rh < y)
        if not separated:
            return True
    return False

for _ in range(30):
    w, h = random.randint(4, 9), random.randint(3, 6)
    x = random.randint(1, WIDTH - w - 1)
    y = random.randint(1, HEIGHT - h - 1)
    candidate = (x, y, w, h)
    if not overlaps(candidate):
        rooms.append(candidate)

print(f"Üretilen oda sayısı: {len(rooms)}")
```

Kod, otuz yerleştirme denemesi yapar. `overlaps` fonksiyonu yeni odanın mevcut odalarla kesişip kesişmediğini denetler. Bu yalnızca ilk adımdır; odaların merkezlerini hesaplayıp en yakın komşuları koridorlarla birleştirmek, zindanı gerçekten oynanabilir hâle getirir.

## Eğlenceyi Algoritmaya Bırakmamak

Prosedürel üretimin hedefi yalnızca çeşitlilik değildir. Bir seviyenin kalitesi kabaca şu dengeyle düşünülebilir:

$$Q = \alpha V + \beta O - \gamma F$$

Burada $V$ çeşitlilik, $O$ oynanabilirlik ve $F$ adaletsizliktir. Katsayılar oyunun önceliklerini temsil eder. Her harita farklı olsa bile oyuncu çıkışa ulaşamıyorsa algoritma görevini başaramamıştır.

Bu nedenle üretilen içerik; bağlantılılık, zorluk, kaynak dağılımı ve başlangıç güvenliği bakımından test edilmelidir. Başarılı sistemler insan tasarımını ortadan kaldırmaz; tasarımcının kurallarını çoğaltır. Algoritma zarları atar, fakat zarların hangi masada ve hangi kurallarla atılacağına hâlâ geliştirici karar verir.
