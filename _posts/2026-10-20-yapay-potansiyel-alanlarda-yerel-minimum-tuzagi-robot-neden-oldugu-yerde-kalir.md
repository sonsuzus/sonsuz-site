---
layout: post
title: "Yapay Potansiyel Alanlarda Yerel Minimum Tuzağı: Robot Neden Olduğu Yerde Kalır?"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - yapay potansiyel alan
  - engelden kaçınma
  - yerel minimum
  - otonom robotlar
  - yol planlama
toc: true
image: /img/yapay-potansiyel-alanlarda-84.png
---

Yapay potansiyel alan yöntemi, mobil robotların hedefe ilerlerken engellerden kaçınmasını sağlayan zarif ve hesaplama açısından hafif bir yaklaşımdır. Hedef robotu çeken bir mıknatıs, engeller ise onu iten görünmez kuvvet kaynakları gibi modellenir. Ne var ki bu sade fikir, robotun hedefe ulaşmadan durduğu meşhur **yerel minimum** problemiyle karşılaşabilir.
``
## Potansiyel alanın temel mantığı

Robotun konumu $q$, hedef konumu ise $q_g$ olsun. Sistemdeki toplam potansiyel enerji, çekici ve itici bileşenlerin toplamıdır:

$$U(q)=U_{att}(q)+U_{rep}(q)$$

Hedefin oluşturduğu çekici potansiyel çoğunlukla şöyle tanımlanır:

$$U_{att}(q)=\frac{1}{2}k_{att}\lVert q-q_g\rVert^2$$

Burada $k_{att}$ çekim katsayısıdır. Engellere ait itici potansiyel ise robot engele belirli bir mesafeden daha yakın olduğunda etkinleşir:

$$U_{rep}(q)=\frac{1}{2}k_{rep}\left(\frac{1}{\rho(q)}-\frac{1}{\rho_0}\right)^2$$

$\rho(q)$ en yakın engele olan mesafeyi, $\rho_0$ ise engelin etki mesafesini temsil eder. Robotun hareket yönü, toplam potansiyelin negatif gradyanından elde edilir:

$$F(q)=-\nabla U(q)=F_{att}(q)+F_{rep}(q)$$

Başka bir deyişle robot, enerji yüzeyinde aşağı doğru yuvarlanan bir bilye gibidir. Sorun, yüzeydeki her çukurun gerçek hedef olmamasıdır.

## Yerel minimum nasıl oluşur?

Yerel minimumda çekici ve itici kuvvetler birbirini dengeler:

$$F_{att}(q)+F_{rep}(q)=0$$

Robot hedefte olmadığı hâlde bileşke kuvvet sıfır olduğu için hareket komutu üretemez. Özellikle U biçimli engeller, birbirine yakın engeller ve hedefin bir engelin hemen arkasında bulunması bu riski artırır. Dar geçitlerde görülen sağa-sola salınım ise tam anlamıyla yerel minimum değildir; fakat yöntemin yalnızca anlık geometrik bilgiye dayanmasından kaynaklanan benzer bir başarısızlıktır.

| Durum | Robotun davranışı | Temel neden |
|---|---|---|
| Serbest alan | Doğrudan hedefe ilerler | Çekici kuvvet baskındır |
| Tek engel | Engelin çevresinden sapar | İtici kuvvet geçici olarak yön değiştirir |
| U biçimli engel | Girintinin içinde kalabilir | Çıkış yönü önce hedeften uzaklaşmayı gerektirir |
| Simetrik dar koridor | Salınım yapabilir | Karşılıklı itici kuvvetler hızla yön değiştirir |
| Engel arkasındaki hedef | Hedefe yakınken durabilir | Çekim ve itme dengelenir |

## Basit bir kuvvet hesabı

Aşağıdaki Python fonksiyonu, iki boyutlu ortamda hedef çekimini ve engel itmesini hesaplar. Kod, yöntemin yerel ve tepkisel yapısını görünür kılar:

```python
import numpy as np

def potential_force(position, goal, obstacles,
                    k_att=1.0, k_rep=0.8, influence=2.0):
    position = np.asarray(position, dtype=float)
    goal = np.asarray(goal, dtype=float)

    force = k_att * (goal - position)

    for obstacle in obstacles:
        delta = position - np.asarray(obstacle, dtype=float)
        distance = np.linalg.norm(delta)

        if 1e-6 < distance < influence:
            direction = delta / distance
            magnitude = k_rep * (1 / distance - 1 / influence) / distance**2
            force += magnitude * direction

    return force
```

Robot her çevrimde bu kuvvetin yönünde küçük bir adım atabilir. Ancak fonksiyon geçmiş hareketleri veya engelin genel şeklini bilmez. Hesaplanan kuvvet sıfıra yaklaşırsa robot, önünde geçerli bir çıkış olsa bile onu keşfedemeyebilir.

## Tuzaktan kurtulma yöntemleri

Yerel minimum riskini azaltmak için birkaç yaklaşım kullanılabilir:

- **Rastgele kaçış kuvveti:** Robot uzun süre ilerleyemezse geçici bir rastgele yön eklenir.
- **Teğetsel kuvvet:** Engeli yalnızca itmek yerine çevresinden dolaşmayı teşvik eden bir bileşen uygulanır.
- **Ara hedefler:** Global planlayıcının ürettiği yol üzerindeki noktalar sırayla hedef seçilir.
- **Harmonik potansiyeller:** Laplace tabanlı alanlarla hedef dışındaki minimumların oluşması sınırlandırılır.
- **Hibrit planlama:** A*, Dijkstra veya RRT global rota için; potansiyel alan ise anlık kaçınma için kullanılır.

Pratikte en güvenilir çözüm hibrit yaklaşımdır. Yapay potansiyel alan hızlı refleksler sağlarken global planlayıcı, robotun bazen hedefe yaklaşmak için önce hedeften uzaklaşması gerektiğini anlayabilir. Böylece robot görünmez bir çukurda düşüncelere dalmak yerine yoluna devam eder.

![yapay-potansiyel-alanlarda-84](/img/yapay-potansiyel-alanlarda-84.svg)

