---
layout: post
title: "Swarm Intelligence: Parçacık Sürü Optimizasyonunun Yapay Zekâdaki Yeri"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zekâ
  - pso
  - sürü zekâsı
  - optimizasyon
  - sezgisel algoritmalar
  - makine öğrenmesi
toc: true
image: /img/swarm-intelligence-parcacik-75.png
---

Doğada merkezi bir yönetici olmadan sergilenen kolektif davranışlar, şaşırtıcı derecede başarılı sonuçlar üretir. Kuşlar yiyecek ararken birbirlerinin hareketlerinden yararlanır, balıklar tehlikeden birlikte kaçar ve karıncalar en kısa yolu kimse onlara harita vermeden bulur. **Parçacık Sürü Optimizasyonu** (Particle Swarm Optimization veya PSO), bu sosyal davranışı matematiksel bir optimizasyon yöntemine dönüştürür.

``

## Sürü zekâsı nedir?

Sürü zekâsı, basit kuralları izleyen çok sayıda bireyin etkileşiminden ortaya çıkan kolektif problem çözme yeteneğidir. Buradaki temel fikir, tek bir bireyin kusursuz olmasına gerek olmadığıdır. Bireyler kendi deneyimlerini grubun deneyimiyle birleştirdiğinde etkili bir arama mekanizması oluşur.

PSO, 1995 yılında James Kennedy ve Russell Eberhart tarafından geliştirilmiştir. Algoritmada her olası çözüm bir **parçacık**, tüm parçacıklar ise bir **sürü** olarak temsil edilir. Parçacıklar çözüm uzayında dolaşarak amaç fonksiyonunun en iyi değerini arar.

| Doğadaki kavram | PSO karşılığı | Görevi |
|---|---|---|
| Kuş | Parçacık | Aday çözümü temsil eder |
| Kuşun konumu | Çözüm vektörü | Parametrelerin mevcut değerlerini taşır |
| Uçuş yönü | Hız vektörü | Sonraki hareketi belirler |
| Bulunan yiyecek | En iyi çözüm | Amaç fonksiyonunun optimumuna karşılık gelir |
| Sürü iletişimi | Küresel en iyi bilgi | Parçacıkları umut vadeden bölgeye yönlendirir |

## PSO nasıl çalışır?

Her parçacığın bir konumu $x_i$ ve hızı $v_i$ bulunur. Ayrıca parçacık, şimdiye kadar keşfettiği en iyi konumu $p_i$ olarak hatırlar. Sürünün bulduğu en iyi konum ise $g$ ile gösterilir.

Hız güncelleme denklemi şöyledir:

$$v_i(t+1)=w v_i(t)+c_1r_1(p_i-x_i(t))+c_2r_2(g-x_i(t))$$

Yeni konum da şu şekilde hesaplanır:

$$x_i(t+1)=x_i(t)+v_i(t+1)$$

Burada $w$ eylemsizlik katsayısıdır ve parçacığın önceki yönünü ne kadar koruyacağını belirler. $c_1$ bilişsel katsayıdır; parçacığın kendi deneyimine bağlılığını temsil eder. $c_2$ sosyal katsayıdır ve sürünün keşfine verilen önemi kontrol eder. $r_1$ ile $r_2$, $[0,1]$ aralığında rastgele sayılardır. Bu rastlantısallık, bütün parçacıkların erkenden aynı noktaya yığılmasını önlemeye yardımcı olur.

| Katsayı tercihi | Baskın davranış | Olası sonuç |
|---|---|---|
| Yüksek $w$ | Geniş alanları keşfetme | Optimumu kaçırma riski azalabilir |
| Yüksek $c_1$ | Bireysel hareket | Parçacıklar bağımsız davranır |
| Yüksek $c_2$ | Sürüye uyum | Hızlı yakınsama sağlanır |
| Dengeli değerler | Keşif ve sömürü dengesi | Genellikle daha kararlı sonuç alınır |

## Python ile basit bir uygulama

Aşağıdaki örnek, $f(x)=x^2$ fonksiyonunun minimumunu arar. Teorik minimum $x=0$ noktasındadır.

```python
import random

parcacik_sayisi = 20
konumlar = [random.uniform(-10, 10) for _ in range(parcacik_sayisi)]
hizlar = [random.uniform(-1, 1) for _ in range(parcacik_sayisi)]
kisisel_en_iyi = konumlar.copy()

def uygunluk(x):
    return x ** 2

kuresel_en_iyi = min(kisisel_en_iyi, key=uygunluk)

for _ in range(100):
    for i in range(parcacik_sayisi):
        r1, r2 = random.random(), random.random()
        hizlar[i] = (
            0.7 * hizlar[i]
            + 1.5 * r1 * (kisisel_en_iyi[i] - konumlar[i])
            + 1.5 * r2 * (kuresel_en_iyi - konumlar[i])
        )
        konumlar[i] += hizlar[i]

        if uygunluk(konumlar[i]) < uygunluk(kisisel_en_iyi[i]):
            kisisel_en_iyi[i] = konumlar[i]

    kuresel_en_iyi = min(kisisel_en_iyi, key=uygunluk)

print("Bulunan minimum noktası:", kuresel_en_iyi)
```

Kod, parçacıkları rastgele başlatır; ardından hız ve konumlarını 100 tur boyunca günceller. Her turda bireysel ve küresel rekorlar yenilenir. Sonuç genellikle sıfıra oldukça yakın çıkar.

## Yapay zekâdaki kullanım alanları

PSO; sinir ağlarının ağırlıklarını ayarlamak, özellik seçmek, hiperparametre optimizasyonu yapmak, robot rotaları planlamak ve enerji sistemlerini düzenlemek için kullanılabilir. Türev bilgisi istememesi, karmaşık ve doğrusal olmayan problemlerde önemli bir avantajdır. Buna karşılık doğru katsayılar seçilmezse yerel optimuma erken yakınsayabilir ve yüksek boyutlarda maliyetli hâle gelebilir.

Kısacası PSO, “en iyi çözümü tek başına bul” yaklaşımı yerine “deneyimini paylaş ve birlikte ara” der. Bazen karmaşık bir problemi çözmek için gereken şey daha güçlü bir birey değil, daha iyi iletişim kuran bir sürüdür.

![swarm-intelligence-parcacik-75](/img/swarm-intelligence-parcacik-75.svg)

