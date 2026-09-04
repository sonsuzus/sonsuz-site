---
layout: post
title: "Uç Bilişim Mimarisi: Veriyi Buluta Uğurlamadan İşlemek"
math: true
categories: 
  - Bilgi
tags: 
  - uç bilişim
  - edge computing
  - dağıtık sistemler
toc: true
---

Akıllı bir kamera düşünün: Karşıdan gelen yayayı fark etmek için görüntüyü kilometrelerce uzaktaki buluta gönderip yanıt bekliyor. İnternet kısa süreliğine yavaşlarsa kamera da düşünme molasına çıkıyor! Uç bilişim, veriyi üretildiği cihazda veya yakındaki bir ağ düğümünde işleyerek bu bağımlılığı azaltır. Böylece daha hızlı kararlar, daha düşük bant genişliği tüketimi ve daha güçlü veri gizliliği elde edilir.

``

## Uç bilişim tam olarak nedir?

Geleneksel bulut mimarisinde sensör, telefon veya kamera tarafından üretilen veri merkezi bir veri merkezine gönderilir. Hesaplama bulutta gerçekleştirilir ve sonuç cihaza geri döner. Uç bilişimde ise hesaplama; cihazın işlemcisinde, yerel bir ağ geçidinde ya da kullanıcıya yakın konumlandırılmış mikro veri merkezinde yapılır.

Buradaki **uç**, ağın verinin üretildiği noktaya yakın bölümüdür. Bir fabrikadaki endüstriyel bilgisayar, baz istasyonundaki sunucu veya otomobilin kontrol ünitesi uç düğüm olabilir.

Toplam yanıt süresini kabaca şöyle modelleyebiliriz:

$$
T_{toplam} = T_{iletim} + T_{kuyruk} + T_{işleme} + T_{geri\ dönüş}
$$

Buluta gidildiğinde iletim ve geri dönüş süreleri büyür. İşlem uçta yapıldığında bu iki bileşen ciddi ölçüde küçülür. Ancak gecikme fiziksel olarak **tam sıfır olmaz**; işlemci süresi, ağ aktarımı ve işletim sistemi zamanlaması devam eder. Bu nedenle “sıfır gecikme” yerine **çok düşük veya sıfıra yakın gecikme** demek daha doğrudur.

## Bulut ve uç bilişim karşılaştırması

| Özellik | Bulut bilişim | Uç bilişim |
|---|---|---|
| İşleme konumu | Merkezi veri merkezi | Cihaz veya yakın düğüm |
| Gecikme | Ağ mesafesine bağlı | Genellikle çok düşük |
| İnternet bağımlılığı | Yüksek | Düşük veya orta |
| Gizlilik | Veri dış sisteme taşınabilir | Veri yerelde tutulabilir |
| İşlem kapasitesi | Çok yüksek | Donanımla sınırlı |
| Yönetim | Merkezi ve kolay | Dağıtık ve daha karmaşık |

Uç bilişim bulutun rakibi değil, takım arkadaşıdır. Acil kararlar uçta alınırken model eğitimi, uzun dönemli analiz ve arşivleme bulutta gerçekleştirilebilir. Bu yaklaşıma **hibrit mimari** denir.

## Basit bir karar mekanizması

Aşağıdaki Python örneği, sıcaklık verisini yerel olarak değerlendirir. Kritik olmayan ölçümler toplu analiz için buluta gönderilebilirken tehlikeli durumda ağ yanıtı beklenmeden alarm üretilir.

```python
CRITICAL_TEMPERATURE = 80

def process_at_edge(temperature):
    if temperature >= CRITICAL_TEMPERATURE:
        activate_alarm()
        stop_machine()
        return 'Yerel acil durum işlemi uygulandı'

    queue_for_cloud(temperature)
    return 'Veri bulut analizi için sıraya alındı'
```

Kodun önemli noktası yalnızca `if` koşulu değildir; kararın **nerede** verildiğidir. Makineyi durdurma komutu uzak sunucudan gelmediği için bağlantı kopsa bile güvenlik mekanizması çalışabilir.

## Mimari katmanlar

Tipik bir uç bilişim sistemi üç katmandan oluşur:

1. **Cihaz katmanı:** Sensörler, kameralar ve makineler ham veriyi üretir.
2. **Uç katmanı:** Ağ geçitleri veriyi filtreler, dönüştürür ve gerçek zamanlı karar verir.
3. **Bulut katmanı:** Büyük veri analizi, yapay zekâ modeli eğitimi ve merkezi yönetim sağlar.

Örneğin saniyede $30$ kare üreten 100 kamera, her kareyi buluta yolladığında ciddi trafik oluşturur. Uç düğüm yalnızca şüpheli olayların yüzde 2’sini gönderirse yaklaşık veri azaltma oranı şöyledir:

$$
Azaltma = 1 - 0.02 = 0.98 = \%98
$$

## Nerelerde kullanılır?

Otonom araçlarda fren kararı, fabrikalarda arıza tespiti, hastanelerde hasta takibi ve mağazalarda görüntü analizi başlıca kullanım alanlarıdır. Buna karşın sınırlı işlem gücü, cihaz güncellemeleri, fiziksel güvenlik ve binlerce dağıtık düğümün izlenmesi önemli zorluklardır.

Kısacası uç bilişim, her veriyi refleks olarak buluta göndermek yerine “Bu karar burada verilebilir mi?” sorusunu sorar. Cevap evetse veri kısa bir yolculuk yapar, sistem hızlanır ve bulutun omuzlarındaki yük hafifler.
