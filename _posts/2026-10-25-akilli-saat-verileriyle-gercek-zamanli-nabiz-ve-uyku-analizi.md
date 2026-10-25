---
layout: post
title: "Akıllı Saat Verileriyle Gerçek Zamanlı Nabız ve Uyku Analizi"
math: true
categories: 
  - Proje
tags: 
  - giyilebilir-teknoloji
  - sağlık-verisi
  - python
  - gerçek-zamanlı-analiz
  - sinyal-işleme
  - makine-öğrenmesi
toc: true
image: /img/akilli-saat-verileriyle-20.png
---

![akilli-saat-verileriyle-20](/img/akilli-saat-verileriyle-20.svg)


Akıllı saatler yalnızca saati gösteren cihazlar olmaktan çıkıp bileğimizde çalışan küçük sağlık laboratuvarlarına dönüştü. Nabız, hareket, kandaki oksijen oranı ve uyku gibi ölçümler; doğru algoritmalarla işlendiğinde anlamlı eğilimlere ve erken uyarılara dönüştürülebilir. Ancak ham sensör verisini doğrudan yorumlamak, rüzgârlı havada fısıltı dinlemeye benzer: Önce gürültüyü temizlemek gerekir.
``

## Sensörden anlamlı veriye

Akıllı saatler nabzı çoğunlukla **fotopletismografi (PPG)** yöntemiyle ölçer. Cihazın altındaki LED cilde ışık gönderir; fotodiyot ise geri yansıyan ışığın şiddetini ölçer. Kalp her attığında damarlardaki kan hacmi değiştiği için yansıma sinyalinde tepe noktaları oluşur.

Ardışık iki tepe arasındaki süre $\Delta t$ saniye ise yaklaşık nabız şu şekilde hesaplanır:

$$HR = \frac{60}{\Delta t}$$

Örneğin iki tepe arasındaki süre $0.8$ saniyeyse nabız $75$ BPM olur. Gerçek dünyada hareket, gevşek kayış, ter ve ortam ışığı sinyali bozabilir. Bu nedenle filtreleme, tepe tespiti ve güven puanı hesaplama aşamaları önemlidir.

| Yaklaşım | Avantajı | Dezavantajı | Kullanım alanı |
|---|---|---|---|
| Hareketli ortalama | Basit ve hızlıdır | Ani değişimleri yumuşatabilir | Canlı nabız göstergesi |
| Medyan filtresi | Sıçramaları temizler | Büyük pencere gecikme yaratır | Sensör hatalarının giderilmesi |
| Butterworth filtresi | Frekansları kontrollü süzer | Parametre ayarı gerekir | PPG sinyal işleme |
| Makine öğrenmesi | Karmaşık örüntüleri bulur | Etiketli veri gerektirir | Uyku evresi tahmini |

## Gerçek zamanlı nabız işleme

Aşağıdaki Python sınıfı, saatten geldiği varsayılan BPM değerlerini kayan pencereye ekler. Medyan kullanarak aykırı ölçümlerin etkisini azaltır ve son değerlerin değişkenliğine göre basit bir güven puanı üretir.

```python
from collections import deque
from statistics import median, pstdev

class HeartRateStream:
    def __init__(self, window_size=10):
        self.values = deque(maxlen=window_size)

    def update(self, bpm):
        if not 30 <= bpm <= 220:
            return {'status': 'invalid'}

        self.values.append(bpm)
        filtered = median(self.values)
        deviation = pstdev(self.values) if len(self.values) > 1 else 0
        confidence = max(0.0, 1.0 - deviation / 20)

        return {
            'status': 'ok',
            'bpm': round(filtered, 1),
            'confidence': round(confidence, 2)
        }

stream = HeartRateStream()
for measurement in [74, 76, 75, 140, 77, 76]:
    print(stream.update(measurement))
```

Buradaki `140` değeri tek başına geldiğinde medyanı dramatik biçimde değiştirmez. Bununla birlikte gerçek bir egzersiz sırasında yükselen nabzın yanlışlıkla gürültü sayılmaması için ivmeölçer verisi de kullanılmalıdır. Kullanıcı koşuyorsa yüksek nabız beklenebilir; koltukta oturuyorsa aynı ölçüm daha dikkat çekicidir.

## Uyku nasıl tahmin edilir?

Uyku analizi genellikle ivmeölçer hareketleri, nabız ve kalp atışları arasındaki değişkenliği birleştirir. Basit bir modelde düşük hareket ve düşen nabız uykuya işaret eder. Daha gelişmiş sistemler uyanıklık, hafif uyku, derin uyku ve REM sınıflarını tahmin eder.

Bir özellik vektörü şöyle tanımlanabilir:

$$x = [HR_{avg}, HRV, movement, oxygen]$$

Bu değerler karar ağacı, lojistik regresyon veya sinir ağına verilebilir. Başlangıç projesinde açıklanabilir olduğu için karar ağacı iyi bir seçimdir. Veriler 30 saniyelik ya da bir dakikalık pencerelere bölünerek her pencere için ortalama, standart sapma ve hareket toplamı hesaplanabilir.

## Sağlık verisinde kritik ayrıntılar

Gerçek zamanlı sistem, eksik paketleri ve Bluetooth kopmalarını yönetmelidir. Ölçümlere zaman damgası eklenmeli, veriler aktarımda ve depolamada şifrelenmeli, kullanıcıdan açık izin alınmalıdır. Ayrıca bu algoritmalar tıbbi teşhis koymamalıdır. “Düzensiz ölçüm algılandı” demek, “Kalp hastalığınız var” demekten hem teknik hem etik açıdan daha doğrudur.

Bu projeyi büyütmek için FastAPI ile veri kabul eden bir servis, WebSocket ile canlı panel ve kişiye özel normal değerleri öğrenen bir anomali modeli ekleyebilirsiniz. Böylece bilekte başlayan küçük sinyal, güvenli ve açıklanabilir bir sağlık analizi sistemine dönüşür.
