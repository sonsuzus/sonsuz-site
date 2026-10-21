---
layout: post
title: "Robotik Enkoderlerde Konum Hafızası: Mutlak ve Artımlı Enkoderler"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - enkoder
  - otomasyon
  - konum-kontrolü
  - sensörler
  - gömülü-sistemler
toc: true
image: /img/robotik-enkoderlerde-konum-72.png
---

![robotik-enkoderlerde-konum-72](/img/robotik-enkoderlerde-konum-72.svg)


Bir robot kolunun elektrik kesildikten sonra eklemlerinin nerede olduğunu hâlâ bilmesi sihir değildir; doğru enkoder seçimidir. Motor milinin veya mekanik bir eksenin açısal konumunu ölçen enkoderler, hareket kontrol sistemlerinin gözü gibidir. Ancak mutlak (absolute) ve artımlı (incremental) enkoderler konumu aynı biçimde anlatmaz: biri doğrudan adres verirken diğeri atılan adımları sayar.
``
## Enkoder neyi ölçer?

Döner enkoder, mil hareketini elektriksel sinyallere dönüştürür. Ölçülen temel büyüklük açısal konumdur. Bir tam tur $360^\circ$ veya $2\pi$ radyan olduğuna göre, tur başına $N$ farklı konum üreten bir enkoderin teorik çözünürlüğü şöyledir:

$$
\Delta\theta = \frac{360^\circ}{N}
$$

Örneğin 1024 konumlu bir enkoder için çözünürlük yaklaşık $0{,}3516^\circ$ olur. Fakat “kaç farklı konum ölçülüyor?” sorusu kadar, “bu konum bilgisi nasıl saklanıyor?” sorusu da önemlidir.

## Artımlı enkoder: Hareketin muhasebecisi

Artımlı enkoder, mil döndükçe A ve B kanallarında darbeler üretir. Denetleyici bu darbeleri sayarak başlangıç noktasına göre bağıl konumu hesaplar:

$$
\theta = \theta_0 + \frac{C}{P}\times360^\circ
$$

Burada $C$ sayılan darbe miktarı, $P$ ise kullanılan sayım yöntemine göre bir turdaki toplam sayımdır. A ve B sinyalleri arasında faz farkı bulunduğundan dönüş yönü de anlaşılır. Bazı modellerdeki Z kanalı ise her turda bir kez referans darbesi verir.

Önemli nokta şudur: Artımlı enkoder kendi başına “mil 127 derecede” demez. Yalnızca “başlangıçtan beri şu kadar ilerledim” der. Güç kesildiğinde denetleyicideki sayaç kaybolursa konum bilgisi de kaybolabilir. Bu nedenle açılışta limit anahtarına ilerleme veya Z darbesini arama gibi bir homing işlemi gerekir.

## Mutlak enkoder: Her konumun kimliği vardır

Mutlak enkoderde her mekanik konuma özgü bir dijital kod atanır. Mil dururken veya sistem yeniden açıldığında kod okunarak konum doğrudan belirlenebilir. Bu yaklaşım, apartman merdivenlerini saymak yerine kapının üzerindeki numaraya bakmaya benzer.

Tek turlu modeller bir tur içindeki açıyı bildirir. Çok turlu modeller ise hem tur içi açıyı hem de tamamlanan tur sayısını korur. Haberleşme SSI, BiSS-C, CANopen veya EtherCAT gibi arayüzlerle gerçekleştirilebilir. Kodlama sırasında geçiş hatalarını azaltmak için sıklıkla Gray kodu kullanılır; komşu iki konum arasında yalnızca bir bit değişir.

| Özellik | Artımlı enkoder | Mutlak enkoder |
|---|---|---|
| Konum türü | Başlangıca göre bağıl | Doğrudan ve benzersiz |
| Güç sonrası konum | Genellikle kaybolur | Yeniden okunabilir |
| Homing ihtiyacı | Çoğunlukla vardır | Çoğunlukla yoktur |
| Çıkış | A/B/Z darbeleri | Dijital konum kelimesi |
| Maliyet | Daha düşük | Daha yüksek |
| Tipik kullanım | Hız kontrolü, konveyör | Robot kolu, güvenli eksen |

## Küçük bir artımlı sayıcı örneği

Aşağıdaki Python kodu, dört kat kenar sayımıyla elde edilen sayacı açıya dönüştürür. Gerçek sistemlerde sayaç, mikrodenetleyicinin kesme veya donanımsal encoder birimiyle güncellenir.

```python
PPR = 1024
quadrature_factor = 4
counts_per_rev = PPR * quadrature_factor

def position_deg(counter):
    normalized = counter % counts_per_rev
    return normalized * 360.0 / counts_per_rev

print(position_deg(1536))  # 135 derece
```

Kod yalnızca sayacı yorumlar; başlangıç referansını kendiliğinden keşfetmez. Sayaç yanlış başlatılırsa hesaplanan açı da aynı miktarda kayar. Mutlak enkoderde ise okunan sayısal değer, uygun ölçekleme ile doğrudan açıya çevrilir.

## Hangisi seçilmeli?

Elektrik kesintisinden sonra eksenin hareket ettirilmeden bilinmesi gerekiyorsa mutlak enkoder güçlü adaydır. Maliyet kritikse, açılışta referanslama yapılabiliyorsa veya temel hedef hız ölçmekse artımlı enkoder yeterli olabilir. Robotik uygulamalarda karar yalnız çözünürlüğe göre verilmemelidir; güvenlik, kablolama, haberleşme gecikmesi, maksimum hız ve homing süresi de değerlendirilmelidir. Kısacası artımlı enkoder yolculuğu sayar, mutlak enkoder ise bulunduğu adresi bilir.
