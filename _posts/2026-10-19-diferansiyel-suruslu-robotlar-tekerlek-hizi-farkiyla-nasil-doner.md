---
layout: post
title: "Diferansiyel Sürüşlü Robotlar Tekerlek Hızı Farkıyla Nasıl Döner?"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - diferansiyel sürüş
  - kinematik
  - tekerlek hızı
  - python
  - mobil robotlar
toc: true
image: /img/diferansiyel-suruslu-robotlar-65.png
---

Diferansiyel sürüşlü bir robotun direksiyonu yoktur; buna rağmen kıvrak biçimde dönebilir, hatta olduğu yerde kendi ekseni etrafında dans edebilir. Bu yeteneğin sırrı, sağ ve sol tekerleklerin farklı hızlarda döndürülmesidir. Alışveriş arabasını tek taraftan daha güçlü ittiğinizi düşünün: hız farkı, aracın yönünü değiştirir.

![diferansiyel-suruslu-robotlar-65](/img/diferansiyel-suruslu-robotlar-65.svg)

``
## Temel mekanik düzen

Bu robotlarda aynı eksen üzerinde bulunan iki bağımsız tahrik tekerleği vardır. Tekerlekler arasındaki mesafeye **iz genişliği** veya dingil uzunluğu denir ve genellikle $L$ ile gösterilir. Sol tekerleğin doğrusal hızı $v_l$, sağ tekerleğinki ise $v_r$ olsun.

Robotun merkezinin ileri yönlü doğrusal hızı iki tekerlek hızının ortalamasıdır:

$$v = (v_r + v_l) / 2$$

Açısal hız ise tekerlekler arasındaki hız farkıyla belirlenir:

$$ω = (v_r - v_l) / L$$

Bu ikinci denklem robotun dönüş mantığını özetler. Hız farkı büyüdükçe robot daha hızlı döner. Tekerlekler arası mesafe büyüdükçe aynı hız farkıyla elde edilen açısal hız azalır; çünkü geniş bir robotu çevirmek daha zordur.

| Sol ve sağ hız ilişkisi | Robotun davranışı | Açısal hız |
|---|---|---:|
| $v_l = v_r > 0$ | Düz ileri gider | $0$ |
| $v_l < v_r$ | Sola döner | Pozitif |
| $v_l > v_r$ | Sağa döner | Negatif |
| $v_l = -v_r$ | Olduğu yerde döner | En yüksek |
| $v_l = v_r = 0$ | Durur | $0$ |

Buradaki sağ ve sol yön işaretleri, kullanılan koordinat sistemine göre ters tanımlanabilir. Önemli olan yazılımın ve matematiksel modelin aynı işaret kuralını kullanmasıdır.

## Görünmez dönüş merkezi: ICC

Robot viraj alırken iki tekerlek aynı merkez çevresinde fakat farklı yarıçaplarda yay çizer. Bu ortak noktaya **Anlık Dönüş Merkezi** ya da ICC denir. İç taraftaki tekerlek daha kısa, dış taraftaki tekerlek daha uzun yol aldığı için dış tekerlek daha hızlı dönmelidir.

Robot merkezinin dönüş yarıçapı $R$, açısal hız sıfır değilken şöyle bulunabilir:

$$R = v / ω = L(v_r + v_l) / (2(v_r - v_l))$$

Tekerlek hızları birbirine yaklaştığında paydadaki fark küçülür ve $R$ büyür; robot geniş bir yay çizer. Hızlar eşit olduğunda yarıçap teorik olarak sonsuza gider, yani hareket düz bir çizgiye dönüşür. Hızlar eşit büyüklükte ve zıt yönlü olduğundaysa $v=0$ olur; dönüş merkezi robotun tam ortasına gelir.

## Basit bir hız hesabı

Aşağıdaki Python fonksiyonu, tekerlek hızlarından robotun doğrusal ve açısal hızını hesaplar:

```python
def robot_hizi(sol_hiz, sag_hiz, tekerlek_araligi):
    dogrusal_hiz = (sag_hiz + sol_hiz) / 2
    acisal_hiz = (sag_hiz - sol_hiz) / tekerlek_araligi
    return dogrusal_hiz, acisal_hiz

v, omega = robot_hizi(0.20, 0.40, 0.30)
print(v, omega)
```

Bu örnekte robotun doğrusal hızı $0.30\ m/s$, açısal hızı yaklaşık $0.67\ rad/s$ olur. Sağ tekerlek daha hızlı olduğu için robot sola yönelir.

Motorlar genellikle doğrusal hız yerine açısal tekerlek hızıyla kontrol edilir. Tekerlek yarıçapı $r$ ve motor açısal hızı $ω_w$ ise doğrusal hız:

$$v_w = rω_w$$

bağıntısıyla bulunur. Böylece enkoderden ölçülen dönüş hızı, robot kinematiğinde kullanılabilir.

## Gerçek dünya neden formüllerden daha huysuzdur?

Teorik model tekerleklerin kaymadığını varsayar. Gerçekte zemin sürtünmesi, motor farklılıkları, pil gerilimi ve ağırlık dağılımı dönüşü etkiler. Aynı PWM değeri iki motorda aynı hızı üretmeyebilir. Bu nedenle enkoder geri bildirimi ve PID kontrolü kullanılarak her tekerleğin hedef hızı ayrı ayrı korunur.

Kısacası diferansiyel sürüş, mekanik olarak sade fakat matematiksel olarak güçlüdür: ortalama hız robotu ilerletir, hız farkı ise döndürür. İki motorun uyumlu anlaşmazlığı, robotun tüm yön kabiliyetini oluşturur.
