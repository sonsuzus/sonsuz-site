---
layout: post
title: "Kod Gözden Geçirme Kültürü: Kalite Kontrolünden Ortak Öğrenmeye"
math: true
categories: 
  - Bilgi
tags: 
  - kod gözden geçirme
  - yazılım kalitesi
  - ekip kültürü
  - pull request
  - clean code
---

Kod gözden geçirme (code review), bir geliştiricinin yazdığı değişikliklerin başka ekip üyeleri tarafından incelenmesidir. Ancak bunu yalnızca “hata avı” olarak görmek büyük resmi kaçırmaktır. İyi kurulmuş bir inceleme kültürü; üretim hatalarını azaltır, mimari kararları görünür kılar, ekipteki bilgi adalarını yıkar ve herkesin daha tutarlı kod yazmasını sağlar. Kısacası pull request, kodun kapısını çalan bir denetçi değil; ekibin birlikte düşünme alanıdır.

``

Kod kalitesini basitçe birden fazla unsurun bileşimi olarak düşünebiliriz:

$$Q = C + M + T + S$$

Burada $Q$ genel kaliteyi, $C$ doğruluğu (correctness), $M$ bakım yapılabilirliği (maintainability), $T$ test edilebilirliği ve $S$ güvenliği temsil eder. Kod gözden geçirme bu bileşenlerin tamamına dokunur. Otomatik testler bir fonksiyonun beklenen sonucu ürettiğini kanıtlayabilir; fakat değişken adının anlaşılır olup olmadığını, modül sınırlarının doğru çizilip çizilmediğini veya çözümün gelecekte büyümeye uygunluğunu genellikle insan değerlendirmesi ortaya çıkarır.

## İnceleme Neyi Yakalar?

Bir inceleyicinin amacı, her satırı yeniden yazmak değildir. Amaç; değişikliğin niyetini anlamak, riskleri belirlemek ve mümkün olan en küçük maliyetle iyileştirme yapmaktır. Özellikle şu sorular değerlidir:

- Bu değişiklik hangi kullanıcı problemini çözüyor?
- Kenar durumlar ve hata senaryoları ele alınmış mı?
- Mevcut mimariyle uyumlu mu?
- Testler davranışı mı doğruluyor, yoksa yalnızca implementasyona mı bağlı?
- Güvenlik, performans ve geriye dönük uyumluluk açısından bir risk var mı?

| Yaklaşım | Sonuç | Ekip Etkisi |
|---|---|---|
| “Bu satır yanlış.” | Savunmacı tartışma doğurabilir. | Öğrenme sınırlı kalır. |
| “Boş değer geldiğinde ne olmasını bekliyoruz?” | Niyeti ve kenar durumları açığa çıkarır. | Ortak problem çözme gelişir. |
| “Bunu şöyle yaz.” | Hızlıdır ama bağlam vermez. | Bağımlılık yaratabilir. |
| “Bu yaklaşımın performans maliyetini birlikte değerlendirelim.” | Karar gerekçesini görünür kılar. | Teknik muhakeme güçlenir. |

## Yorum Yazmak da Bir Mühendislik Becerisidir

Yapıcı geri bildirim, kişiyle değil kodla ilgilenir. “Sen bunu yanlış yapmışsın” yerine “Bu sorgu her istek için çalışıyor; veri büyüdüğünde önbellekleme düşünmeli miyiz?” demek, hem sorunu tanımlar hem de çözüm için alan bırakır. Yorumları önem derecesine göre ayırmak da süreci rahatlatır: `blocker` üretime çıkışı engeller, `suggestion` iyileştirme önerir, `nitpick` ise zorunlu olmayan biçimsel bir nottur.

Örneğin aşağıdaki kod ilk bakışta çalışır görünür, fakat boş sipariş listesinde hata üretir:

```python
def calculate_average_order(orders):
    total = sum(order.amount for order in orders)
    return total / len(orders)
```

İnceleme yorumu yalnızca “sıfıra bölme hatası var” olmamalıdır. Daha öğretici bir yaklaşım şudur: “Boş sipariş listesi iş kuralında geçerli mi? Geçerliyse ortalama için `0`, `None` veya istisna seçeneklerinden hangisi API sözleşmemizle uyumlu?” Ardından karar netleştiğinde kod güvenli hâle getirilebilir:

```python
def calculate_average_order(orders):
    if not orders:
        return None

    total = sum(order.amount for order in orders)
    return total / len(orders)
```

Buradaki kritik nokta `None` döndürmek değil, davranışın bilinçli biçimde seçilmesi ve test edilmesidir.

## Sağlıklı Bir Süreç Nasıl Kurulur?

Etkili incelemeler küçük pull request'lerle başlar. Binlerce satırlık değişiklikte inceleyici ayrıntıları kaçırır; yazar da geri bildirimleri uygulamakta zorlanır. İdeal olarak PR açıklaması problem bağlamını, çözüm yaklaşımını, test adımlarını ve özellikle dikkat edilmesi gereken noktaları içerir. Biçimsel kontrolleri ise insanlara bırakmak yerine linter, formatter ve CI araçlarına devretmek gerekir.

| Pratik | Neden Önemli? |
|---|---|
| Küçük ve odaklı PR | İnceleme yükünü ve hata olasılığını azaltır. |
| Açık PR açıklaması | İnceleyicinin niyeti hızlı kavramasını sağlar. |
| Otomatik kalite kontrolleri | İnsan yorumlarını mimari ve mantık konularına yöneltir. |
| Dönüşümlü inceleyici atama | Bilginin tek kişide toplanmasını önler. |

Sonuç olarak kod gözden geçirme, merge düğmesine basmadan önceki zorunlu bir bariyer değildir. Doğru dil, küçük değişiklikler ve net standartlarla uygulandığında ekibin kolektif hafızasına yapılan düzenli bir yatırımdır. İyi bir inceleme sonunda yalnızca kod değil, onu yazan ve okuyan geliştiriciler de biraz daha iyi hâle gelir.
