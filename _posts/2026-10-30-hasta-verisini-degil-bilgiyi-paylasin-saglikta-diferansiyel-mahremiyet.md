---
layout: post
title: "Hasta Verisini Değil, Bilgiyi Paylaşın: Sağlıkta Diferansiyel Mahremiyet"
math: true
categories: 
  - Bilgi
tags: 
  - sağlık verileri
  - mahremiyet
  - differential privacy
  - veri güvenliği
  - python
  - istatistik
toc: true
image: /img/hasta-verisini-degil-39.png
---

Bir hastanenin diyabet eğilimlerini araştırdığını düşünün. Araştırmacılar toplumdaki riskleri görmek istiyor; kimsenin komşusunun teşhisini öğrenmesini değil! Peki, hasta kayıtlarından yararlı sonuçlar çıkarırken kişileri nasıl koruyabiliriz? İsimleri silmek iyi bir başlangıçtır, fakat gerçek mahremiyet daha fazlasını gerektirir. Diferansiyel mahremiyet, tam da bu noktada matematiği güvenlik görevlisine dönüştürür.

``

## İsim silmek neden yetmez?

Bir kayıttan ad, telefon ve kimlik numarasını kaldırmak, o kaydı otomatik olarak anonim yapmaz. Yaş, posta kodu ve hastaneye başvuru tarihi gibi **dolaylı tanımlayıcılar**, başka kaynaklarla eşleştirildiğinde kişiyi yeniden ortaya çıkarabilir. Nadir hastalıklar bu riski özellikle artırır.

Örneğin, küçük bir ilçede yaşayan 97 yaşındaki tek kişinin kayıtlarında isim bulunmasa bile kimliği tahmin edilebilir. Dolayısıyla takma kimlik kullanmak ile anonimlik aynı şey değildir. Takma kimlikli kayıtlar, bağlantı anahtarı veya yardımcı bilgiler üzerinden kişilere bağlanabilir.

| Teknik | Temel yaklaşım | Önemli sınır |
|---|---|---|
| Maskeleme | Doğrudan tanımlayıcıları kaldırır | Dolaylı eşleştirmeyi engellemez |
| k-anonimlik | Belirli özelliklerde kayıtları benzeştirir | Hassas özellikler yine çıkarılabilir |
| Diferansiyel mahremiyet | Çıktılara kontrollü rastgelelik ekler | Doğruluk ve bütçe yönetimi gerektirir |

## Diferansiyel mahremiyetin matematiksel fikri

Diferansiyel mahremiyet, genellikle satırları anonimleştirmekten ziyade **yayımlanan istatistikleri veya model çıktılarını** korur. Amaç, tek bir hastanın araştırmaya katılıp katılmamasının sonuçları fazla değiştirmemesidir.

Bir hastanın eklenmesi veya çıkarılmasıyla farklılaşan iki veri kümesine $D$ ve $D'$ diyelim. Rastgeleleştirilmiş mekanizma $M$, herhangi bir çıktı kümesi $S$ için şu koşulu sağlamalıdır:

$$P(M(D)\in S)\le e^{\varepsilon}P(M(D')\in S)+\delta$$

Burada $\varepsilon$ mahremiyet kaybını kontrol eder: küçük değer daha güçlü koruma, genellikle daha fazla gürültü demektir. $\delta$ ise eşitsizliğe eklenen küçük bir olasılık payıdır; doğrudan yeniden kimliklendirme ihtimali olarak okunmamalıdır. Laplace mekanizması uygun koşullarda $\delta=0$ sağlar.

Önemli ayrıntı: Koruma birimi **hasta** olmalıdır. Aynı hastanın yirmi muayenesini bağımsız kişiler gibi sayarsanız, kayıt düzeyindeki güvence hasta düzeyindeki güvenceye dönüşmez.

## Gürültü rastgele, miktarı hesaplı

Bir sorgunun duyarlılığı $\Delta f$, tek hastanın değişmesiyle sonucun değişebileceği en büyük miktardır. Her hasta sayıma en fazla bir katkı yapıyorsa, ekleme/çıkarma komşuluğunda sayımın duyarlılığı $1$ olur.

Laplace mekanizması şu çıktıyı üretir:

$$\widetilde{f}(D)=f(D)+\operatorname{Laplace}(0,\Delta f/\varepsilon)$$

$\varepsilon=0.5$ için gürültü ölçeği $2$, $\varepsilon=0.1$ için $10$ olur. Yani mahremiyet düğmesini çevirdikçe istatistik biraz daha bulanıklaşır. Bu, gelişigüzel veri bozmak değil; etkisi hesaplanan bir tasarım tercihidir.

## Python ile korumalı hasta sayımı

Aşağıdaki eğitim örneğinde her Boolean değer, farklı bir hastanın hipertansiyon durumunu temsil eder. Gerçek sistemde tekrarlanan ziyaretler önce hasta düzeyinde birleştirilmelidir. Kod yalnızca gürültülü toplamı döndürür; gerçek toplam yayımlanmaz.

```python
import numpy as np


def ozel_sayim(hasta_bayraklari, epsilon=0.5):
    if not np.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("Epsilon pozitif ve sonlu olmalı.")
    if not all(type(x) is bool for x in hasta_bayraklari):
        raise ValueError("Her hasta için bir Boolean gerekli.")

    gercek_toplam = sum(hasta_bayraklari)
    duyarlilik = 1.0
    rng = np.random.default_rng()
    gurultu = rng.laplace(0.0, duyarlilik / epsilon)
    return max(0, int(round(gercek_toplam + gurultu)))


# Tamamen sentetik: 1.000 hasta, 240 pozitif durum.
ornek = [True] * 240 + [False] * 760
print(ozel_sayim(ornek))
```

Negatif sonuçları sıfıra çekmek ve yuvarlamak, yalnızca korumalı çıktıya uygulanan **son işlemedir**; ek mahremiyet kaybı yaratmaz. Ancak sonucu yanlılaştırabilir. NumPy örneği üretim garantisi değildir: güvenli rastgelelik, kayan nokta davranışı ve mekanizma doğruluğu için OpenDP gibi denetlenmiş araçlar değerlendirilmelidir.

## Mahremiyet bütçesi sınırsız değildir

Aynı hastalar üzerinde tekrar tekrar sorgu yayımlamak bilgi biriktirir. Temel bileşim kuralında toplam bütçe $\varepsilon_{toplam}\le\sum_i\varepsilon_i$ şeklinde izlenebilir. Sonuçları tekrar üreterek ortalamasını almak, gürültüyü azaltırken mahremiyet maliyetini artırır.

Bu nedenle sorgu onayı, bütçe kaydı ve erişim denetimi birlikte tasarlanmalıdır. Ortalama gibi sorgularda katkı sınırları ayrıca belirlenmelidir; sınırsız ölçüm değerleri uygun duyarlılık hesabını bozar. Küçük hasta gruplarında gürültünün göreli etkisi büyüdüğünden, klinik yorumlar belirsizlikle sunulmalıdır.

Diferansiyel mahremiyet, ham veriyi şifrelemenin veya KVKK yükümlülüklerinin yerine geçmez. Sağlam yaklaşım; veri minimizasyonu, güvenli saklama ve kontrollü yayımlamayı birleştirir. Böylece araştırma ilerlerken hastanın mahremiyeti, sonradan eklenen bir aksesuar değil, sistemin temel tasarım ilkesi olur.

![hasta-verisini-degil-39](/img/hasta-verisini-degil-39.svg)

