---
layout: post
title: "Robotik Cerrahinin Perde Arkası: Ameliyat Robotlarını Yöneten Algoritmalar"
math: true
categories: 
  - Bilgi
tags: 
  - robotik cerrahi
  - algoritma
  - kontrol sistemleri
  - ters kinematik
  - yapay zeka
  - robotik
toc: true
image: /img/robotik-cerrahinin-perde-39.png
---

Robotik cerrahi dendiğinde gözümüzde ameliyatı tek başına yapan metal bir doktor canlanabilir. Gerçekte günümüzde kullanılan sistemlerin çoğu, cerrahın el hareketlerini hassas biçimde robot kollarına aktaran gelişmiş teleoperasyon platformlarıdır. Cerrah karar verir; robot ise bu kararı filtreleme, kinematik, kontrol ve güvenlik algoritmaları yardımıyla mikrometre düzeyinde harekete dönüştürür.
``

## Hareketin başlangıç noktası: teleoperasyon

Cerrah, konsoldaki kumandaları hareket ettirdiğinde sensörler konum, yönelim ve hız verilerini ölçer. Bu ham veriler doğrudan motora gönderilmez. Çünkü insan eli doğal olarak titrer, sensörlerde gürültü bulunur ve cerrahın geniş hareketlerinin hastanın içinde çok daha küçük hareketlere çevrilmesi gerekir.

Örneğin kumanda 5 santimetre hareket ettirilirken cerrahi aletin yalnızca 1 santimetre ilerlemesi istenebilir. Ölçekleme basitçe

$$x_r = s x_c$$

ile ifade edilebilir. Burada $x_c$ cerrahın hareketi, $x_r$ robotun hedef hareketi, $s$ ise ölçek katsayısıdır. $s=0.2$ olduğunda robot, cerrahın hareketinin beşte birini uygular.

| Algoritma katmanı | Görevi | Günlük hayattaki benzetme |
|---|---|---|
| Sinyal filtreleme | Titreme ve sensör gürültüsünü azaltır | Kameradaki görüntü sabitleme |
| Ters kinematik | Alet hedefini eklem açılarına çevirir | Eli uzatırken dirseği ayarlamak |
| Hareket planlama | Güvenli bir yol üretir | Navigasyonun rota çizmesi |
| Kontrol algoritması | Motorları hedefte tutar | Aracın hız sabitleyicisi |
| Güvenlik denetimi | Yasak hareketleri engeller | Sanal güvenlik bariyeri |

## Ters kinematik: Robot kolu nasıl bükülecek?

Cerrah alet ucunun nereye gitmesini istediğini belirtir; fakat robotun motorları doğrudan Kartezyen koordinatlarla çalışmaz. Her eklemin hangi açıya gelmesi gerektiği hesaplanmalıdır. İleri kinematikte eklem değerlerinden uç konumu bulunur:

$$p = f(q)$$

Ters kinematikte ise hedef konumdan eklem değerleri aranır:

$$q = f^{-1}(p)$$

Buradaki zorluk, aynı noktaya birden fazla eklem düzeniyle ulaşılabilmesi veya bazı hedeflerin fiziksel olarak erişilemez olmasıdır. Sayısal çözücüler, Jacobian matrisi üzerinden küçük eklem değişimlerini hesaplar: $v = J(q)\dot{q}$. Sistem ayrıca eklem sınırlarını, çarpışma riskini ve cerrahi aletin giriş noktasını korumak zorundadır.

## PID ve kuvvet kontrolü

Hedef eklem açısı bulunduktan sonra motorların bu hedefi düzgün izlemesi gerekir. En yaygın yaklaşımlardan biri PID kontroldür:

$$u(t)=K_p e(t)+K_i\int e(t)dt+K_d\frac{de(t)}{dt}$$

Oransal terim mevcut hataya tepki verir, integral terimi kalıcı sapmayı azaltır, türev terimi ise ani değişimleri frenler. Daha karmaşık sistemlerde model öngörülü kontrol, empedans kontrolü ve kuvvet geri bildirimi kullanılır. Empedans kontrolü, robotun dokuyla temas ederken taş gibi katı davranması yerine kontrollü bir esneklik göstermesini sağlar.

Aşağıdaki sade Python örneği, tek eksenli bir PID denetleyicinin hedef konuma yaklaşmasını gösterir:

```python
class PID:
    def __init__(self, kp, ki, kd):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.integral = 0.0
        self.previous_error = 0.0

    def update(self, target, position, dt):
        error = target - position
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt
        self.previous_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative
```

`update` metodunun ürettiği değer motor komutu olarak düşünülebilir. Gerçek ameliyat robotlarında buna tork sınırları, sensör doğrulama, gecikme telafisi ve acil durdurma kontrolleri eklenir.

## Yapay zeka ameliyatı devralıyor mu?

Makine öğrenmesi; anatomik yapıların görüntüde işaretlenmesi, alet takibi, dikiş aşamalarının tanınması ve riskli bölgelerin belirlenmesi için kullanılabilir. Ancak öğrenen modellerin tahminleri belirsizlik taşıdığı için kritik hareket kontrolü genellikle doğrulanabilir, deterministik algoritmalara bırakılır.

Robotik cerrahinin gerçek gücü tek bir “süper algoritmadan” değil; filtreleme, kinematik, kontrol, görüntü işleme ve güvenlik katmanlarının milisaniyeler içinde birlikte çalışmasından gelir. Robot yorulmaz ve titremeyi azaltır; fakat hedefi, stratejiyi ve klinik kararı hâlâ insan belirler.

![robotik-cerrahinin-perde-39](/img/robotik-cerrahinin-perde-39.svg)

