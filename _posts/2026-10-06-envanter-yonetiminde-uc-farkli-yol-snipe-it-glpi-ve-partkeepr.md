---
layout: post
title: "Envanter Yönetiminde Üç Farklı Yol: Snipe-IT, GLPI ve PartKeepr"
math: true
categories: 
  - Program
tags: 
  - envanter yönetimi
  - snipe-it
  - glpi
  - partkeepr
  - açık kaynak
  - it varlık yönetimi
toc: true
image: /img/envanter-yonetiminde-uc-76.png
---

Bir dizüstü bilgisayarın kimde olduğunu, rafta kaç direnç kaldığını veya yazılım lisanslarının ne zaman yenileneceğini hâlâ elektronik tablolarla takip ediyorsanız, envanteriniz küçük çaplı bir polisiye romana dönüşmüş olabilir. Açık kaynak dünyasında öne çıkan Snipe-IT, GLPI ve PartKeepr bu karmaşayı çözer; ancak aynı probleme değil, farklı envanter ihtiyaçlarına odaklanırlar.

``

## Envanter yönetiminin temel mantığı

İyi bir envanter sistemi yalnızca ürün adlarını ve miktarlarını saklamaz. Her varlığın **kimliği**, **konumu**, **durumu**, **sorumlusu** ve **hareket geçmişi** bulunmalıdır. Temel stok dengesi şu formülle gösterilebilir:

$$S_{yeni} = S_{mevcut} + Giriş - Çıkış$$

Örneğin depoda 120 mikrodenetleyici varsa, 30 yenisi geldiyse ve üretimde 45 tanesi kullanıldıysa yeni stok $120+30-45=105$ olur. BT varlıklarında ise sayı kadar yaşam döngüsü önemlidir:

$$Maliyet_{toplam} = SatınAlma + Bakım + Lisans - HurdaDeğeri$$

Bu nedenle doğru araç, yalnızca “kaç tane var?” sorusuna değil, “nerede, kimde ve hangi maliyetle?” sorularına da yanıt vermelidir.

## Üç aracın karşılaştırması

| Özellik | Snipe-IT | GLPI | PartKeepr |
|---|---|---|---|
| Ana kullanım | BT varlıkları | ITSM ve kapsamlı BT yönetimi | Elektronik parça stoğu |
| Tipik kayıtlar | Laptop, telefon, lisans | Bilgisayar, yazıcı, talep, sözleşme | Direnç, sensör, entegre |
| Zimmet takibi | Çok güçlü | Güçlü | Temel stok yaklaşımı |
| Yardım masası | Yok | Yerleşik | Yok |
| Parça parametreleri | Sınırlı | Özelleştirilebilir | Çok güçlü |
| Öğrenme eğrisi | Düşük-orta | Orta-yüksek | Orta |

### Snipe-IT: Zimmet işlerinin pratik uzmanı

Snipe-IT; bilgisayar, telefon, monitör, aksesuar ve lisans gibi kurumsal varlıklara odaklanır. Bir cihazı kullanıcıya teslim edebilir, iade tarihini kaydedebilir, garanti süresini izleyebilir ve QR kod ile fiziksel doğrulama yapabilirsiniz. Arayüzü GLPI’ye göre daha sade olduğundan küçük ve orta ölçekli ekipler için hızlı bir başlangıç sunar.

### GLPI: Envanterin ötesinde bir ITSM merkezi

GLPI, varlık yönetimini yardım masası, sözleşmeler, tedarikçiler, değişiklikler ve bilgi bankasıyla birleştirir. Envanter ajanları ve eklentiler yardımıyla ağdaki cihaz bilgileri otomatik toplanabilir. Buna karşılık kapsamlı yapısı daha fazla kurulum, rol tasarımı ve süreç planlaması gerektirir. “Cihazı kaydedelim” yerine “BT operasyonunu tek merkezden yönetelim” diyen ekipler için daha uygundur.

### PartKeepr: Elektronik laboratuvarının çekmece bekçisi

PartKeepr; üretici kodu, paket tipi, teknik parametre, depo konumu ve proje kullanımı gibi elektronik bileşen ayrıntılarını yönetmek için tasarlanmıştır. Aynı görünümlü iki direncin değer yüzünden tamamen farklı davranabildiği laboratuvarlarda oldukça anlamlıdır. Ancak proje sürümü, topluluk etkinliği ve güvenlik güncellemeleri kurulmadan önce mutlaka incelenmelidir; eski bir uygulamayı internete açık çalıştırmak risklidir.

## Basit bir seçim puanı

Kararı sayısallaştırmak için ağırlıklı puan kullanılabilir:

$$P = 0.4U + 0.35Ö + 0.25B$$

Burada $U$ kullanım uygunluğu, $Ö$ özellik yeterliliği, $B$ ise bakım kolaylığıdır. Her değeri 10 üzerinden puanlayarak adayları karşılaştırabilirsiniz.

Kurulum denemelerini Docker ile izole etmek de pratiktir:

```bash
# Servisleri arka planda başlatır
Docker compose up -d

# Çalışan konteynerlerin durumunu gösterir
docker compose ps
```

Komut adının doğru biçimi küçük harfli `docker` olmalıdır; ilk satır bu nedenle `docker compose up -d` şeklinde uygulanmalıdır. Denemede örnek veri kullanın, yedekleme ve sürüm yükseltme süreçlerini de test edin.

## Hangisini seçmeli?

Temel ihtiyacınız cihaz zimmeti ve lisans takibiyse **Snipe-IT**, yardım masasıyla birleşen kurumsal BT yönetimiyse **GLPI**, elektronik parça ve laboratuvar stoğuysa **PartKeepr** daha mantıklıdır. En iyi araç en fazla özelliğe sahip olan değil, ekibinizin düzenli veri girebildiği ve sürdürülebilir biçimde güncelleyebildiği araçtır.

![envanter-yonetiminde-uc-76](/img/envanter-yonetiminde-uc-76.svg)

