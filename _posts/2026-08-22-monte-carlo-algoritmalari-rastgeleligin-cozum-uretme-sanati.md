---
layout: post
title: "Monte Carlo Algoritmaları: Rastgeleliğin Çözüm Üretme Sanatı"
math: true
categories: 
  - Bilgi
tags: 
  - Monte Carlo
  - Rastgele Algoritmalar
  - Python
---

Bir algoritmanın zar atarak ciddi bir problemi çözmesi ilk anda şaka gibi gelebilir. Oysa Monte Carlo algoritmaları, belirsizliği kontrollü örneklemeye dönüştürür: Çok sayıda rastgele deneme yapar, sonuçların istatistiksel davranışını gözlemler ve yaklaşık ya da olasılıksal bir cevap üretir. Özellikle kesin çözümün pahalı olduğu yüksek boyutlu problemlerde, fizik simülasyonlarında, finansal risk analizinde ve makine öğrenmesinde güçlü bir araçtır.

``

Monte Carlo yaklaşımının temel fikri oldukça basittir: Hesaplamak istediğimiz değeri doğrudan formülle bulmak zor ise, o değeri temsil eden rastgele deneyler tasarlarız. Deney sayısı $N$ arttıkça elde edilen tahmin genellikle gerçek değere yaklaşır. Bunun arkasında **Büyük Sayılar Yasası** vardır. Bağımsız örneklerin ortalaması, beklenen değere yakınsar:

$$\frac{1}{N}\sum_{i=1}^{N} X_i \xrightarrow[N \to \infty]{} \mathbb{E}[X]$$

Buradaki kritik kelime “yaklaşır”dır. Monte Carlo çoğu zaman kesin cevap vaat etmez; hata payı olan, fakat hata davranışı ölçülebilir bir cevap verir. Tipik örnekleme hatası yaklaşık olarak $O(1/\sqrt{N})$ ölçeğindedir. Yani hatayı yarıya indirmek için yaklaşık dört kat fazla örnek gerekir. Rastgeleliğin faturası budur.

| Yaklaşım | Sonuç türü | Güçlü yönü | Sınırlaması |
|---|---|---|---|
| Deterministik algoritma | Kesin sonuç | Tekrarlanabilir ve net | Karmaşık uzaylarda pahalı olabilir |
| Monte Carlo | Olasılıksal/yaklaşık sonuç | Büyük ve karmaşık uzaylarda esnek | Örnek sayısı, doğruluğu belirler |
| Las Vegas algoritması | Kesin sonuç, rastgele süre | Doğruluk garantisi | Çalışma süresi değişkendir |

Klasik bir örnekle başlayalım: $\pi$ sayısını tahmin etmek. Kenar uzunluğu 2 olan bir karenin içine, yarıçapı 1 olan bir çeyrek daire yerleştirelim. Kareye rastgele atılan noktaların daire içinde kalma olasılığı alan oranına eşittir:

$$P(\text{daire içinde}) = \frac{\pi}{4}$$

Daire içine düşen nokta sayısı $k$, toplam nokta sayısı $N$ ise $\pi \approx 4k/N$ olur. Aşağıdaki Python kodu bu fikri uygular:

```python
import random

def pi_tahmin_et(ornek_sayisi: int) -> float:
    icerde = 0

    for _ in range(ornek_sayisi):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1:
            icerde += 1

    return 4 * icerde / ornek_sayisi

print(pi_tahmin_et(1_000_000))
```

Kod, $[0,1] \times [0,1]$ karesinde noktalar üretir. `x*x + y*y <= 1` koşulu, noktanın birim çeyrek dairenin içinde olup olmadığını test eder. Her çalıştırmada sonuç biraz değişir; bu hata değil, algoritmanın doğasıdır. Test edilebilirlik gerektiğinde `random.seed(42)` ile rastgele sayı üretecini sabitlemek yararlıdır.

Monte Carlo yalnızca geometrik alan hesaplamaz. Örneğin integral hesabında, $x$ değerlerini uygun dağılımdan seçip $f(x)$ fonksiyonunun ortalamasını alarak integral tahmini yapılabilir. Finans dünyasında binlerce olası fiyat senaryosu üretilir; her senaryodaki getiri hesaplanır ve risk ölçülür. Oyun yapay zekâsında ise Monte Carlo Tree Search, gelecek hamleleri rastgele oynatarak umut vadeden hamleleri seçer.

| Problem | Rastgele deney | Tahmin edilen çıktı |
|---|---|---|
| $\pi$ hesabı | Kareye nokta atma | Alan oranı |
| İntegral | Rastgele $x$ örnekleme | Fonksiyon ortalaması |
| Finans | Fiyat yolu simülasyonu | Beklenen getiri/risk |
| Oyun ağacı | Rastgele oyun sonlandırma | Hamle başarısı |

Başarılı bir Monte Carlo tasarımı için üç soru sorulmalıdır: Örnekler hedef dağılımı gerçekten temsil ediyor mu? Kaç örnek kabul edilebilir hata sağlar? Nadir ama önemli olaylar yeterince görülüyor mu? Son soru özellikle önemlidir; çok düşük olasılıklı riskler sıradan rastgele örneklemede gözden kaçabilir. Bu durumda importance sampling gibi yöntemler, önemli bölgeleri daha sık örnekleyerek verimliliği artırır.

Özetle Monte Carlo, rastgeleliği “gürültü” olmaktan çıkarıp hesaplama kaynağına dönüştürür. Mükemmel cevabı kovalamak yerine, belirsizliği ölçerek yeterince iyi cevaba hızlı ulaşır. Bazen çözüm, formülü daha çok zorlamakta değil; akıllıca tasarlanmış milyonlarca küçük zar atışındadır.
