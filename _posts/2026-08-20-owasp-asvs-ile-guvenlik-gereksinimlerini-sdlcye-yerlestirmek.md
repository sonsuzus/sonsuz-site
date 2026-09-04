---
layout: post
title: "OWASP ASVS ile Güvenlik Gereksinimlerini SDLC'ye Yerleştirmek"
math: true
categories: 
  - Bilgi
tags: 
  - owasp asvs
  - uygulama güvenliği
  - sdlc
toc: true
image: /img/owasp-asvs-ile-81.png
---

![owasp-asvs-ile-81](/img/owasp-asvs-ile-81.svg)


Uygulama güvenliği, yayın öncesi yapılan tek seferlik bir sızma testi değildir; gereksinimden üretime kadar sürdürülen ölçülebilir bir mühendislik disiplinidir. OWASP Application Security Verification Standard (ASVS), bu disiplini somutlaştırmak için kimlik doğrulama, oturum yönetimi, erişim kontrolü, kriptografi ve hata yönetimi gibi alanlarda doğrulanabilir güvenlik gereksinimleri sunar. Böylece ekipler “güvenli olmalı” gibi muğlak cümleleri test edilebilir kabul kriterlerine dönüştürür.
``

ASVS'nin temel değeri, güvenliği geliştiricinin sezgisine veya son dakika denetimine bırakmamasıdır. Her kontrol, uygulamanın hangi davranışı sergilemesi gerektiğini tarif eder. Örneğin yalnızca “parolaları koru” demek yerine, parolaların uygun maliyet parametreleriyle güçlü bir parola türetme fonksiyonu kullanılarak saklanması istenir. Bu yaklaşımda kalite denklemi kabaca şöyle düşünülebilir:

$$Risk \approx Olasılık \times Etki$$

ASVS kontrolleri olasılığı düşürmek için önleyici mekanizmalar, etkiyi azaltmak için de yetkilendirme, kayıt ve güvenli hata yönetimi sağlar. Elbette bu matematiksel bir kesinlik değil; risk önceliklendirmesi için ortak bir zihinsel modeldir.

## Doğrulama seviyesini seçmek

ASVS, her uygulamanın aynı savunma katmanına ihtiyaç duymadığını kabul eder. Bu nedenle kontrolleri üç doğrulama seviyesinde ele alır. Seçim; iş etkisi, işlenen verinin hassasiyeti, saldırı yüzeyi ve düzenleyici yükümlülüklere göre yapılmalıdır.

| Seviye | Uygun senaryo | Amaç |
|---|---|---|
| L1 | Düşük riskli, herkese açık uygulamalar | Yaygın güvenlik açıklarına karşı temel savunma |
| L2 | Giriş yapan kullanıcılar ve kurumsal veriler | Standart iş uygulamaları için güçlü güvence |
| L3 | Finans, sağlık, kritik altyapı | Yüksek değerli varlıklar için derinlemesine koruma |

L1'i bir başlangıç çizgisi, L2'yi çoğu ürün ekibi için hedef, L3'ü ise yüksek tehdit modeline sahip sistemler için sıkı bir sözleşme gibi düşünebilirsiniz. En pahalı kontrol listesini körlemesine seçmek yerine, tehdit modellemesiyle gerekçelendirilmiş bir seviye belirlemek daha doğrudur.

## Gereksinimden pipeline'a uzanan yol

En verimli entegrasyon, ASVS maddelerini kullanıcı hikâyelerinin kabul kriterlerine bağlamaktır. Örneğin “Kullanıcı e-posta adresini değiştirebilir” hikâyesine yeniden kimlik doğrulama, oran sınırlama, denetim kaydı ve e-posta doğrulama kontrolleri eklenebilir. Böylece güvenlik işi görünmez bir “sonra bakarız” maddesi olmaktan çıkar.

| SDLC aşaması | ASVS'nin rolü | Somut çıktı |
|---|---|---|
| Planlama | Seviye ve kapsam seçimi | Güvenlik gereksinimleri listesi |
| Tasarım | Tehdit modeline kontrol eşleme | Veri akış diyagramı, karar kayıtları |
| Geliştirme | Güvenli kodlama kontrolleri | Kod inceleme kontrol listesi |
| CI/CD | Otomatik kanıt toplama | SAST, bağımlılık ve secret tarama sonuçları |
| Yayın sonrası | Kontrolün çalıştığını izleme | Alarm, log ve yeniden doğrulama raporu |

Bazı ASVS maddeleri otomasyona çok uygundur; örneğin bağımlılıklardaki bilinen zafiyetleri veya depoya yanlışlıkla eklenen anahtarları taramak. Ancak erişim kontrolü gibi bağlama bağlı konular, otomatik testin yanında insan incelemesi gerektirir. Güzel haber: otomasyon insanı gereksiz kopyala-yapıştır işinden kurtarır; kötü haber: otomasyon yetki modelinizin niyetini telepatik biçimde okuyamaz.

Aşağıdaki örnek, CI sürecinde basit bir güvenlik kapısı oluşturur. Gerçek projelerde eşikler, hata yönetimi ve raporlama daha ayrıntılı tasarlanmalıdır.

```yaml
security-checks:
  stage: test
  script:
    - npm ci
    - npm audit --audit-level=high
    - npx semgrep --config=auto src/
    - gitleaks detect --source . --no-banner
```

Bu adımlar sırasıyla bağımlılık risklerini, kaynak koddaki şüpheli kalıpları ve yanlışlıkla sızdırılmış gizli bilgileri arar. Pipeline başarısız olduğunda ekip, bulguyu üretimden önce ele alır; yani hata düzeltme maliyetinin en düşük olduğu noktada.

## Ölç, kanıtla, iyileştir

ASVS uyumluluğunu “evet/hayır” tablosu olarak değil, yaşayan bir güvenlik backlog'u olarak yönetin. Her kontrol için sorumlu kişi, kanıt bağlantısı, geçerlilik tarihi ve istisna gerekçesi kaydedin. Basit bir ilerleme göstergesi şöyle hesaplanabilir:

$$Kapsam\ Oranı = \frac{Doğrulanan\ Kontrol\ Sayısı}{Uygulanabilir\ Kontrol\ Sayısı} \times 100$$

Bu oran tek başına güvenliği kanıtlamaz; kritik kontrollerin ağırlığını, açıkların yaşını ve istisnaların süresini de takip etmek gerekir. Yine de ekipler arasında ortak dil oluşturur. Sonuçta ASVS, güvenliği bir denetim günü paniği olmaktan çıkarır: tasarlanmış, test edilmiş ve sürekli geliştirilen bir ürün özelliğine dönüştürür.
