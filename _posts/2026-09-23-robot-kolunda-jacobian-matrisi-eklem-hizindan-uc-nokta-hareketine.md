---
layout: post
title: "Robot Kolunda Jacobian Matrisi: Eklem Hızından Uç Nokta Hareketine"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - jacobian
  - kinematik
  - robot-kolu
  - python
  - lineer-cebir
toc: true
---

Bir robot kolunun eklemlerini döndürdüğümüzde uç efektörün hangi yönde ve ne kadar hızlı hareket edeceğini nasıl buluruz? Tersinden sorarsak, robotun elini belirli bir hızla ilerletmek için motorları hangi hızlarda çevirmeliyiz? Robotikte bu iki dünya arasındaki tercüman **Jacobian matrisi**dir. İlk bakışta ürkütücü görünen bu matris, aslında eklem hızlarını Kartezyen uzaydaki harekete bağlayan yerel bir yol haritasıdır.
``
## İki farklı hız uzayı

$n$ eklemli bir robotun eklem konumlarını şu vektörle gösterelim:

$$q = [q_1, q_2, \ldots, q_n]^T$$

Robotun uç efektör konumu ise ileri kinematik fonksiyonuyla hesaplanır:

$$x = f(q)$$

Buradaki $x$, yalnızca $(x,y,z)$ konumunu veya konumla birlikte yönelimi içerebilir. Bu eşitliğin zamana göre türevini aldığımızda Jacobian sahneye çıkar:

$$\dot{x} = J(q)\dot{q}$$

$\dot{q}$ eklem hızlarını, $\dot{x}$ uç efektörün doğrusal ve açısal hızını temsil eder. $J(q)$ ise robotun mevcut duruşuna bağlıdır; kol hareket ettikçe Jacobian da değişir.

| Kavram | Eklem uzayı | Kartezyen uzay |
|---|---|---|
| Konum | $q$ | $x=f(q)$ |
| Hız | $\dot{q}$ | $\dot{x}$ |
| Birim | rad/s veya m/s | m/s ve rad/s |
| Bağlantı | Motor komutları | $\dot{x}=J\dot{q}$ |

## İki eklemli düzlemsel kol

Uzunlukları $L_1$ ve $L_2$ olan, iki döner eklemli bir kol düşünelim. Uç noktanın konumu şöyledir:

$$x=L_1\cos q_1+L_2\cos(q_1+q_2)$$

$$y=L_1\sin q_1+L_2\sin(q_1+q_2)$$

Jacobian, konum bileşenlerinin eklem değişkenlerine göre kısmi türevlerinden oluşur:

$$J(q)=\begin{bmatrix}
\frac{\partial x}{\partial q_1} & \frac{\partial x}{\partial q_2} \\
\frac{\partial y}{\partial q_1} & \frac{\partial y}{\partial q_2}
\end{bmatrix}$$

Türevleri yerleştirdiğimizde:

$$J(q)=\begin{bmatrix}
-L_1\sin q_1-L_2\sin(q_1+q_2) & -L_2\sin(q_1+q_2) \\
L_1\cos q_1+L_2\cos(q_1+q_2) & L_2\cos(q_1+q_2)
\end{bmatrix}$$

Bu matrisle verilen eklem hızlarının uç noktada oluşturacağı hızı doğrudan hesaplayabiliriz.

```python
import numpy as np

def jacobian(q1, q2, L1=1.0, L2=0.8):
    s1 = np.sin(q1)
    c1 = np.cos(q1)
    s12 = np.sin(q1 + q2)
    c12 = np.cos(q1 + q2)

    return np.array([
        [-L1*s1 - L2*s12, -L2*s12],
        [ L1*c1 + L2*c12,  L2*c12]
    ])

q = np.radians([30, 45])
q_dot = np.array([0.4, -0.2])
velocity = jacobian(*q) @ q_dot
print(velocity)
```

Kod önce mevcut eklem açıları için Jacobian’ı kurar, ardından `J @ q_dot` işlemiyle uç noktanın $x$ ve $y$ yönlerindeki hızını üretir. Yani motorların hareketi, robot elinin hareketine çevrilir.

## Ters hız kinematiği

Hedef uç efektör hızı biliniyorsa eklem hızlarını bulmak isteriz:

$$\dot{q}=J^{-1}\dot{x}$$

Ancak Jacobian her zaman kare veya terslenebilir değildir. Bu durumda Moore–Penrose sözde tersi kullanılır:

$$\dot{q}=J^{+}\dot{x}$$

```python
target_velocity = np.array([0.1, 0.05])
q_dot_command = np.linalg.pinv(jacobian(*q)) @ target_velocity
```

| Yöntem | Kullanım | Sınırlama |
|---|---|---|
| $J^{-1}$ | Kare ve tekil olmayan Jacobian | Her robotta kullanılamaz |
| $J^+$ | Fazla veya eksik serbestlik | Tekillik yakınında büyük hız üretebilir |
| Sönümlü sözde ters | Tekilliğe yakın durumlar | Küçük takip hatası oluşturabilir |

## Tekillik: Robotun mekanik çıkmazı

Kol tamamen açıldığında bazı yönlerde hareket üretmek zorlaşabilir. Jacobian bu durumda rank kaybeder; determinantı kare sistemlerde sıfıra yaklaşır. İstenen küçük bir uç efektör hızı, gerçekçi olmayan eklem hızları gerektirebilir. Bu nedenle denetleyiciler tekillik ölçümü, hız sınırlandırma ve sönümlü en küçük kareler gibi yöntemlerden yararlanır.

Özetle Jacobian, robotun o anki duruşunda “eklemleri biraz oynatırsam elim nasıl hareket eder?” sorusunu cevaplar. Hız kontrolünden kuvvet analizine, yörünge takibinden görsel servoya kadar modern robot kolu uygulamalarının merkezinde bu güçlü bağlantı bulunur.
