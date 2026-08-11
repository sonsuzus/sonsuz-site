---
layout: post
title: "Kelebek Etkisini Kodlamak: Deterministik Lorenz Çekici Simülasyonu"
math: true
categories: 
  - Proje
tags: 
  - Python
  - Kaos Teorisi
  - Lorenz Çekici
---

Bir kelebeğin kanat çırpışı gerçekten fırtına yaratır mı? Meteorolojik anlamda bu cümle biraz şiirseldir; fakat Lorenz çekicisi, çok daha ilginç bir gerçeği gösterir: Sistem tamamen deterministik kurallarla çalışsa bile başlangıçtaki ufacık farklar zamanla devasa sonuçlara dönüşebilir. Bu projede aynı denklemleri iki neredeyse özdeş başlangıç noktasıyla çözecek, ardından yollarının nasıl ayrıldığını izleyeceğiz.

``

Lorenz sistemi, atmosferdeki konveksiyon hareketini basitleştirmek için Edward Lorenz tarafından geliştirilen üç diferansiyel denklemden oluşur:

$$
\dot{x}=\sigma(y-x),\qquad
\dot{y}=x(\rho-z)-y,\qquad
\dot{z}=xy-\beta z
$$

Buradaki $x$, $y$ ve $z$ fiziksel modelde akış ve sıcaklık bileşenlerini temsil edebilir. Ancak simülasyon açısından önemli olan, her anın bir önceki durum tarafından **tekil biçimde** belirlenmesidir. Rastgele sayı üretmiyoruz; yani sistem deterministiktir. Buna karşılık uzun vadede tahmin edilmesi zordur. Bu ikili, kaos teorisinin kalbidir.

| Kavram | Deterministik sistem | Rastgele sistem |
|---|---|---|
| Sonraki durum | Mevcut durum ve kurallardan hesaplanır | Olasılıksal seçim içerir |
| Aynı başlangıç | Aynı sonucu üretir | Farklı sonuçlar üretebilir |
| Lorenz örneği | Evet | Hayır |
| Uzun vadeli tahmin | Kaotik bölgede zorlaşır | Doğası gereği sınırlıdır |

Klasik kaotik parametreler $\sigma=10$, $\rho=28$ ve $\beta=8/3$ değerleridir. İki yörüngenin başlangıcında yalnızca $10^{-8}$ büyüklüğünde fark oluşturalım. Başta grafikler üst üste görünür; sonra ayrılık hızlanır. Bu büyüme kabaca Lyapunov üssü ile ifade edilir:

$$
\delta(t) \approx \delta_0 e^{\lambda t}
$$

Burada $\delta_0$ başlangıç farkı, $\lambda>0$ ise hassas bağımlılığın işaretidir. Elbette ayrılık sonsuza dek üstel büyümez; çekicinin sınırlı geometrisi nedeniyle yörüngeler aynı karmaşık bölgede dolaşmayı sürdürür.

Aşağıdaki Python kodu `scipy` ile sayısal integrasyon yapar ve iki yörüngeyi üç boyutta çizer. `solve_ivp`, denklemleri küçük zaman adımlarına bölerek yaklaşık çözer; analitik çözüm aramak yerine kontrollü bir sayısal yöntem kullanır.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0

def lorenz(t, durum):
    x, y, z = durum
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return [dx, dy, dz]

zaman = np.linspace(0, 40, 12000)
baslangic_a = [1.0, 1.0, 1.0]
baslangic_b = [1.0 + 1e-8, 1.0, 1.0]

cozum_a = solve_ivp(lorenz, (0, 40), baslangic_a,
                    t_eval=zaman, rtol=1e-9, atol=1e-12)
cozum_b = solve_ivp(lorenz, (0, 40), baslangic_b,
                    t_eval=zaman, rtol=1e-9, atol=1e-12)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")
ax.plot(*cozum_a.y, lw=0.7, label="Başlangıç A")
ax.plot(*cozum_b.y, lw=0.7, alpha=0.75, label="Başlangıç B")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.legend()
plt.show()
```

Daha görünür bir kanıt için yörüngeler arasındaki Öklid uzaklığını da hesaplayabiliriz. Logaritmik ölçek, ilk aşamadaki hızlı ayrışmayı özellikle net gösterir.

```python
fark = np.linalg.norm(cozum_a.y - cozum_b.y, axis=0)
plt.semilogy(zaman, fark)
plt.xlabel("Zaman")
plt.ylabel("Yörüngeler arası uzaklık")
plt.grid(True, which="both")
plt.show()
```

| Deney | Beklenen gözlem |
|---|---|
| `1e-8` fark | Bir süre sonra belirgin ayrışma |
| Aynı başlangıç | Çizgiler tamamen çakışır |
| Daha kısa zaman | Benzer davranış yanılsaması |
| Daha düşük tolerans | Sayısal hata daha erken etkili olabilir |

Önemli nüans şu: Bilgisayardaki kayan nokta aritmetiği de mikroskobik yuvarlama hataları taşır. Bu hata kaosun sebebi değildir; kaotik sistem, var olan küçük hataları büyütür. Dolayısıyla Lorenz çekicisi bize rastgelelik değil, kusursuz kuralların bile uzun vadede neden pratik olarak öngörülemez olabileceğini öğretir.
