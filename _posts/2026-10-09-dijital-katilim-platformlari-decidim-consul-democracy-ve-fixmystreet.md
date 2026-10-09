---
layout: post
title: "Dijital Katılım Platformları: Decidim, CONSUL DEMOCRACY ve FixMyStreet"
math: true
categories: 
  - Program
tags: 
  - decidim
  - consul-democracy
  - fixmystreet
  - e-demokrasi
  - açık-kaynak
  - dijital-katılım
toc: true
image: /img/dijital-katilim-platformlari-83.png
---

Bir mahalledeki bozuk kaldırımı bildirmek, belediyeye yeni bir bisiklet yolu önermek veya belirli bir konuda binlerce imza toplamak istiyorsanız sıradan bir formdan fazlasına ihtiyacınız vardır. Decidim, CONSUL DEMOCRACY ve FixMyStreet; vatandaşlarla kurumlar arasında dijital köprü kuran açık kaynaklı platformlardır. Ancak aynı aileden görünseler de farklı problemleri çözerler.

``

## Üç platform, üç yaklaşım

**Decidim**, Barselona çıkışlı kapsamlı bir katılımcı demokrasi altyapısıdır. Teklif oluşturma, destek toplama, toplantı düzenleme, anket, bütçeleme ve sonuç takibi gibi süreçleri modüler biçimde sunar. Bir dilekçe sistemi kurmanın yanında tüm karar alma döngüsünü yönetmek isteyen kurumlara uygundur.

**CONSUL DEMOCRACY**, vatandaş önerileri, tartışmalar, oylamalar ve katılımcı bütçeleme üzerine yoğunlaşır. Teklif belirli bir destek eşiğine ulaştığında değerlendirme ya da oylama aşamasına geçirilebilir. Bu nedenle klasik “öneri ver, imza topla, gündeme taşı” modeliyle oldukça uyumludur.

**FixMyStreet** ise doğrudan bir dilekçe platformu değildir. Vatandaşların harita üzerinde çukur, kırık sokak lambası veya kaçak döküm gibi yerel sorunları bildirmesini sağlar. Bildirim, konuma göre sorumlu kuruma yönlendirilir ve çözüm durumu kamuya açık şekilde izlenebilir.

| Özellik | Decidim | CONSUL DEMOCRACY | FixMyStreet |
|---|---|---|---|
| Temel amaç | Çok yönlü katılım | Öneri ve oylama | Coğrafi sorun bildirimi |
| İmza/destek toplama | Güçlü | Güçlü | Doğal özelliği değil |
| Harita odaklı çalışma | Ek modüllerle | Sınırlı | Çok güçlü |
| Katılımcı bütçe | Var | Var | Yok |
| Uygun ölçek | Kurum ve şehir | Belediye ve ülke | Belediye ve mahalle |

## İmza sistemi nasıl düşünülmeli?

Basit modelde her dilekçenin bir destek sayısı ve hedefi bulunur. İlerleme oranı şöyle hesaplanabilir:

$$P = 100 * S / H$$

Burada $S$ doğrulanmış destek sayısını, $H$ hedeflenen desteği, $P$ ise yüzde ilerlemeyi ifade eder. Örneğin 2.000 destek hedefleyen bir öneri 1.250 doğrulanmış imzaya ulaştığında ilerleme oranı yüzde 62,5 olur.

Fakat yalnızca sayaç tutmak yeterli değildir. Aynı kişinin tekrar imza atması engellenmeli, e-posta veya kimlik doğrulaması yapılmalı ve kişisel veriler gereksiz yere yayımlanmamalıdır. İdeal süreç şu durum makinesini izleyebilir:

`Taslak → Moderasyon → Yayında → Eşik Aşıldı → Kurumsal İnceleme → Sonuçlandı`

Aşağıdaki basitleştirilmiş Python fonksiyonu, doğrulanmış ve benzersiz destekleri sayar:

```python
def petition_progress(signatures, target):
    # Doğrulanmış kullanıcı kimliklerini kümeye alarak tekrarları eler.
    verified_users = {
        item["user_id"]
        for item in signatures
        if item["verified"] is True
    }

    support_count = len(verified_users)
    percentage = min((support_count / target) * 100, 100)

    return {
        "support_count": support_count,
        "percentage": round(percentage, 2),
        "threshold_reached": support_count >= target
    }
```

Gerçek sistemde `user_id` değerleri herkese açık gösterilmemeli; mümkünse tek yönlü özetler, yetkilendirme katmanları ve kayıt saklama politikaları kullanılmalıdır. Ayrıca kötüye kullanım önleme mekanizması erişilebilirliği bozmamalıdır: aşırı CAPTCHA kullanımı gerçek vatandaşları da kaçırabilir.

## Hangisini seçmelisiniz?

| İhtiyaç | Önerilen platform |
|---|---|
| Dilekçe, toplantı ve bütçe tek yerde olsun | Decidim |
| Öneriler destek eşiğiyle oylamaya geçsin | CONSUL DEMOCRACY |
| Sorunlar haritada işaretlenip kuruma gönderilsin | FixMyStreet |

Seçimde yalnızca özellik listesini değil; kurulum ekibinin Ruby/Rails deneyimini, barındırma bütçesini, moderasyon kapasitesini, çok dillilik ihtiyacını ve kurum içi süreçleri de değerlendirmek gerekir. En parlak arayüz bile arka tarafta dilekçeyi yanıtlayacak bir iş akışı yoksa dijital bir öneri kutusuna dönüşür.

Sonuç olarak Decidim geniş kapsamlı bir demokrasi laboratuvarı, CONSUL DEMOCRACY yapılandırılmış bir öneri ve oylama motoru, FixMyStreet ise konum tabanlı belediye sorunları için uzmanlaşmış bir araçtır. Başarılı seçim, “Hangisi daha güçlü?” sorusundan önce “Vatandaş hangi sürece katılacak?” sorusunu yanıtlamakla başlar.

![dijital-katilim-platformlari-83](/img/dijital-katilim-platformlari-83.svg)

