---
layout: post
title: "BookStack Üzerinde Rol ve İzin Yönetimi: Güvenli Bir Yetkilendirme Mimarisi"
math: true
categories: 
  - Bilgi
tags: 
  - bookstack
  - yetkilendirme
  - rbac
toc: true
---

BookStack, sınıf notlarından atölye belgelerine kadar pek çok içeriği düzenli biçimde paylaşmayı sağlar. Ancak öğrenci, eğitmen, mentor ve misafirlerin aynı sistemde bulunduğu senaryolarda yalnızca hesap açmak yeterli değildir. Kimin hangi kitabı görebileceği, sayfaları kimin değiştirebileceği ve içerikleri kimin silebileceği önceden tasarlanmalıdır.

``

## Yetkilendirmenin temel mantığı

BookStack erişim modeli iki katmanlı düşünülebilir: **rol tabanlı genel izinler** ve **içeriğe özel izinler**. Genel rol, kullanıcının sistem çapında neler yapabileceğini belirler. İçerik izinleri ise belirli bir raf, kitap, bölüm veya sayfa üzerinde bu davranışı daraltır ya da genişletir.

Bir kullanıcının kaynak üzerindeki etkin iznini basitleştirilmiş biçimde şöyle ifade edebiliriz:

$$P_{etkin}(u, r)=P_{rol}(u) \cap P_{icerik}(u,r)$$

Burada $u$ kullanıcıyı, $r$ erişilmek istenen kaynağı temsil eder. Gerçek değerlendirme; atanmış roller, içerik seviyesindeki geçersiz kılmalar ve üst kaynaklardan devralınan kurallarla birlikte yapılır. Güvenli yaklaşım, varsayılan olarak en az yetkiyi vermektir.

| Katman | Örnek | Kullanım amacı |
|---|---|---|
| Sistem rolü | Öğrenci | Genel görüntüleme ve sınırlı düzenleme |
| Raf | Yazılım Sınıfı | İlgili kitapları mantıksal olarak gruplama |
| Kitap | Python 101 | Belirli bir grubun erişimini yönetme |
| Bölüm | Eğitmen Notları | Kitap içindeki hassas alanı ayırma |
| Sayfa | Cevap Anahtarı | En ayrıntılı erişim kontrolünü uygulama |

## Rol tasarımını sade tutun

Her öğrenci için ayrı rol oluşturmak kısa sürede yönetim kabusuna dönüşür. Bunun yerine görev temelli roller tanımlayın:

- **Yönetici:** Sistem ayarlarını, kullanıcıları ve rolleri yönetir.
- **İçerik yöneticisi:** Kitap oluşturur, taşır ve düzenler; sistem ayarlarına erişmez.
- **Eğitmen:** Kendi eğitim alanındaki içerikleri hazırlar ve yayımlar.
- **Öğrenci:** İzin verilen kitapları görüntüler, gerekiyorsa belirli sayfaları düzenler.
- **Misafir:** Yalnızca herkese açık materyalleri okur.

Örneğin “Öğrenci” rolüne sistem genelinde kitap silme yetkisi vermek yerine yalnızca görüntüleme izni verilebilir. Grup çalışması kitabında içerik izinleri açılarak bu role oluşturma ve düzenleme hakkı tanınabilir. Böylece istisna, tüm platforma yayılmaz.

## Kitap ve sayfa bazlı mimari

Bir kurs için ayrı raf, her ders için ayrı kitap kullanmak anlaşılır bir sınır oluşturur. “Web Geliştirme” rafında ders kitabı, proje belgeleri ve eğitmen rehberi bulunabilir. Öğrenciler ilk iki kitabı görebilirken eğitmen rehberi yalnızca eğitmen rolüne açılır.

Sayfa bazlı izinler güçlüdür fakat çok sayıda istisna üretir. Yüzlerce sayfayı tek tek yönetmek yerine ortak kuralları kitap seviyesinde uygulayın; cevap anahtarı veya değerlendirme formu gibi gerçekten hassas sayfalarda özel izin kullanın.

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Kitap bazlı izin | Kolay denetlenir | Bazı özel sayfalar için yetersiz kalabilir |
| Sayfa bazlı izin | Hassas kontrol sağlar | İzin karmaşası ve unutulmuş istisnalar üretir |
| Kişiye özel izin | Geçici ihtiyaçları çözer | Kullanıcı sayısı arttıkça ölçeklenmez |
| Rol bazlı izin | Tutarlı ve ölçeklenebilir | Kötü tasarlanmış roller fazla yetki verebilir |

## Yapılandırma ve operasyon

Kimlik doğrulamasını LDAP veya OIDC ile merkezileştirmek, kullanıcı yaşam döngüsünü kolaylaştırır. Aşağıdaki Docker Compose kesiti OIDC bağlantısının çevresel değişkenlerle tanımlanmasını gösterir:

```yaml
environment:
  - AUTH_METHOD=oidc
  - OIDC_NAME=Kampus Girisi
  - OIDC_ISSUER=https://kimlik.example.edu
  - OIDC_CLIENT_ID=bookstack
  - OIDC_CLIENT_SECRET=${OIDC_SECRET}
  - OIDC_ISSUER_DISCOVER=true
```

Bu yapı tek oturum açmayı sağlar; fakat BookStack içindeki içerik izinlerinin yerini almaz. Kimlik sağlayıcı “kimsin?” sorusunu, BookStack rolleri ise “ne yapabilirsin?” sorusunu cevaplar.

Son olarak dönem başlarında ve sonlarında izin denetimi yapın. Ayrılan katılımcıları pasifleştirin, geçici rolleri kaldırın ve bir test öğrencisi hesabıyla erişimleri doğrulayın. Yönetici hesabıyla yapılan kontrol yanıltıcı olabilir; çünkü yönetici, sıradan kullanıcının karşılaşacağı kısıtları görmez. İyi mimari, en fazla rolü değil, en az istisnayla anlaşılabilir güvenliği hedefler.
