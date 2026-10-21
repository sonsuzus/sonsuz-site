---
layout: post
title: "Robotikte İleri ve Ters Kinematik: Neden Biri Kolay, Diğeri Zor?"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - ileri kinematik
  - ters kinematik
  - matematik
  - python
  - kinematik
toc: true
image: /img/robotikte-ileri-ve-49.png
---

![robotikte-ileri-ve-49](/img/robotikte-ileri-ve-49.svg)


Bir robot koluna eklem açılarını verdiğinizde elinin nereye gideceğini bulmak genellikle düzenli bir hesap işidir. Ancak elin ulaşmasını istediğiniz noktayı verip gerekli eklem açılarını sorduğunuzda işler bir anda matematiksel bir bulmacaya dönüşür. İleri kinematik ile ters kinematik arasındaki temel zorluk farkı, aynı hareket zincirine iki farklı yönden bakmalarından kaynaklanır.

``

## Kinematik neyi inceler?

Kinematik; kuvvetleri, motor torklarını ve kütleleri hesaba katmadan robotun konum ve hareket geometrisini inceler. Seri bağlı bir robot kolunda her eklem, kendisinden sonra gelen bağlantıların konumunu etkiler.

Bir robotun eklem değişkenlerini şu vektörle gösterelim:

$$
\mathbf{q} = [q_1, q_2, \ldots, q_n]^T
$$

Robotun uç noktasının konum ve yönelimini ise $\mathbf{x}$ temsil etsin. Bu iki büyüklük arasındaki ilişki genel olarak şöyledir:

$$
\mathbf{x} = f(\mathbf{q})
$$

Buradaki $f$, robotun geometrisini tanımlayan doğrusal olmayan dönüşüm fonksiyonudur.

## İleri kinematik neden daha kolaydır?

İleri kinematikte eklem açıları bilinir ve uç noktanın pozu hesaplanır. Her bağlantı için dönüşüm matrisi oluşturulur, ardından matrisler sırayla çarpılır:

$$
T_0^n = T_0^1 T_1^2 \cdots T_{n-1}^n
$$

Yani tarif nettir: İlk eklemden başla, dönüşümleri uygula ve robot eline kadar ilerle. Seri bir robotta hesap yükü çoğunlukla eklem sayısıyla birlikte düzenli biçimde artar. Uygun matris işlemleri kullanıldığında temel değerlendirme yaklaşık $O(n)$ kabul edilebilir.

İki bağlantılı düzlemsel bir kol için ileri kinematik oldukça doğrudandır:

$$
x = L_1\cos(\theta_1) + L_2\cos(\theta_1 + \theta_2)
$$

$$
y = L_1\sin(\theta_1) + L_2\sin(\theta_1 + \theta_2)
$$

```python
import math

def forward_kinematics(theta1, theta2, length1, length2):
    # Eklem açılarını kullanarak uç noktanın koordinatlarını hesaplar.
    x = length1 * math.cos(theta1)
    x += length2 * math.cos(theta1 + theta2)

    y = length1 * math.sin(theta1)
    y += length2 * math.sin(theta1 + theta2)
    return x, y

print(forward_kinematics(0.5, 0.8, 2.0, 1.5))
```

Aynı giriş değerleri her zaman aynı pozu üretir. Dolayısıyla hesap deterministik ve tek yönlüdür.

## Ters kinematik neden zorlaşır?

Ters kinematikte hedef poz $\mathbf{x}$ bilinir ve şu denklem çözülmeye çalışılır:

$$
\mathbf{q} = f^{-1}(\mathbf{x})
$$

Sorun, $f^{-1}$ fonksiyonunun her zaman sıradan bir ters fonksiyon olmamasıdır. Aynı hedefe dirsek yukarıda veya aşağıda olacak şekilde birden fazla eklem düzeniyle ulaşılabilir. Hedef robotun çalışma alanı dışındaysa hiçbir çözüm bulunmaz. Gereğinden fazla ekleme sahip robotlarda ise sonsuz sayıda çözüm oluşabilir.

| Özellik | İleri kinematik | Ters kinematik |
|---|---|---|
| Bilinen değer | Eklem değişkenleri | Hedef poz |
| Aranan değer | Uç nokta pozu | Eklem değişkenleri |
| Çözüm sayısı | Genellikle tek | Sıfır, bir veya birden fazla |
| Temel işlem | Matrisleri sırayla çarpma | Doğrusal olmayan denklem çözme |
| Başlangıç tahmini | Gerekmez | Sayısal yöntemlerde gerekir |
| Tekillik etkisi | Poz yine hesaplanabilir | Çözüm kararsızlaşabilir |

## Sayısal çözüm ve Jacobian

Karmaşık robotlarda kapalı formda analitik çözüm bulunamayabilir. Bu durumda Jacobian matrisi, eklem hızları ile uç nokta hızını ilişkilendirir:

$$
\dot{\mathbf{x}} = J(\mathbf{q})\dot{\mathbf{q}}
$$

Hedefe iteratif yaklaşmak için sözde ters kullanılabilir:

$$
\Delta\mathbf{q} = J^+(\mathbf{q})(\mathbf{x}_{hedef}-\mathbf{x}_{mevcut})
$$

Algoritma ileri kinematiği tekrar tekrar çalıştırır, hatayı ölçer ve açıları günceller. Bu nedenle maliyet yalnızca eklem sayısına değil; iterasyon sayısına, yakınsama toleransına ve Jacobian hesabına da bağlıdır. Tekillik yakınlarında $J$ rank kaybedebilir; küçük bir konum değişikliği çok büyük eklem hareketleri isteyebilir.

Pratikte ters kinematik çözücüleri eklem limitleri, çarpışma önleme ve enerji tüketimi gibi hedefleri de gözetir. Böylece problem yalnızca denklem çözmekten çıkarak kısıtlı optimizasyona dönüşür. Özetle ileri kinematik robotun mevcut durumunu hesaplayan güvenilir bir yolculukken, ters kinematik aynı hedefe giden uygun yolu seçenekler, engeller ve belirsizlikler arasında arayan çok daha zahmetli bir navigasyondur.
