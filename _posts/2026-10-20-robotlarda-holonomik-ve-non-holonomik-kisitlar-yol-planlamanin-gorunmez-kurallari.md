---
layout: post
title: "Robotlarda Holonomik ve Non-Holonomik Kısıtlar: Yol Planlamanın Görünmez Kuralları"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - yol planlama
  - holonomik
  - non-holonomik
  - kinematik
  - otonom robotlar
toc: true
image: /img/robotlarda-holonomik-ve-78.png
---

Bir robotun harita üzerinde boş bir nokta bulması, o noktaya gerçekten ulaşabileceği anlamına gelmez. Satranç taşları gibi robotların da hareket kuralları vardır: Holonomik robotlar yana kayabilirken non-holonomik robotlar çoğunlukla önce yönelmek, sonra ilerlemek zorundadır. Yol planlayıcı bu fiziksel gerçeği hesaba katmazsa kusursuz görünen rota, gerçek dünyada duvara sürtünen pahalı bir hayale dönüşebilir.

``

## Hareket kısıtı ne demektir?

Bir robotun konfigürasyonu genellikle

$$q = (x, y, \theta)$$

ile gösterilir. Burada $x$ ve $y$ konumu, $\theta$ ise yönelimi temsil eder. Robot üç boyutlu bir konfigürasyon uzayında bulunsa da her yönde anlık hız üretemeyebilir.

Bir kısıt yalnızca konfigürasyon değişkenleriyle

$$f(q)=0$$

şeklinde yazılabiliyorsa **holonomik** kabul edilir. Kısıt hızlara bağlıysa ve konum düzeyinde bütünleştirilemiyorsa non-holonomik davranış ortaya çıkar. Bu tür kısıtların yaygın gösterimi şöyledir:

$$A(q)\dot{q}=0$$

Örneğin diferansiyel sürüşlü bir robotun yana kaymama koşulu:

$$-\sin(\theta)\dot{x}+\cos(\theta)\dot{y}=0$$

biçimindedir. Denklem basitçe şunu söyler: Robotun tekerlek ekseni doğrultusunda yanal hızı yoktur. Yani robot araba park eder gibi birkaç manevra yapmak zorunda kalabilir.

## İki hareket dünyasının karşılaştırması

| Özellik | Holonomik robot | Non-holonomik robot |
|---|---|---|
| Anlık hareket | Serbestlik derecelerinde bağımsız | Belirli hız yönleriyle sınırlı |
| Tipik örnek | Omni veya mecanum tekerlekli platform | Otomobil, bisiklet, diferansiyel robot |
| Yana hareket | Genellikle mümkün | Doğrudan mümkün değil |
| Planlama uzayı | Çoğu zaman $(x,y)$ yeterli olabilir | $(x,y,\theta)$ gerekir |
| Rota biçimi | Keskin dönüşler mümkün | Eğrilik ve dönüş yarıçapı önemlidir |
| Planlama maliyeti | Görece düşük | Daha yüksek |

![robotlarda-holonomik-ve-78](/img/robotlarda-holonomik-ve-78.svg)


Holonomik bir platform için A* algoritması iki boyutlu ızgarada kısa bir yol bulabilir. Robot, gerektiğinde yönünü değiştirmeden yana kayabilir. Non-holonomik bir araçta ise aynı yol üzerindeki doksan derecelik köşe fiziksel olarak uygulanamayabilir.

## Yol planlamasına etkisi

Non-holonomik planlamada yalnızca engellerden kaçmak yetmez. Planlayıcı; yönelim, minimum dönüş yarıçapı, geri hareket izni ve direksiyon sınırı gibi değişkenleri de değerlendirmelidir. Bu nedenle klasik A* yerine **Hybrid A***, **state lattice**, **RRT**, **RRT\*** veya Dubins ve Reeds–Shepp eğrileri kullanılabilir.

Dubins aracı yalnızca ileri hareket eder ve eğriliği sınırlıdır. Reeds–Shepp modeli ise geri vitese de izin verir. Böylece iki durum arasındaki mesafe, Öklid uzaklığından daha gerçekçi hesaplanır:

$$d_{gerçek}(q_1,q_2) \geq d_{Öklid}(q_1,q_2)$$

Çünkü kuş uçuşu en kısa çizgi, otomobil sürüşü açısından her zaman uygulanabilir değildir.

## Basit bir kısıt kontrolü

Aşağıdaki Python fonksiyonu, diferansiyel robotun verilen dünya hızlarında yanal kayma üretip üretmediğini denetler:

```python
import math

def hareket_gecerli_mi(theta, vx, vy, tolerans=1e-3):
    # Robot gövdesine göre yanal hız bileşenini hesaplar.
    yanal_hiz = -math.sin(theta) * vx + math.cos(theta) * vy
    return abs(yanal_hiz) < tolerans

print(hareket_gecerli_mi(0.0, 1.0, 0.0))  # True: ileri hareket
print(hareket_gecerli_mi(0.0, 0.0, 1.0))  # False: doğrudan yana kayma
```

Gerçek bir planlayıcı, komşu durum üretirken yalnızca bu koşulu test etmekle kalmaz; robotun hareket modelini kısa bir süre boyunca simüle eder. Örneğin

$$\dot{x}=v\cos\theta,\qquad \dot{y}=v\sin\theta,\qquad \dot{\theta}=\omega$$

modeliyle farklı $v$ ve $\omega$ komutları denenerek erişilebilir yeni düğümler oluşturulur. Böylece arama ağacındaki her bağlantı gerçekten uygulanabilir olur.

## Sonuç

Holonomik planlama geometrik olarak “Nereden geçebilirim?” sorusuna odaklanırken non-holonomik planlama buna “Oraya hangi yönelim ve manevrayla ulaşabilirim?” sorusunu ekler. Daha gerçekçi kısıtlar daha fazla hesaplama gerektirir; ancak uygulanamayan kısa bir yol yerine güvenli, pürüzsüz ve sürülebilir bir rota üretir. Robotik dünyasında en kısa yol bazen düz çizgi değil, doğru kıvrımdır.
