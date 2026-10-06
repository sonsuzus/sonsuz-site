---
layout: post
title: "Personel Yönetiminde Açık Kaynak Üçlüsü: OrangeHRM, Sentrifugo ve ERPNext HR"
math: true
categories: 
  - Program
tags: 
  - insan kaynakları
  - orangehrm
  - sentrifugo
  - erpnext
  - açık kaynak
  - personel yönetimi
toc: true
image: /img/personel-yonetiminde-acik-89.png
---

Personel izinlerini hâlâ elektronik tablolarla takip ediyor, performans değerlendirmelerini e-postalarda arıyor ve özlük bilgileri için klasörler arasında mekik dokuyorsanız dijital dönüşüm zili çalıyor demektir. OrangeHRM, Sentrifugo ve ERPNext HR; insan kaynakları süreçlerini merkezileştiren üç güçlü açık kaynak seçenektir. Ancak aynı probleme yaklaşsalar da kapsamları, kullanım biçimleri ve hedefledikleri kurum profilleri farklıdır.
``

## Personel yönetim sistemi ne yapar?

Bir personel yönetim sistemi, çalışanın kuruma girişinden ayrılışına kadar oluşan verileri tek noktada toplar. Temel hedef yalnızca kayıt tutmak değil; izin, devamlılık, işe alım, performans ve raporlama süreçlerini ölçülebilir hâle getirmektir.

Sistemin sağladığı operasyonel kazancı basitçe şöyle modelleyebiliriz:

$$
K = (T_m - T_s) \times N - M
$$

Burada $T_m$ manuel işlem süresini, $T_s$ sistem kullanıldığındaki süreyi, $N$ aylık işlem sayısını ve $M$ bakım maliyetini gösterir. Sonuç pozitif ve yüksekse yazılım gerçek bir zaman tasarrufu sağlıyor demektir. Elbette çalışanların sistemi benimsememesi durumunda en güzel denklem bile kahve molasında kaybolabilir!

## Üç sistemin karakteri

| Özellik | OrangeHRM | Sentrifugo | ERPNext HR |
|---|---|---|---|
| Temel yaklaşım | Uzmanlaşmış İK yönetimi | Modüler ve sade İK portalı | ERP ile bütünleşik İK |
| Kurulum kolaylığı | Orta | Görece kolay | Orta-zor |
| İşe alım | Güçlü | Mevcut | Güçlü |
| Performans yönetimi | Güçlü | Güçlü | Esnek |
| Bordro ve muhasebe ilişkisi | Sürüme göre sınırlı | Sınırlı | Çok güçlü |
| Uygun kurum | Küçük ve orta ölçekli | Küçük ekipler | Büyüyen ve bütünleşme isteyen işletmeler |

### OrangeHRM

OrangeHRM, yalnızca insan kaynaklarına odaklanan olgun bir platformdur. Çalışan profilleri, izinler, zaman takibi, aday yönetimi ve performans değerlendirmesi gibi klasik ihtiyaçları dengeli biçimde karşılar. Topluluk sürümü temel kullanım için yeterli olabilir; gelişmiş özelliklerin bir bölümü ticari paketlerde bulunur.

Arayüzünün anlaşılır olması eğitim yükünü azaltır. Buna karşılık muhasebe, stok veya satış süreçleriyle derin bağlantı isteyen işletmeler ek entegrasyon geliştirmek zorunda kalabilir.

### Sentrifugo

Sentrifugo; izin, performans, çalışan bilgileri, disiplin kayıtları ve öz değerlendirme gibi modülleriyle daha hafif bir seçenektir. Küçük ekipler için hızlı başlangıç sunar ve gereksiz kurumsal karmaşadan kaçınır.

Ancak proje hareketliliği, güncelleme sıklığı ve topluluk desteği kurulumdan önce dikkatle incelenmelidir. Açık kaynakta yalnızca özellik listesine değil, son sürüm tarihine ve güvenlik güncellemelerine de bakmak gerekir.

### ERPNext HR

ERPNext HR, insan kaynaklarını muhasebe, proje, satış ve varlık yönetimiyle aynı veri modeli içinde çalıştırır. Bir çalışanın masraf talebi muhasebeye, çalışma çizelgesi projeye ve bordro kaydı finansal raporlara bağlanabilir. Bu bütünlük büyük avantajdır; fakat yalnızca izin takibi isteyen bir ekip için kapsamı fazla gelebilir.

## Puanlama ile seçim yapmak

Kararı kişisel beğeniden çıkarmak için ağırlıklı puanlama kullanılabilir:

$$
P = \sum_{i=1}^{n} w_i s_i
$$

Aşağıdaki Python kodu, kriter ağırlıklarıyla ürün puanlarını çarpar ve seçenekleri sıralar:

```python
weights = {
    "ik_ozellikleri": 0.35,
    "entegrasyon": 0.30,
    "kolaylik": 0.20,
    "topluluk": 0.15
}

products = {
    "OrangeHRM": [9, 6, 8, 8],
    "Sentrifugo": [7, 5, 8, 5],
    "ERPNext HR": [8, 10, 6, 9]
}

for name, scores in products.items():
    total = sum(weight * score for weight, score in zip(weights.values(), scores))
    print(name, round(total, 2))
```

Kod, her ürün için karşılaştırılabilir tek bir sonuç üretir. Ağırlıkları kurumunuzun önceliklerine göre değiştirmelisiniz; örneğin entegrasyon kritikse ERPNext doğal olarak öne çıkacaktır.

## Son karar

Sade ve uzmanlaşmış bir İK deneyimi için **OrangeHRM**, küçük ölçekli ve temel ihtiyaçlar için **Sentrifugo**, şirket genelinde bütünleşik bir yönetim altyapısı için **ERPNext HR** daha uygundur. Canlıya geçmeden önce deneme kurulumu yapmak, gerçek kullanıcılarla izin ve işe alım senaryolarını test etmek, yedekleme planını belirlemek ve kişisel verilerin korunmasına yönelik erişim rollerini yapılandırmak şarttır. En iyi sistem, en uzun özellik listesine sahip olan değil; ekibin gerçekten kullandığı sistemdir.

![personel-yonetiminde-acik-89](/img/personel-yonetiminde-acik-89.svg)

