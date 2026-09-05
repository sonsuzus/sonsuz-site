---
layout: post
title: "Simulated Annealing: Yerel Minimumlardan Kaçan Akıllı Optimizasyon"
math: true
categories: 
  - Bilgi
tags: 
  - optimizasyon
  - algoritmalar
  - python
image: /img/simulated-annealing-yerel-35.png
---

Bazı optimizasyon problemlerinde en iyi çözümü bulmak, dağlık bir arazide gece yürümeye benzer: El feneriniz yalnızca yakın çevreyi gösterir. Sürekli aşağı doğru ilerlerseniz ilk rastladığınız vadiye inersiniz; fakat daha uzakta çok daha derin bir vadi olabilir. **Simulated Annealing** (Benzetimli Tavlama), kontrollü miktarda “yanlış” hamle yaparak bu tuzaktan kaçmayı hedefleyen olasılıksal bir optimizasyon yaklaşımıdır.

![simulated-annealing-yerel-35](/img/simulated-annealing-yerel-35.svg)

``

Algoritmanın ilham kaynağı metalurjidir. Isıtılan bir metalin atomları yüksek enerjide serbestçe hareket eder. Metal yavaşça soğutulduğunda atomlar daha düzenli ve düşük enerjili bir yapıya yerleşir. Çok hızlı soğutma ise kusurlu, kararsız bir yapı bırakabilir. Optimizasyondaki karşılığı nettir: çözüm uzayında başlangıçta cesurca dolaşır, zamanla daha seçici davranırız.

Bir amaç fonksiyonunu $f(x)$ ile gösterelim ve onu **minimize** etmek isteyelim. Mevcut çözüm $x$, komşu aday ise $x'$ olsun. Enerji farkı şu şekilde hesaplanır:

$$\Delta E = f(x') - f(x)$$

Eğer $\Delta E \leq 0$ ise aday çözüm daha iyidir ve doğrudan kabul edilir. İlginç bölüm, daha kötü adaylarda başlar. Algoritma bu adayı aşağıdaki olasılıkla kabul edebilir:

$$P(\text{kabul}) = \exp\left(-\frac{\Delta E}{T}\right)$$

Buradaki $T$, sıcaklıktır. Sıcaklık yüksekken kötü hamlelerin kabul olasılığı da yüksektir; böylece algoritma yerel minimumdan sıçrayabilir. $T$ küçüldükçe bu hoşgörü azalır ve arama en iyi bölgelerde yoğunlaşır.

| Yaklaşım | Kötü hamle kabulü | Yerel minimum riski | Hesaplama davranışı |
|---|---:|---:|---|
| Tepe tırmanma (Hill Climbing) | Hayır | Yüksek | Hızlı ama dar görüşlü |
| Açgözlü arama | Hayır | Yüksek | Her adımda anlık iyiyi seçer |
| Simulated Annealing | Sıcaklığa bağlı | Daha düşük | Keşif ve sömürüyü dengeler |

Soğutma takvimi algoritmanın karakterini belirler. Yaygın bir seçenek geometrik soğutmadır: $T_{k+1} = \alpha T_k$. Burada genellikle $0.8 < \alpha < 0.99$ seçilir. Büyük bir $\alpha$, daha yavaş ama daha kapsamlı arama demektir. Çok küçük değer ise algoritmayı erken “dondurarak” sıradan bir yerel aramaya dönüştürebilir.

Aşağıdaki Python örneği, $f(x)=x^2+10\sin(x)$ fonksiyonunun düşük değerli bir noktasını arar. `komsu` üretimi problemden probleme değişir; rota optimizasyonunda iki şehri takas etmek, çizelgelemede iki görevin yerini değiştirmek buna örnek olabilir.

```python
import math
import random

def f(x):
    return x * x + 10 * math.sin(x)

def simulated_annealing(baslangic, sicaklik=20.0, alfa=0.98, adim_sayisi=1000):
    mevcut = baslangic
    en_iyi = mevcut

    for _ in range(adim_sayisi):
        aday = mevcut + random.uniform(-1.0, 1.0)  # Komşu çözüm üret
        fark = f(aday) - f(mevcut)

        # İyi adayı kesin, kötü adayı olasılıkla kabul et
        if fark <= 0 or random.random() < math.exp(-fark / sicaklik):
            mevcut = aday

        if f(mevcut) < f(en_iyi):
            en_iyi = mevcut

        sicaklik *= alfa
        if sicaklik < 1e-6:
            break

    return en_iyi, f(en_iyi)

x, deger = simulated_annealing(baslangic=8)
print(f"En iyi x: {x:.4f}, fonksiyon değeri: {deger:.4f}")
```

Pratikte üç ayar özellikle önemlidir: başlangıç sıcaklığı, soğutma hızı ve iterasyon sayısı. Başlangıç sıcaklığı, ilk aşamada kötü çözümlerin makul sıklıkta kabul edilmesini sağlamalıdır. Ayrıca algoritma rastgelelik içerdiği için tek bir çalıştırma kesin hüküm değildir; farklı rastgele tohumlarla birkaç deneme yapmak iyi bir alışkanlıktır.

Simulated Annealing, gezgin satıcı problemi, ders programı oluşturma, üretim planlama ve hiperparametre arama gibi devasa ya da karmaşık çözüm uzaylarında güçlüdür. Küresel optimum garantisi pratik ayarlarda yoktur; buna rağmen doğru komşuluk fonksiyonu ve dengeli soğutma ile, “ilk iyi görünen vadiye yerleşmek” yerine daha iyi manzaralar keşfetmenizi sağlar.
