---
layout: post
title: "Dijital Kütüphaneyi Kurmak: BookStack ve Wiki Sistemlerinde Bilgi Hiyerarşisi"
math: true
categories: 
  - Bilgi
tags: 
  - bookstack
  - wiki
  - dokümantasyon
  - bilgi-mimarisi
  - teknik-yazım
  - devops
toc: true
image: /img/dijital-kutuphaneyi-kurmak-59.png
---

![dijital-kutuphaneyi-kurmak-59](/img/dijital-kutuphaneyi-kurmak-59.svg)


Teknik dokümantasyon büyüdükçe bilgi üretmekten daha zor bir problem ortaya çıkar: Üretilen bilgiyi yeniden bulmak. BookStack, bu sorunu gerçek bir kütüphaneden tanıdığımız raf, kitap, bölüm ve sayfa metaforlarıyla çözer. Kullanıcıya soyut bir içerik ağacı göstermek yerine, “Aradığım şey hangi kitapta olurdu?” sorusunu sordurur. Böylece yüzlerce servis, prosedür ve mimari karar arasında kaybolma ihtimali azalır.

``

## BookStack hiyerarşisinin mantığı

BookStack içeriği dört temel seviyede düzenler:

1. **Raf:** Birbiriyle ilişkili kitapları gruplandırır.
2. **Kitap:** Belirli bir ürün, ekip veya konu alanını temsil eder.
3. **Bölüm:** Kitap içindeki büyük konu kümelerini ayırır.
4. **Sayfa:** Asıl bilgiyi barındıran en küçük içerik birimidir.

Örneğin “Yazılım Platformu” rafında “Kimlik Servisi” ve “Ödeme Servisi” kitapları bulunabilir. Ödeme kitabı; “Mimari”, “Operasyon” ve “Sorun Giderme” bölümlerine ayrılabilir. “Başarısız ödeme kuyruğunu temizleme” ise doğrudan uygulanabilir bir sayfa olur.

Bu model, bilgi mimarisindeki **aşamalı açıklama** ilkesini uygular. Kullanıcı önce geniş bir bağlam seçer, ardından ayrıntıya iner. Dengeli bir ağaçta yaklaşık erişim maliyeti şöyle düşünülebilir:

$$L \approx \log_b(N)$$

Burada $N$ içerik sayısını, $b$ her seviyedeki ortalama seçenek sayısını, $L$ ise hedefe ulaşmak için gereken seçim miktarını temsil eder. Çok düşük $b$ derin ve yorucu menüler; çok yüksek $b$ ise seçenek bombardımanı yaratır.

## Sistemler nasıl karşılaştırılır?

| Sistem | Temel organizasyon modeli | Güçlü yanı | Olası zorluk |
|---|---|---|---|
| BookStack | Raf → Kitap → Bölüm → Sayfa | Sezgisel ve kontrollü hiyerarşi | Birden fazla kategoriye uyan içerikler |
| MediaWiki | Sayfa, kategori ve bağlantı ağı | Esnek çapraz bağlantılar | Başlangıçta dağınık görünebilir |
| Confluence | Alan → Sayfa ağacı | Ekip ve kurumsal süreç uyumu | Derin ağaçlarda gezinme güçlüğü |
| DokuWiki | Ad alanı → Sayfa | Hafif yapı ve dosya tabanlı çalışma | Görsel yönetim olanakları daha sınırlı |

BookStack’ın metaforu güçlüdür; ancak gerçek bilgi her zaman tek bir dala ait değildir. Örneğin OAuth yapılandırması hem güvenlik hem de API kitaplarıyla ilişkili olabilir. Bu durumda sayfayı kopyalamak yerine etiketler, çapraz bağlantılar ve merkezi referans sayfaları kullanılmalıdır. Kopyalama, zamanla birbirinden farklı “doğrular” üretir.

## İyi bir hiyerarşi nasıl tasarlanır?

Organizasyonu araç ekranından değil, kullanıcı ihtiyaçlarından başlatın. İçerikleri şu sorularla sınıflandırın:

- Kullanıcı bu sayfayı hangi görevi yaparken arar?
- İçeriğin sahibi hangi ekip veya roldür?
- Sayfa ürün, süreç, kavram ya da acil durum bilgisi midir?
- Aynı bilgi başka bir yerde tekrar ediliyor mu?

Basit bir keşfedilebilirlik puanı da tanımlanabilir:

$$D = 0.35H + 0.25S + 0.20T + 0.20C$$

Burada $H$ hiyerarşik açıklığı, $S$ arama kalitesini, $T$ etiket tutarlılığını ve $C$ çapraz bağlantı yeterliliğini gösterir. Formül bilimsel bir standart değildir; dokümantasyon denetimlerinde ortak değerlendirme dili oluşturur.

Aşağıdaki örnek, bir sayfanın makineler tarafından da sınıflandırılabilecek üst verilerini gösterir:

```yaml
title: Ödeme Kuyruğunu Yeniden İşleme
book: Ödeme Servisi
chapter: Sorun Giderme
tags:
  - ödeme
  - kuyruk
  - operasyon
owner: platform-ekibi
review_period_days: 90
```

Bu alanlar; içerik sahibini belirlemek, süresi dolan sayfaları raporlamak ve arama filtreleri üretmek için kullanılabilir. Özellikle `owner` ve `review_period_days`, wikinizin dijital bir mezarlığa dönüşmesini engeller.

## Hiyerarşi tek başına yeterli değildir

İyi bir wiki hem **ağaç** hem de **ağ** gibi davranmalıdır. Raflar ve kitaplar ana rotayı sunarken bağlantılar alternatif yollar açar. Arama sistemi başlıklara ek olarak etiketleri, eş anlamlıları ve sayfa içeriğini taramalıdır. “Login bozuk” araması yapan biri, başlığı “OIDC Kimlik Doğrulama Hataları” olan sayfaya ulaşabilmelidir.

Son olarak hiyerarşiyi değişmez kabul etmeyin. Arama kayıtları, bulunamayan sorgular ve destek talepleri düzenli incelenmelidir. Kullanıcılar sürekli yanlış kitabı açıyorsa sorun kullanıcıda değil, tabelalardadır. Başarılı bilgi organizasyonu, içeriği yalnızca saklamaz; doğru kişiyi, doğru zamanda, doğru sayfaya götürür.
