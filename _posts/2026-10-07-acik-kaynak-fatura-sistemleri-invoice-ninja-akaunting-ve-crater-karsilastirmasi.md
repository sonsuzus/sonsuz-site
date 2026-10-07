---
layout: post
title: "Açık Kaynak Fatura Sistemleri: Invoice Ninja, Akaunting ve Crater Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - fatura
  - invoice ninja
  - akaunting
  - crater
  - açık kaynak
  - muhasebe
toc: true
image: /img/acik-kaynak-fatura-68.png
---

![acik-kaynak-fatura-68](/img/acik-kaynak-fatura-68.svg)


Fatura hazırlamak yalnızca birkaç ürünü alt alta yazıp toplamı göstermek değildir. Müşteri kayıtları, vergiler, para birimleri, ödeme durumları ve yasal numaralandırma kuralları işin içine girdiğinde küçük bir tablo hızla mini bir muhasebe sistemine dönüşür. Neyse ki Invoice Ninja, Akaunting ve Crater gibi açık kaynak araçlar bu karmaşayı yönetilebilir hâle getiriyor.

``

## Fatura sisteminin temel mantığı

Bir fatura uygulamasında müşteri, ürün ve ödeme birbirinden bağımsız veriler olarak saklanır. Fatura ise bunları belirli bir tarihte bir araya getiren belgedir. Bu yaklaşım aynı müşteriyi veya ürünü her işlemde yeniden yazmayı önler.

Temel hesaplama şu şekilde ifade edilebilir:

$$
Ara\ Toplam = \sum_{i=1}^{n}(Miktar_i \times Birim\ Fiyat_i)
$$

Vergi ve indirim eklendiğinde ödenecek tutar:

$$
Genel\ Toplam = Ara\ Toplam - İndirim + Vergi
$$

Örneğin 500 TL tutarındaki bir hizmete yüzde 10 indirim ve ardından yüzde 20 vergi uygulanırsa sonuç $500-50+90=540$ TL olur. Burada işlem sırası önemlidir; verginin indirimden önce hesaplanması farklı bir sonuç üretir.

## Üç güçlü aday

| Özellik | Invoice Ninja | Akaunting | Crater |
|---|---|---|---|
| Ana odak | Faturalama ve ödeme | Muhasebe yönetimi | Sade faturalama |
| Teknoloji | Laravel, Flutter | Laravel, Vue.js | Laravel, Vue.js |
| Çoklu şirket | Güçlü | Güçlü | Daha sınırlı |
| Muhasebe özellikleri | Orta | Gelişmiş | Temel |
| Kullanım kolaylığı | Orta | Orta | Yüksek |
| Eklenti yaklaşımı | Entegrasyon ağırlıklı | Uygulama mağazası | Daha yalın |

### Invoice Ninja

Invoice Ninja; teklif oluşturma, yinelenen faturalar, zaman takibi ve çevrim içi ödeme konularında öne çıkar. Serbest çalışanlar ve ajanslar için oldukça uygundur. Müşteriye özel portal sunması sayesinde faturalar görüntülenebilir, indirilebilir ve desteklenen ağ geçitleri üzerinden ödenebilir.

Özellik sayısı fazla olduğundan ilk yapılandırma biraz zaman alabilir. Buna karşılık otomatik hatırlatmalar ve yinelenen faturalar, düzenli hizmet veren işletmelerin ciddi zaman kazanmasını sağlar.

### Akaunting

Akaunting yalnızca fatura kesmek isteyenlerden ziyade gelir, gider, banka hesabı ve nakit akışı takibi yapmak isteyen işletmelere hitap eder. Çift taraflı muhasebe gibi gelişmiş ihtiyaçlar eklentilerle karşılanabilir.

Modüler yapı önemli bir avantajdır; ancak ihtiyaç duyulan bazı özelliklerin ücretli uygulamalar olarak sunulabileceği unutulmamalıdır. “Fatura da keseyim, şirketin finansal durumunu da izleyeyim” diyorsanız güçlü aday budur.

### Crater

Crater modern arayüzü ve sade kurulumu ile dikkat çeker. Fatura, teklif, gider ve ödeme yönetimi gibi temel işlevleri gereksiz kalabalık yaratmadan sunar. Küçük işletmeler veya kendi sunucusunda hafif bir çözüm isteyen geliştiriciler için güzel bir başlangıçtır.

Bununla birlikte proje seçerken güncelleme sıklığını, topluluk etkinliğini ve güvenlik yamalarını kontrol etmek gerekir. Açık kaynak dünyasında iyi görünen bir arayüz kadar sürdürülebilir bakım da değerlidir.

## Basit bir fatura hesabı

Aşağıdaki JavaScript fonksiyonu satır toplamlarını hesaplar, indirimi uygular ve vergi ekler:

```javascript
function calculateInvoice(items, discountRate, taxRate) {
  const subtotal = items.reduce(
    (sum, item) => sum + item.quantity * item.unitPrice,
    0
  );

  const discount = subtotal * discountRate;
  const taxableAmount = subtotal - discount;
  const tax = taxableAmount * taxRate;

  return {
    subtotal,
    discount,
    tax,
    total: taxableAmount + tax
  };
}

const result = calculateInvoice(
  [{ quantity: 2, unitPrice: 750 }],
  0.10,
  0.20
);

console.log(result.total); // 1620
```

Bu kod eğitim amaçlıdır. Gerçek sistemlerde kayan nokta hatalarını önlemek için para tutarları kuruş cinsinden tam sayı olarak veya hassas ondalık kütüphaneleriyle saklanmalıdır.

## Hangisini seçmeli?

Yinelenen faturalar, müşteri portalı ve ödeme entegrasyonları öncelikliyse **Invoice Ninja**; kapsamlı finans takibi isteniyorsa **Akaunting**; hızlı, sade ve geliştirici dostu bir deneyim aranıyorsa **Crater** daha uygundur. Son karardan önce yedekleme, e-posta teslimatı, yerel vergi mevzuatı, Türkçe desteği ve projenin güncelliği mutlaka test edilmelidir.
