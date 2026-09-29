---
layout: post
title: "Sıfır Güven Mimarisi: Ağdaki Herkese Yabancı Muamelesi Yapmak"
math: true
categories: 
  - Bilgi
tags: 
  - sıfır güven
  - zero trust
  - siber güvenlik
  - ağ güvenliği
  - kimlik doğrulama
  - yetkilendirme
toc: true
image: /img/sifir-guven-mimarisi-77.png
---

![sifir-guven-mimarisi-77](/img/sifir-guven-mimarisi-77.svg)


Şirket ağının içindeyseniz güvenilir, dışındaysanız şüphelisiniz… Geleneksel güvenlik yaklaşımı uzun süre bu kadar basit çalıştı. Ancak bulut servisleri, uzaktan çalışma, mobil cihazlar ve ele geçirilmiş kullanıcı hesapları kale duvarlarını anlamsızlaştırdı. Sıfır Güven, herkesi kötü ilan etmek yerine hiçbir isteğe konumundan dolayı ayrıcalık tanımayan modern bir güvenlik felsefesidir.

``

## Kale ve hendek modeli neden eskidi?

Eski modelde kurum ağı bir kaleye benzer: Güvenlik duvarı hendeği, VPN ise kontrollü giriş kapısını temsil eder. Kullanıcı kapıdan geçtiğinde içeride rahatça dolaşabilir. Ne yazık ki saldırgan da çalınmış bir hesapla içeri girdiğinde aynı rahatlığa kavuşur.

Sıfır Güven yaklaşımının özeti **“Asla güvenme, daima doğrula”** ifadesidir. Buradaki doğrulama yalnızca oturum açarken parola sormak değildir. Kullanıcının kimliği, cihazın durumu, erişilen kaynak, konum, saat ve davranış örüntüsü her istekte değerlendirilir.

| Özellik | Geleneksel model | Sıfır Güven modeli |
|---|---|---|
| Güven kaynağı | Ağ konumu | Kimlik ve bağlam |
| Doğrulama | Oturum başlangıcında | Sürekli ve dinamik |
| Yetki | Geniş ağ erişimi | En az ayrıcalık |
| İhlal varsayımı | Dış tehdit öncelikli | Saldırgan içeride olabilir |
| Ağ yapısı | Büyük güvenli bölge | Mikro segmentler |

## Güven ikili bir değer değildir

Bir isteği yalnızca “izin ver” veya “reddet” şeklinde düşünmeden önce risk puanı hesaplanabilir. Basitleştirilmiş bir model şöyle olsun:

$$Risk = 0.35I + 0.30D + 0.20L + 0.15B$$

Burada $I$ kimlik riskini, $D$ cihaz riskini, $L$ konum riskini ve $B$ davranış anomalisini temsil eder. Değerler 0 ile 100 arasındaysa yüksek sonuç daha tehlikeli bir isteği gösterir. Risk düşükken erişim verilebilir; orta düzeyde ek doğrulama istenebilir; yüksek düzeyde istek engellenebilir.

Bu formül evrensel değildir. Asıl fikir, güvenin bir kez kazanılan kalıcı rozet değil, sürekli güncellenen bağlamsal bir karar olmasıdır.

## Temel yapı taşları

Sıfır Güven uygulamasında birkaç bileşen birlikte çalışır:

- **Güçlü kimlik:** Çok faktörlü kimlik doğrulama ve mümkünse parola yerine geçiş anahtarları kullanılır.
- **En az ayrıcalık:** Kullanıcıya yalnızca görevi için gereken kaynak ve süre kadar yetki verilir.
- **Cihaz sağlığı:** Güncelleme durumu, disk şifreleme ve güvenlik yazılımı kontrol edilir.
- **Mikro segmentasyon:** Ağ küçük bölgelere ayrılır; bir sunucunun ele geçirilmesi diğerlerine serbest geçiş sağlamaz.
- **Gözlemlenebilirlik:** Erişimler kaydedilir, anormal davranışlar analiz edilir ve karar mekanizmasına geri beslenir.

## Bir politika nasıl görünür?

Aşağıdaki Rego örneği, kurumsal bir API için basitleştirilmiş erişim kararı üretir:

```rego
package access

default allow := false

allow if {
    input.user.authenticated == true
    input.user.mfa == true
    input.device.compliant == true
    input.request.risk_score < 40
    input.resource.department == input.user.department
}
```

Bu politika, kullanıcının oturum açmış olmasını tek başına yeterli görmez. MFA tamamlanmalı, cihaz güvenlik kurallarına uymalı, risk puanı 40’ın altında kalmalı ve kullanıcının departmanı kaynakla eşleşmelidir. Gerçek sistemlerde saat, veri hassasiyeti ve geçici yetki gibi ek koşullar da bulunur.

## Her istekte parola mı sorulacak?

Hayır. Sürekli doğrulama, kullanıcıyı sürekli açılır pencerelerle bezdirmek anlamına gelmez. Geçerli cihaz sertifikaları, kısa ömürlü erişim belirteçleri ve davranış analizi arka planda çalışabilir. Yalnızca risk yükseldiğinde ek doğrulama devreye girer. Böylece güvenlik ile kullanıcı deneyimi arasında dengeli bir ilişki kurulur.

Sıfır Güven tek seferde satın alınan bir ürün değil; kimlik, ağ, cihaz ve uygulama politikalarını dönüştüren aşamalı bir yolculuktur. Önce kritik varlıkları belirlemek, erişim akışlarını ölçmek ve geniş yetkileri daraltmak gerekir. Sonuçta amaç herkesten korkmak değil, güveni varsaymak yerine kanıtlamaktır.
