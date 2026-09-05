---
layout: post
title: "SSDLC: Güvenliği Projenin Sonuna Değil, Temeline Eklemek"
math: true
categories: 
  - Bilgi
tags: 
  - ssdlc
  - siber güvenlik
  - tehdit modelleme
toc: true
---

Bir uygulamayı tamamladıktan sonra güvenlik testi yapmak, evi inşa edip anahtarı teslim ettikten sonra kapısının olmadığını fark etmeye benzer. Güvenli Yazılım Geliştirme Yaşam Döngüsü veya kısaca SSDLC, güvenliği son dakikada eklenen bir kontrol olmaktan çıkarır; planlama, tasarım, geliştirme, test, dağıtım ve bakım aşamalarının tamamına yerleştirir.
``
SSDLC, klasik Yazılım Geliştirme Yaşam Döngüsü'nün güvenlik faaliyetleriyle genişletilmiş hâlidir. Temel yaklaşım **shift left**, yani güvenlik kontrollerini sürecin mümkün olduğunca erken aşamalarına kaydırmaktır. Böylece ekip yalnızca mevcut açıkları yakalamaz, açığa dönüşebilecek tasarım kararlarını da sorgular.

Bir güvenlik kusurunun maliyeti, keşfedildiği aşama ilerledikçe genellikle büyür. Bunu basitleştirilmiş biçimde şöyle düşünebiliriz:

$$C_f = C_0 \times k^n$$

Burada $C_f$ düzeltme maliyetini, $C_0$ erken aşamadaki temel maliyeti, $k$ aşamalar arasındaki maliyet katsayısını ve $n$ kusurun kaç aşama geç keşfedildiğini gösterir. Tasarım sırasında değiştirilecek bir yetkilendirme akışı birkaç saat sürerken, üretimde aynı değişiklik veri taşıma, kesinti ve olay müdahalesi gerektirebilir.

## Geleneksel yaklaşım ve SSDLC

| Konu | Geleneksel SDLC | SSDLC |
|---|---|---|
| Güvenlik zamanı | Test veya yayın öncesi | Planlamadan bakıma kadar |
| Sorumluluk | Güvenlik ekibi | Tüm ürün ekibi |
| Ana yaklaşım | Açığı bul ve kapat | Açığı tasarımda önle |
| Gereksinimler | İşlev odaklı | İşlev ve kötüye kullanım odaklı |
| Üretim sonrası | Tepkisel müdahale | Sürekli izleme ve iyileştirme |

## Aşamalara göre güvenlik faaliyetleri

**Planlama aşamasında** korunacak varlıklar, yasal yükümlülükler ve risk iştahı belirlenir. Örneğin kullanıcı parolası, ödeme bilgisi ve erişim anahtarı aynı hassasiyet seviyesinde değerlendirilmemelidir.

**Tasarım aşamasında** veri akış diyagramları hazırlanır, güven sınırları işaretlenir ve tehdit modellemesi yapılır. Microsoft tarafından yaygınlaştırılan STRIDE modeli yararlı bir kontrol listesidir:

| Tehdit | Anlamı | Örnek savunma |
|---|---|---|
| Spoofing | Kimliğe bürünme | MFA ve güçlü kimlik doğrulama |
| Tampering | Veriyi değiştirme | İmza ve bütünlük kontrolü |
| Repudiation | İşlemi inkâr etme | Değiştirilemez denetim kayıtları |
| Information Disclosure | Bilgi sızdırma | Şifreleme ve maskeleme |
| Denial of Service | Hizmeti aksatma | Hız sınırlama |
| Elevation of Privilege | Yetki yükseltme | En az ayrıcalık ilkesi |

Her tehdit için olasılık ve etki puanlanabilir:

$$Risk = Olasılık \times Etki$$

İki değerin 1 ile 5 arasında olduğu bir sistemde 20 puanlı risk, 4 puanlı riskten önce ele alınır. Ancak sayıların karar desteği olduğu, mutlak gerçek olmadığı unutulmamalıdır.

## Güvenlik gereksinimini koddan önce yazmak

Normal kullanıcı hikâyelerine saldırgan bakış açısıyla hazırlanan kötüye kullanım senaryoları eklenebilir:

```gherkin
Feature: Oturum güvenliği

  Scenario: Tekrarlanan başarısız girişlerin sınırlandırılması
    Given aynı IP adresinden 5 başarısız giriş yapılmışsa
    When yeni bir giriş isteği gönderildiğinde
    Then istek geçici olarak engellenmelidir
    And olay güvenlik günlüğüne kaydedilmelidir
```

Bu senaryo, geliştiriciye yalnızca “giriş ekranı yap” demez; kaba kuvvet saldırısına karşı beklenen davranışı da açıklar. Böylece test ekibi ölçülebilir kabul kriterlerine sahip olur.

**Geliştirme aşamasında** güvenli kodlama standartları, kod incelemesi, bağımlılık taraması ve gizli anahtar kontrolü uygulanır. **Test aşamasında** SAST kaynak kodu, DAST çalışan uygulamayı, SCA ise üçüncü taraf paketleri inceler. Bu kontroller CI/CD hattında otomatikleştirilebilir:

```yaml
security-checks:
  steps:
    - run: dependency-scanner --fail-on=high
    - run: static-analysis ./src
    - run: secret-scan --history
```

Bu örnek, yüksek riskli bağımlılık bulunduğunda derlemeyi durdurur; kaynak kodu ve depo geçmişindeki yanlışlıkla eklenmiş anahtarları tarar.

SSDLC'nin amacı sıfır risk vaadi vermek değildir. Amaç, riskleri erken görünür kılmak, bilinçli kararlar almak ve güvenliği yalnızca “güvenlikçilerin işi” olmaktan çıkarmaktır. En iyi başlangıç; küçük bir tehdit modelleme oturumu, net güvenlik gereksinimleri ve otomatik taramalarla yapılabilir. Güvenli ürünler finalde cilalanmaz, ilk çizgiden itibaren tasarlanır.
