---
layout: post
title: "Bulut Oyun Teknolojisi: Tuşa Basınca Uzak Sunucuda Neler Oluyor?"
math: true
categories: 
  - Bilgi
tags: 
  - bulut oyun
  - cloud gaming
  - oyun teknolojileri
  - ağ gecikmesi
  - video akışı
  - sunucu altyapısı
toc: true
image: /img/bulut-oyun-teknolojisi-91.png
---

Güçlü bir ekran kartına sahip olmadan yüksek kaliteli oyunları çalıştırmak sihir gibi görünebilir. Bulut oyun teknolojisinde oyun aslında telefonunuzda, televizyonunuzda veya eski dizüstü bilgisayarınızda çalışmaz. Uzak bir veri merkezindeki güçlü sunucu oyunu işler; ortaya çıkan görüntüler sıkıştırılarak internet üzerinden size gönderilir. Siz de yalnızca canlı videoyu izler ve kontrol komutlarını sunucuya iletirsiniz.
``
## Bulut oyun döngüsü nasıl çalışır?

Sistem, oyuncunun bir tuşa basmasıyla başlayan sürekli bir veri alışverişi üzerine kuruludur. Klavye, fare veya oyun kolundan alınan komut önce istemci uygulaması tarafından küçük bir ağ paketine dönüştürülür. Paket sunucuya ulaştığında oyun motoru yeni durumu hesaplar, ekran kartı kareyi oluşturur ve video kodlayıcı bu kareyi sıkıştırır. Son olarak görüntü istemciye gönderilip ekranda gösterilir.

Bu zincirin toplam gecikmesi kabaca şöyle modellenebilir:

$$T_{toplam} = T_{gidiş} + T_{işleme} + T_{kodlama} + T_{dönüş} + T_{çözme}$$

Örneğin komutun sunucuya ulaşması 20 ms, oyunun kareyi üretmesi 12 ms, kodlama ve çözme işlemleri toplam 15 ms, görüntünün dönüşü ise 20 ms sürerse gecikme yaklaşık $67\,ms$ olur. Bu değer strateji oyunlarında kabul edilebilirken rekabetçi bir nişancı oyununda oyuncuya belirgin gelebilir.

## Yerel oyun ile bulut oyunun karşılaştırması

| Özellik | Yerel oyun | Bulut oyun |
|---|---|---|
| Grafik işlemi | Kullanıcının cihazında | Uzak sunucuda |
| Donanım ihtiyacı | Genellikle yüksek | Düşük veya orta |
| İnternet bağımlılığı | Çevrimdışı oyunlarda az | Çok yüksek |
| Giriş gecikmesi | Genellikle düşük | Ağ koşullarına bağlı |
| Güncelleme | Cihaza indirilir | Sunucuda uygulanır |
| Görüntü kalitesi | Yerel ve kayıpsız olabilir | Sıkıştırma izleri görülebilir |

![bulut-oyun-teknolojisi-91](/img/bulut-oyun-teknolojisi-91.svg)


Bulut oyun cihaz maliyetini azaltır; ancak hesaplama yükünü ortadan kaldırmaz, yalnızca veri merkezine taşır. Sunucularda güçlü GPU'lar, çok çekirdekli işlemciler ve hızlı depolama sistemleri bulunur. Aynı fiziksel GPU, sanallaştırma teknolojileri sayesinde birden fazla oyuncuya bölüştürülebilir.

## Video akışı neden kritik?

Ham görüntüleri internetten göndermek pratik değildir. Saniyede 60 kare üreten, 1920×1080 çözünürlüklü ve piksel başına 24 bit kullanan sıkıştırılmamış bir akışın yaklaşık veri hızı şöyledir:

$$1920 \times 1080 \times 24 \times 60 \approx 2.99\text{ Gbit/s}$$

Bu nedenle H.264, H.265 veya AV1 gibi kodekler kullanılır. Kodek, birbirini takip eden karelerde değişmeyen bölgeleri tekrar göndermek yerine hareket ve fark bilgilerini taşır. Böylece gerekli bant genişliği çoğu senaryoda 15–50 Mbit/s aralığına düşebilir. Buna karşılık daha güçlü sıkıştırma, kodlama süresini veya görüntü bozulmasını artırabilir.

## Ağ kalitesi yalnızca hız değildir

Yüksek indirme hızı tek başına kusursuz deneyim sağlamaz. **Ping**, paketin gidiş-dönüş süresini; **jitter**, gecikmedeki düzensizliği; **paket kaybı** ise ulaşmayan veri oranını belirtir. Video aktarımında çoğunlukla düşük gecikmeli UDP tabanlı protokoller tercih edilir. Kayıp bir paketin yeniden gönderilmesini beklemek yerine sonraki karenin gösterilmesi, oyunun donmasını engelleyebilir.

Aşağıdaki basit Python kodu, yaklaşık toplam gecikmeyi hesaplar:

```python
def bulut_oyun_gecikmesi(gidis, isleme, kodlama, donus, cozme):
    return gidis + isleme + kodlama + donus + cozme

gecikme = bulut_oyun_gecikmesi(18, 10, 8, 18, 6)
print(f"Tahmini gecikme: {gecikme} ms")
```

Gerçek sistemler ağ durumunu sürekli ölçerek bit hızını ve çözünürlüğü dinamik biçimde değiştirir. Bağlantı kötüleştiğinde 4K görüntüyü korumaya çalışmak yerine çözünürlüğü düşürmek, oynanabilirliği sürdürür.

## Gelecekte bizi ne bekliyor?

Edge computing sayesinde oyun sunucuları oyunculara daha yakın noktalara yerleştiriliyor. 5G, gelişmiş AV1 kodlayıcıları ve gecikme tahmin teknikleri de deneyimi iyileştiriyor. Bulut oyun, güçlü bilgisayarları tamamen gereksiz kılmasa da donanımı bir ürün olmaktan çıkarıp uzaktan erişilen bir hizmete dönüştürüyor. Kısacası geleceğin oyun konsolu, salonunuzdaki kutudan çok size en yakın veri merkezindeki sunucu olabilir.
