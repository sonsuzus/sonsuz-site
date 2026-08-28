---
layout: post
title: "CAP Teoremini E-Ticaret Sepetinde Simüle Etmek"
math: true
categories: 
  - Proje
tags: 
  - CAP Teoremi
  - Dağıtık Sistemler
  - E-Ticaret
---

Dağıtık sistemler, tek bir veritabanına güvenmek yerine veriyi birden fazla düğümde tutarak ölçeklenebilirlik ve hata toleransı sağlar. Ancak ağ bölünmesi yaşandığında sihirli bir biçimde hem her isteğe anında cevap verip hem de tüm kopyaları kusursuz biçimde eşitleyemezler. CAP teoremi bu zorunlu ödünleşimi görünür kılar. Bunu teorik bir üçgen olarak ezberlemek yerine, e-ticaret sepeti ve stok ekranı üzerinde küçük bir simülasyonla incelemek çok daha öğreticidir.

``

CAP; **Consistency (tutarlılık)**, **Availability (erişilebilirlik)** ve **Partition Tolerance (ağ bölünmesine dayanıklılık)** kavramlarının baş harflerinden oluşur. Ağ bölünmesi varken bir dağıtık sistem, aynı anda yalnızca tutarlılık veya erişilebilirlik lehine kesin karar verebilir. Buradaki tutarlılık, tüm istemcilerin her anda en güncel başarılı yazmayı görmesi anlamındaki doğrusal tutulmuş (linearizable) tutarlılıktır.

Matematiksel sezgiyle, iki replika için stok değeri $S_A$ ve $S_B$ olsun. Ağ sağlıklıyken ideal hedef şudur:

$$S_A(t) = S_B(t) = S_{gerçek}(t)$$

Bağlantı koptuğunda A düğümü sipariş alırken B düğümü ürün sayfasını sunmaya devam ediyorsa, eşitliği korumak için A'nın yazmayı reddetmesi gerekir. Yazmayı kabul ederse bir süreliğine $S_A(t) \ne S_B(t)$ oluşabilir. İşte CAP kararı tam burada ortaya çıkar.

| Tercih | Ağ bölünmesindeki davranış | E-ticaret örneği | Bedel |
|---|---|---|---|
| CP | Bazı istekleri bekletir veya reddeder | Stok doğrulanamıyorsa ödeme başlatılmaz | Kullanıcı hata/geri dönüş görür |
| AP | Her düğüm cevap vermeyi sürdürür | Sepete ekleme kabul edilir, stok sonra uzlaştırılır | Fazla satış veya eski veri riski |
| CA | Tutarlı ve erişilebilir görünür | Tek bölgedeki klasik veritabanı | Bölünmeye dayanıklı değildir |

Aşağıdaki Python örneği, iki depo düğümünün bağlantısı kesildiğinde AP yaklaşımının nasıl fazla satış üretebileceğini canlandırır. Her iki düğüm başlangıçta bir adet ürün görür; bağlantı kopunca ikisi de aynı ürünü satabilir.

```python
class StockNode:
    def __init__(self, name, stock):
        self.name = name
        self.stock = stock
        self.partitioned = False

    def buy_ap(self):
        # AP: Yerel düğüm cevap verir; diğer replikayı beklemez.
        if self.stock <= 0:
            return f"{self.name}: stok yok"
        self.stock -= 1
        return f"{self.name}: sipariş kabul edildi"

    def buy_cp(self):
        # CP: Bağlantı yoksa doğrulama yapılamaz, işlem reddedilir.
        if self.partitioned:
            return f"{self.name}: stok doğrulanamadı, tekrar deneyin"
        return self.buy_ap()

warehouse_a = StockNode("İstanbul", 1)
warehouse_b = StockNode("Ankara", 1)
warehouse_a.partitioned = warehouse_b.partitioned = True

print(warehouse_a.buy_ap())
print(warehouse_b.buy_ap())
print("Toplam fiziksel ürün: 1, kabul edilen sipariş: 2")
```

Bu kodda problem `buy_ap` metodunun hatalı olması değildir; yöntem bilinçli olarak erişilebilirliği seçer. Gerçek bir pazaryerinde sepet işlemi AP olabilir çünkü kullanıcı deneyimi önemlidir. Buna karşılık ödeme alma, kuponun tek kullanımlılığı veya son ürünü ayırma gibi kritik adımlar CP karakteri taşıyabilir. Böylece sistem, her veriye aynı CAP politikasını uygulamak yerine iş kuralına göre karar verir.

Pratikte AP seçen ekipler çatışma çözümü de tasarlamalıdır. Siparişlere benzersiz kimlik vermek, olay günlüğü tutmak, stok rezervasyonu için zaman aşımı kullanmak ve uzlaştırma kuyruğu çalıştırmak yaygın tekniklerdir. CP seçen ekipler ise kullanıcıya anlaşılır hata mesajları, güvenli tekrar deneme anahtarları ve alternatif bölge yönlendirmesi sağlamalıdır.

Sonuç olarak CAP, “hangi veritabanı daha iyi?” sorusunun kısa cevabı değildir. Daha doğru soru şudur: **Ağ koparsa hangi e-ticaret işlemini durdurabilir, hangisini sonradan telafi edebiliriz?** Sepet, stok, ödeme ve teslimat için bu soruyu ayrı ayrı yanıtlamak, teoriyi üretim mimarisine dönüştürmenin en sağlam yoludur.
