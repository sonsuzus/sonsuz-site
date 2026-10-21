---
layout: post
title: "Humanoid Robotlarda Dengeli Adımlar: Yürüme Döngüsünde Faz Analizi"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - humanoid
  - yürüme-döngüsü
  - faz-analizi
  - kararlılık
  - kontrol-sistemleri
toc: true
image: /img/humanoid-robotlarda-dengeli-62.png
---

İnsansı bir robotun yürümesi, uzaktan bakıldığında sırayla sağ ve sol ayağı öne atmaktan ibaret görünebilir. Oysa robot açısından her adım; temas kuvvetleri, gövde momentumu, eklem açıları ve zamanlamanın birlikte yönetildiği dinamik bir denge problemidir. Faz analizi, robotun bu karmaşık hareketin neresinde bulunduğunu ve küçük bir bozucudan sonra güvenli döngüsüne dönüp dönemeyeceğini anlamamızı sağlar.
``

## Yürüme döngüsü neden periyodiktir?

Bir gait cycle, aynı ayağın iki benzer teması arasındaki hareket dizisidir. Döngü genellikle **tek destek**, **çift destek**, **salınım** ve **temas geçişi** evrelerine ayrılır. Eklem açıları tam olarak tekrarlanmasa bile sistem durumunun benzer bir yörüngeyi izlemesi beklenir.

Robotun durumu şu vektörle gösterilebilir:

$$
\mathbf{x}(t)=[\mathbf{q}(t),\dot{\mathbf{q}}(t)]^T
$$

Burada $\mathbf{q}$ eklem konumlarını, $\dot{\mathbf{q}}$ ise hızları temsil eder. Kararlı yürüyüşte durum uzayındaki hareket, **limit döngü** adı verilen kapalı bir yörünge oluşturur. Robot küçük bir itme aldığında yörüngeden uzaklaşabilir; önemli olan birebir aynı noktaya değil, tekrar bu döngüye yaklaşmasıdır. Buna **yörüngesel kararlılık** denir.

## Zaman değil, faz neden önemlidir?

Sadece saate bakarak “robot adımın yüzde 40’ında” demek yanıltıcı olabilir. Yokuş, zemin esnekliği veya dışarıdan gelen bir itme adım süresini değiştirir. Faz değişkeni ise hareketin fiziksel ilerleyişini takip eder:

$$
\phi \in [0,2\pi), \qquad \dot{\phi}=\omega
$$

Örneğin kalça açısı ve açısal hızı birlikte kullanılarak faz düzleminde bir yörünge çizilebilir. Böylece kontrolcü, kronometreden bağımsız biçimde ayağın salınımın başında mı yoksa yere temas etmek üzere mi olduğunu anlayabilir.

| Yaklaşım | İzlenen bilgi | Bozuculara tepki | Temel risk |
|---|---|---|---|
| Zaman tabanlı kontrol | Geçen süre | Sınırlı uyum | Hareket ile saat ayrışabilir |
| Olay tabanlı kontrol | Topuk teması gibi olaylar | Temaslarda güçlü | İki olay arasında az bilgi verir |
| Faz tabanlı kontrol | Döngüdeki sürekli ilerleme | Yüksek uyum | Güvenilir faz kestirimi gerekir |

![humanoid-robotlarda-dengeli-62](/img/humanoid-robotlarda-dengeli-62.svg)


## Kararlılık nasıl ölçülür?

Yürümenin belirli bir olayında, örneğin sağ topuk temasında, sistem durumu örneklenebilir. Bu kesite **Poincaré kesiti** denir. Ardışık adımlar arasındaki ilişki

$$
\mathbf{x}_{k+1}=P(\mathbf{x}_k)
$$

şeklinde yazılır. Sabit yürüyüş için $\mathbf{x}^*=P(\mathbf{x}^*)$ olmalıdır. Haritanın sabit nokta çevresindeki özdeğerleri, yani Floquet çarpanları, kritik bilgiyi verir. Baskın çarpanın mutlak değeri $\vert \lambda_{max}\vert <1$ ise sapmalar küçülür; $\vert \lambda_{max}\vert >1$ ise robot birkaç adım sonra dramatik bir “yerçekimiyle tanışma” yaşayabilir.

## Basit bir faz portresi

Aşağıdaki Python kodu, idealize edilmiş bir eklem hareketinin açı-hız faz portresini üretir. Kapalı eğri, periyodik davranışın görsel imzasıdır:

```python
import numpy as np
import matplotlib.pyplot as plt

# Bir adımlık örnek kalça açısı
phase = np.linspace(0, 2 * np.pi, 500)
angle = 0.35 * np.sin(phase)
angular_velocity = 0.35 * np.cos(phase)

plt.plot(angle, angular_velocity)
plt.xlabel("Eklem açısı (rad)")
plt.ylabel("Açısal hız (rad/s)")
plt.title("Kalça Eklemi Faz Portresi")
plt.grid(True)
plt.axis("equal")
plt.show()
```

Gerçek robotta eğrinin kalınlaşması sensör gürültüsünü, giderek genişlemesi kararsızlığı, bozucu sonrası yeniden daralması ise toparlanmayı gösterebilir. Bu analiz; ZMP, basınç merkezi ve gövde kütle merkezi ölçümleriyle birleştirildiğinde daha anlamlı hâle gelir.

## Kontrolcüye sağladığı avantaj

Faz analizi sayesinde kontrol sistemi ayağın yere temas zamanını ayarlayabilir, adım uzunluğunu değiştirebilir ve gövde momentumunu dengeleyebilir. Ayrıca farklı hızlardaki yürüyüşler tek bir faz koordinatında karşılaştırılabilir. Kısacası faz, robotun yalnızca **ne yaptığını** değil, hareketin **hangi bölümünde ve ne kadar kararlı biçimde** yaptığını söyler. Dengeli bir humanoid için doğru adım kadar, doğru anda atılan adım da belirleyicidir.
