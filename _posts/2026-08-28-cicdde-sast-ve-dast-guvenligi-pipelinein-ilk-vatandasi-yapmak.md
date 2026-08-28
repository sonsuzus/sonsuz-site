---
layout: post
title: "CI/CD’de SAST ve DAST: Güvenliği Pipeline’ın İlk Vatandaşı Yapmak"
math: true
categories: 
  - Bilgi
tags: 
  - CI/CD
  - SAST
  - DAST
---

Modern yazılım ekipleri için hız tek başına başarı ölçütü değildir: Güvenli olmayan bir özelliği dakikalar içinde canlıya almak, sadece hatayı daha hızlı yaymaktır. Bu nedenle CI/CD pipeline’ına güvenlik taramalarını eklemek, güvenliği sürüm sonundaki bir denetim kapısı olmaktan çıkarıp geliştirme yaşam döngüsünün doğal parçası hâline getirir. SAST ve DAST araçları bu yaklaşımın iki güçlü, fakat farklı bakış açısına sahip oyuncusudur.

``

## Neden erken tarama kritik?

Bir açığın çözüm maliyeti, yazılım yaşam döngüsünde geç fark edildikçe büyür. Tasarım aşamasında düzeltilen basit bir yetkilendirme kusuru yalnızca birkaç satırlık değişiklik gerektirebilir; üretimde fark edilirse olay müdahalesi, müşteri iletişimi, log incelemesi ve acil sürüm süreçlerine dönüşebilir. Bunu kavramsal olarak şöyle ifade edebiliriz:

$$Maliyet \approx Temel\_Maliyet \times k^{Aşama}$$

Buradaki $k > 1$, hatanın sonraki aşamalarda bulunmasının çarpan etkisini temsil eder. Amaç kusursuz bir tarama sonucu değil, geliştiriciye **hızlı, bağlamlı ve aksiyon alınabilir** geri bildirim vermektir.

## SAST ve DAST aynı işi mi yapar?

Hayır. SAST (Static Application Security Testing), kaynak kodu veya derlenmiş çıktıyı uygulama çalışmadan analiz eder. SQL sorgularında kullanıcı girdisinin doğrudan kullanılması, zayıf kriptografi, hard-coded parola ve tehlikeli API çağrıları gibi kod seviyesindeki riskleri yakalamada başarılıdır.

DAST (Dynamic Application Security Testing) ise çalışan uygulamayı dışarıdan bir saldırgan gibi test eder. HTTP istekleri gönderir, yanıtları gözlemler ve örneğin XSS, yanlış güvenlik başlıkları, oturum yönetimi problemleri ya da erişim denetimi zafiyetleri arar. SAST kaynak koda bakarken, DAST uygulamanın çalışma anındaki davranışına bakar.

| Özellik | SAST | DAST |
|---|---|---|
| Analiz zamanı | Build veya pull request aşaması | Test/staging ortamı hazır olduğunda |
| Bakış açısı | İçeriden: kod ve veri akışı | Dışarıdan: çalışan uygulama |
| Güçlü olduğu alan | Kod kusurları, gizli anahtarlar | Çalışma zamanı ve HTTP zafiyetleri |
| Temel sınırlama | Çalışma ortamı yapılandırmasını göremeyebilir | Kodun hangi satırının sorunlu olduğunu her zaman söyleyemez |

## Pipeline’a doğru yerde yerleştirme

Etkili entegrasyon, her taramayı her adımda körü körüne çalıştırmak değildir. Pull request aşamasında hızlı SAST kuralları çalıştırılabilir. Ana dala birleşme sonrasında daha kapsamlı analiz, bağımlılık taraması ve secret scanning devreye alınabilir. Staging dağıtımından sonra DAST başlatmak mantıklıdır; çünkü araç, API uçlarını ve kullanıcı akışlarını gerçekçi biçimde sınar.

Aşağıdaki GitHub Actions örneği, SAST için Semgrep ve staging ortamı için OWASP ZAP tabanlı bir akışı özetler:

```yaml
name: security-pipeline
on: [pull_request, push]

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: semgrep/semgrep-action@v1
        with:
          config: p/owasp-top-ten

  dast:
    needs: sast
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: ZAP baseline scan
        uses: zaproxy/action-baseline@v0.12.0
        with:
          target: 'https://staging.ornek-uygulama.com'
```

Bu yapıdaki `sast` işi, değişikliklerin kod güvenliği kurallarını ihlal edip etmediğini erkenden kontrol eder. `dast` işi ise yalnızca ana dal için çalışarak geçici inceleme ortamlarını gereksiz yükten korur. Gerçek projelerde staging URL’si, kimlik bilgileri ve rapor çıktıları secret yönetimi üzerinden güvenli biçimde verilmelidir.

## Eşikler, yanlış pozitifler ve ekip kültürü

Tarama sonucu bulunan her uyarıda pipeline’ı kırmak ilk gün için iyi bir fikir olmayabilir. Özellikle eski projelerde yüzlerce teknik borç uyarısı geliştiricilerin aracı görmezden gelmesine neden olur. Bunun yerine kritik ve yüksek şiddetli yeni bulguları bloklayan; orta ve düşük seviyeleri raporlayan kademeli bir politika uygulanmalıdır.

| Bulgu seviyesi | Önerilen CI/CD davranışı |
|---|---|
| Kritik | Build başarısız, güvenlik incelemesi zorunlu |
| Yüksek | PR engellenir veya onaylı istisna gerekir |
| Orta | Ticket oluşturulur, SLA ile izlenir |
| Düşük | Raporlanır, periyodik iyileştirmeye alınır |

Sonuç olarak SAST ve DAST birbirinin alternatifi değil, savunma katmanlarıdır. Güvenlik taramasını geliştiricinin geri bildirim döngüsüne ne kadar yaklaştırırsanız, açıklar üretime o kadar az yaklaşır. En iyi pipeline, yalnızca kodu derleyen değil; güvenli davranmayı ekip için varsayılan hâle getirendir.
