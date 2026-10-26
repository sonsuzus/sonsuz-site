---
layout: post
title: "Akıllı Tarımda Edge Computing: Tarlanın Kendi Beyni"
math: true
categories: 
  - Bilgi
tags: 
  - akıllı tarım
  - edge computing
  - nesnelerin interneti
  - sensörler
  - yapay zeka
  - iot
toc: true
image: /img/akilli-tarimda-edge-45.png
---

![akilli-tarimda-edge-45](/img/akilli-tarimda-edge-45.svg)


Toprak nemini ölçen bir sensörün karar vermek için kilometrelerce uzaktaki bulut sunucusunu beklediğini düşünün. Bu sırada bağlantı kesilir, yanıt gecikir ve susuz kalan domatesler sessizce dram yaşar! Edge computing, sensör verisini doğrudan tarladaki ağ geçidi, mikrodenetleyici veya mini bilgisayar üzerinde işleyerek bu sorunu çözer. Böylece tarımsal sistemler daha hızlı, dayanıklı ve ekonomik hâle gelir.

``

## Edge computing nedir?

Geleneksel IoT mimarisinde sensörlerden alınan ham veriler internete aktarılır, bulutta analiz edilir ve sonuç tekrar sahadaki cihaza gönderilir. Edge computing yaklaşımında ise hesaplama, verinin üretildiği noktaya mümkün olduğunca yaklaştırılır. Bir Raspberry Pi, endüstriyel ağ geçidi veya yapay zekâ destekli kamera bu “kenar” görevini üstlenebilir.

Bir sulama kararının toplam gecikmesini basitçe şöyle gösterebiliriz:

$$T_{toplam} = T_{iletim} + T_{işleme} + T_{yanıt}$$

Bulut tabanlı yapıda iletim ve yanıt süreleri internet kalitesine bağlıdır. Edge cihazında ise veri yerel işlendiği için $T_{iletim}$ büyük ölçüde azalır. Milisaniyelerin kritik olduğu don, yangın veya hayvan hareketi tespiti gibi senaryolarda bu fark oldukça önemlidir.

| Özellik | Bulut bilişim | Edge computing |
|---|---|---|
| Gecikme | İnternet bağlantısına bağlı | Genellikle çok düşük |
| Bant genişliği | Ham veri nedeniyle yüksek | Özet veriyle düşük |
| Çevrimdışı çalışma | Sınırlı | Büyük ölçüde mümkün |
| Veri mahremiyeti | Veri dış sunucuya gider | Veri sahada tutulabilir |
| İşlem kapasitesi | Çok yüksek | Donanıma göre sınırlı |

## Tarlada veri nasıl işlenir?

Bir akıllı sulama sisteminde nem, sıcaklık ve yağış sensörleri belirli aralıklarla ölçüm yapar. Edge cihazı önce hatalı okumaları filtreler, ardından eşik veya makine öğrenmesi modeline göre karar verir. Yalnızca günlük ortalamalar, uyarılar ve cihaz sağlık bilgileri buluta gönderilir.

Örneğin, nem sensöründeki ani sıçramaları yumuşatmak için hareketli ortalama kullanılabilir:

$$\bar{x}_t = \frac{1}{n}\sum_{i=0}^{n-1}x_{t-i}$$

Burada $n$, dikkate alınan son ölçüm sayısıdır. Bu yöntem, tek bir hatalı değerin sulama pompasını gereksiz yere çalıştırmasını önler.

Aşağıdaki Python kodu, beş nem ölçümünün ortalamasını hesaplayıp yerel bir sulama kararı üretir:

```python
from statistics import mean

NEM_ESIGI = 35


def sulama_karari(olcumler, yagmur_bekleniyor=False):
    filtrelenmis_nem = mean(olcumler[-5:])

    if filtrelenmis_nem < NEM_ESIGI and not yagmur_bekleniyor:
        return "Pompayı çalıştır"
    return "Sulama gerekmiyor"

nem_verileri = [37, 34, 33, 32, 31]
print(sulama_karari(nem_verileri))
```

Kod, son beş değeri kullanarak sensör gürültüsünün etkisini azaltır. Gerçek sistemde sonuç bir röle üzerinden pompayı kontrol edebilir. Yağış tahmini önceden edge cihazına aktarılmışsa gereksiz sulama da engellenir.

## Yapay zekâ tarlanın kenarına taşınırsa

Edge cihazları yalnızca eşik kontrolü yapmaz. Sıkıştırılmış görüntü sınıflandırma modelleriyle yaprak hastalıkları, yabancı otlar veya zararlılar kameradan tespit edilebilir. Kamera görüntüsünün tamamını buluta göndermek yerine yalnızca “üç bitkide hastalık şüphesi var” sonucu iletilir. Bu yaklaşım hem bant genişliğini hem de depolama maliyetini düşürür.

Ancak edge donanımının enerji, bellek ve işlem gücü sınırlıdır. Model küçültme, niceleme ve uyku modları bu nedenle önem kazanır. Güneş paneliyle çalışan bir cihazda doğruluk kadar enerji tüketimi de başarı ölçütüdür:

$$Verim = \frac{Doğru\ karar\ sayısı}{Tüketilen\ enerji}$$

## Hibrit yaklaşım en güçlü seçenek

Edge computing bulutun rakibi değil, tamamlayıcısıdır. Anlık sulama ve alarm kararları sahada alınırken uzun dönemli verim analizi, model eğitimi ve filo yönetimi bulutta gerçekleştirilebilir. Sonuçta çiftçi bağlantı kesilse bile çalışan, kritik veriye hızlı tepki veren ve internet faturasını kabartmayan bir sisteme sahip olur. Kısacası tarla yalnızca ürün değil, karar da üretmeye başlar.
