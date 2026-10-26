---
layout: post
title: "Tool-Assisted Speedrun: Kusursuz Oyun Koşularının Bilimi"
math: true
categories: 
  - Bilgi
tags: 
  - tas
  - speedrun
  - oyun geliştirme
  - emülasyon
  - algoritma
  - optimizasyon
toc: true
image: /img/tool-assisted-speedrun-24.png
---

Bir karakterin aynı karede hem mermiden kaçıp hem duvardan sekerek bölüm sonu canavarını saniyeler içinde yenmesi insanüstü görünebilir. Tool-Assisted Speedrun, kısaca TAS, tam olarak bu tür koşuları üretmek için emülatörlerin, kare kare giriş düzenlemenin ve yazılım araçlarının kullanıldığı teknik bir oyun optimizasyonu disiplinidir.
``
TAS'ın amacı genellikle oyunu gerçek zamanlı oynamak değil, teorik olarak mümkün olan en hızlı veya en etkileyici giriş dizisini oluşturmaktır. Oyuncu reflekslerinin yerini dikkatli analiz alır; ancak ortaya çıkan hareketlerin tamamı oyunun kabul ettiği kontrol girdilerinden oluşur. Başka bir deyişle araç, oyunun kurallarını değiştirmez; doğru tuşa doğru karede basmayı kolaylaştırır.

## Bir TAS nasıl çalışır?

Dijital oyunlar zamanı çoğunlukla karelerle ölçer. Saniyede 60 kare çalışan bir oyunda tek karenin süresi yaklaşık olarak

$$
t_f = \frac{1}{60} \approx 0{,}0167\text{ saniye}
$$

olur. İnsanların görsel uyarılara tepki süresi yaklaşık 150–250 milisaniyeyken TAS üreticisi girdiyi tek kare, yani yaklaşık 16,7 milisaniye hassasiyetle yerleştirebilir. Üstelik gerekirse oyunu yavaşlatabilir veya tamamen durdurabilir.

| Özellik | Gerçek zamanlı speedrun | TAS koşusu |
|---|---|---|
| Girdi yöntemi | Fiziksel kontrolcü | Kare tabanlı giriş dosyası |
| Hata düzeltme | Koşuyu yeniden başlatma | Save state'e geri dönme |
| Hassasiyet | İnsan refleksiyle sınırlı | Tek kare düzeyi |
| Rastgelelik | Anlık yönetilir | Analiz edilip yönlendirilebilir |
| Temel hedef | İnsan performansı | Teorik optimizasyon |

### Temel araçlar

**Frame advance**, oyunu her komutta yalnızca bir kare ilerletir. **Save state**, belirli bir ana dönerek farklı girdilerin denenmesini sağlar. **Input recording** ise kullanılan tuşları video yerine küçük bir veri dosyasında saklar. Emülatör aynı başlangıç durumunda aynı girdileri aldığında aynı sonucu üretir; buna determinizm denir.

Basitleştirilmiş biçimde oyun durumu şöyle modellenebilir:

$$
S_{n+1} = F(S_n, I_n)
$$

Burada $S_n$ mevcut oyun durumunu, $I_n$ ilgili karedeki kontrol girdisini, $F$ ise oyunun güncelleme kurallarını temsil eder. TAS dosyası aslında $I_0, I_1, \ldots, I_k$ dizisidir. Video yalnızca bu dizinin çalıştırılmasıyla elde edilen sonuçtur.

## Yazılım en iyi girdiyi nasıl arar?

Kısa bölümlerde olası girdiler programla taranabilir. Aşağıdaki Python örneği, sağa gitme ve zıplama seçeneklerinin dört karelik bütün kombinasyonlarını üretir:

```python
from itertools import product

inputs = ["bekle", "sağ", "zıpla", "sağ+zıpla"]

def skor(sequence):
    # Gerçekte burada emülatörden konum ve süre okunabilir.
    return sum(2 if "sağ" in action else 0 for action in sequence)

candidates = product(inputs, repeat=4)
best = max(candidates, key=skor)
print(best, skor(best))
```

Bu kod oyuncunun yerine doğrudan oyun oynamaz; olası giriş dizilerini üretip tanımlanan skora göre karşılaştırır. Gerçek projelerde arama uzayı çok hızlı büyür. Her karede dört seçenek varsa $n$ kare için kombinasyon sayısı $4^n$ olur. Bu nedenle brute force yerine sezgisel arama, dalları budama, bellek izleme ve oyun fiziğine özel botlar kullanılır.

## RNG manipülasyonu ve küçük tuhaflıklar

Rastgele sayı üreteçleri çoğu eski oyunda gerçekten rastgele değildir. Bir başlangıç tohumu ve önceki durum üzerinden hesaplanırlar. Oyuncu bir kare bekleyerek, farklı yöne bakarak veya menüyü açarak sonraki düşman davranışını değiştirebilir. Böylece istenen eşyanın düşmesi ya da bir saldırının gerçekleşmemesi sağlanabilir.

TAS üreticileri ayrıca hız taşması, duvar kırpma, yanlış warp ve gecikme azaltma gibi teknikleri inceler. Bazen daha az nesnenin ekranda kalmasını sağlamak, oyun motorunun daha az yavaşlamasına ve toplam sürenin düşmesine yardım eder.

TAS bir hile gösterisinden çok deneysel bir laboratuvardır: fizik kuralları ölçülür, rotalar karşılaştırılır ve her kare optimize edilir. Sonuçta ortaya yalnızca hızlı bir video değil, oyunun sınırlarını belgeleyen yeniden üretilebilir bir yazılım eseri çıkar.

![tool-assisted-speedrun-24](/img/tool-assisted-speedrun-24.svg)

