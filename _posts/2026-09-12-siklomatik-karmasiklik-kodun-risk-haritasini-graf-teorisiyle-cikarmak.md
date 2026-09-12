---
layout: post
title: "Siklomatik Karmaşıklık: Kodun Risk Haritasını Graf Teorisiyle Çıkarmak"
math: true
categories: 
  - Bilgi
tags: 
  - siklomatik karmaşıklık
  - kod kalitesi
  - graf teorisi
toc: true
---

Bir fonksiyon çalışıyor olabilir; peki onu güvenle değiştirebilir misiniz? İç içe koşullar, döngüler ve farklı çıkış yolları çoğaldıkça kod, küçük bir değişikliğin beklenmedik sonuçlar doğurabileceği bir labirente dönüşür. Siklomatik karmaşıklık, bu labirentteki bağımsız yolları sayarak kodun test edilme, anlaşılma ve bakım riskini sayısal biçimde görünür kılar.

``

## Temel fikir: Kaynak koddan grafa

Thomas McCabe tarafından 1976'da tanımlanan siklomatik karmaşıklık, bir program parçasını **kontrol akış grafiği** olarak ele alır. Bu grafikte:

- **Düğümler ($N$):** Komutları veya ardışık komut bloklarını,
- **Kenarlar ($E$):** Kontrolün izleyebileceği geçişleri,
- **Bağlı bileşenler ($P$):** Birbirinden bağımsız akış grafiklerini temsil eder.

Temel formül şöyledir:

$$M = E - N + 2P$$

Tek bir fonksiyon inceleniyorsa çoğunlukla $P=1$ olur ve formül şu hâle gelir:

$$M = E - N + 2$$

Bu sayı, grafikteki **doğrusal olarak bağımsız yürütme yollarının** miktarını verir. Başka bir ifadeyle her yeni karar noktası, kodun izleyebileceği alternatif bir rota açar.

Pratikte tek giriş ve tek çıkışlı yapılarda daha kolay bir yaklaşım kullanılabilir:

$$M = D + 1$$

Buradaki $D$, karar noktalarının sayısıdır. `if`, `while`, `for`, `case` ve dile ya da kullanılan araca göre mantıksal `and`/`or` ifadeleri bu sayıyı artırabilir.

## Küçük bir örnek

Aşağıdaki Python fonksiyonu, sipariş için indirim hesaplıyor:

```python
def indirim_hesapla(tutar, premium, kupon):
    indirim = 0

    if tutar > 1000:
        indirim += 10

    if premium:
        indirim += 5

    if kupon:
        indirim += 15

    return min(indirim, 30)
```

Fonksiyonda üç bağımsız `if` bulunduğu için $D=3$ olur:

$$M = 3 + 1 = 4$$

Bu sonuç, temel yol testi yaklaşımında bütün bağımsız akışları kapsamak için en az dört dikkatle seçilmiş test senaryosuna ihtiyaç duyulduğunu söyler. Ancak tüm olası kombinasyonların sayısı sekize kadar çıkabilir. Dolayısıyla siklomatik karmaşıklık, doğrudan “toplam test sayısı” değil, bağımsız yollar için alt sınır niteliğinde bir göstergedir.

## Değerleri nasıl yorumlamalıyız?

Eşikler ekipten ekibe değişse de yaygın bir yorumlama tablosu şöyledir:

| Karmaşıklık | Genel değerlendirme | Önerilen yaklaşım |
|---:|---|---|
| 1–10 | Düşük risk | Normal inceleme ve birim testleri |
| 11–20 | Orta risk | Fonksiyonu bölmeyi değerlendirin |
| 21–50 | Yüksek risk | Refaktör ve yoğun test uygulayın |
| 50+ | Çok yüksek risk | Tasarımı yeniden ele alın |

`M=4` değerine sahip örneğimiz rahat görünür. Fakat indirim kurallarına ülke, ürün türü, kampanya tarihi ve müşteri seviyesi eklendiğinde fonksiyon hızla “koşul çorbasına” dönüşebilir.

## Karmaşıklığı azaltma yöntemleri

En etkili çözüm, büyük fonksiyonları anlamlı sorumluluklara ayırmaktır. Uzun `if/elif` zincirleri yerine strateji deseni, polimorfizm veya veri odaklı kural tabloları kullanılabilir. İç içe koşulları azaltmak için erken dönüşler de yararlıdır:

```python
def islem_yap(kullanici):
    if kullanici is None:
        return "Kullanıcı bulunamadı"

    if not kullanici.aktif:
        return "Hesap pasif"

    return "İşlem tamamlandı"
```

Erken dönüşler karar sayısını her zaman düşürmese de iç içeliği azaltarak kodun zihinsel yükünü hafifletir. Bu noktada siklomatik karmaşıklığın tek başına yeterli olmadığını unutmamak gerekir.

| Metrik | Neyi ölçer? | Kör noktası |
|---|---|---|
| Siklomatik karmaşıklık | Bağımsız kontrol yollarını | Kodun okunabilirliğini tam ölçmez |
| Bilişsel karmaşıklık | İnsan için anlama zorluğunu | Matematiksel yol sayısını vermez |
| Kod satırı | Fiziksel büyüklüğü | Mantıksal riski açıklamaz |

Sonuç olarak bu metrik bir kalite hükmü değil, duman dedektörüdür. Yüksek değer mutlaka kötü kod anlamına gelmez; fakat daha dikkatli inceleme, güçlü testler ve olası refaktör için oldukça yüksek sesle “Buraya bak!” der.
