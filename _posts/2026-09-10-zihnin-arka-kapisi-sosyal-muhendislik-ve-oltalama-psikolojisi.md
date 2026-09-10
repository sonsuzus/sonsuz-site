---
layout: post
title: "Zihnin Arka Kapısı: Sosyal Mühendislik ve Oltalama Psikolojisi"
math: true
categories: 
  - Bilgi
tags: 
  - siber güvenlik
  - phishing
  - sosyal mühendislik
toc: true
---

Bir sistem en güncel yamalarla korunabilir, parolalar karmaşık olabilir ve ağ trafiği sürekli izlenebilir. Buna rağmen tek bir çalışan, “Hesabınız 10 dakika içinde kapatılacak” mesajına tıklayarak bütün savunma hattını aşabilir. Sosyal mühendislik tam olarak bu çelişkiden yararlanır: Saldırgan, yazılımdaki teknik bir açığı değil; insan zihninin hızlı karar vermek için kullandığı kestirmeleri hedefler. Oltalama yani phishing, yalnızca sahte bağlantı göndermek değil, kurbanın düşünme biçimini yönlendiren planlı bir psikolojik manipülasyondur.
``

## İnsan neden oltaya gelir?

Beyin, her kararı uzun uzun analiz edemez. Günlük hayatta enerji kazanmak için sezgisel ve hızlı çalışan zihinsel mekanizmalara başvurur. Bu mekanizmalar çoğu zaman faydalıdır; ancak bağlam saldırgan tarafından üretildiğinde güvenlik açığına dönüşebilir.

Oltalama mesajlarında özellikle üç tetikleyici öne çıkar:

- **Aciliyet:** “Şimdi doğrulamazsanız erişiminiz kapanacak.” Düşünmek için ayrılan süre yapay biçimde daraltılır.
- **Korku:** Hesap kaybı, para cezası veya veri sızıntısı gibi sonuçlar öne çıkarılır.
- **Otorite:** Mesajın yönetici, banka, devlet kurumu ya da BT ekibinden geldiği izlenimi oluşturulur.
- **Merak ve ödül:** Beklenmeyen bir dosya, hediye veya maaş artışı vaadiyle tıklama isteği uyandırılır.

Bu etkileri basitleştirilmiş bir risk modeliyle gösterebiliriz:

$$P(Tıklama) = \sigma(\alpha A + \beta K + \gamma O - \delta F)$$

Burada $A$ aciliyet, $K$ korku, $O$ otorite etkisi, $F$ ise farkındalık düzeyidir. $\sigma$ sonucu 0 ile 1 arasına taşıyan lojistik fonksiyondur. Model bilimsel bir teşhis aracı değildir; farkındalık arttıkça dürtüsel tıklama olasılığının neden azaldığını anlatan kavramsal bir çerçevedir.

## Meşru mesaj ile oltalama arasındaki fark

| İncelenen unsur | Meşru iletişim | Şüpheli oltalama |
|---|---|---|
| Zaman baskısı | Makul süre ve açıklama sunar | Dakikalar içinde işlem ister |
| Kimlik doğrulama | Resmî uygulamaya yönlendirir | Mesaj içindeki bağlantıyı dayatır |
| Dil | Tutarlı ve bağlama uygundur | Tehditkâr, aşırı heyecanlı veya beklenmediktir |
| Talep | Normal iş akışıyla uyumludur | Parola, kod ya da ödeme ister |
| Alan adı | Kurumun bilinen alan adıdır | Benzer harflerle taklit edilmiştir |

Tek bir belirti kesin kanıt sayılmaz. Örneğin yazım hatası bulunmayan bir ileti de kötü niyetli olabilir. Bu nedenle karar, işaretlerin toplamına ve mesajın bağlamına göre verilmelidir.

## Küçük bir savunma aracı

Aşağıdaki Python örneği, bir URL’de sık rastlanan şüpheli özellikleri puanlar. Bu kod antivirüs değildir; kullanıcıya bağlantıyı açmadan önce durup incelemesi gerektiğini hatırlatan öğretici bir kontroldür.

```python
from urllib.parse import urlparse
import ipaddress


def url_risk_score(url):
    parsed = urlparse(url)
    host = parsed.hostname or ""
    score, reasons = 0, []

    if parsed.scheme != "https":
        score += 1
        reasons.append("HTTPS kullanılmıyor")

    try:
        ipaddress.ip_address(host)
        score += 2
        reasons.append("Alan adı yerine IP adresi var")
    except ValueError:
        pass

    if host.count(".") >= 4:
        score += 1
        reasons.append("Çok fazla alt alan adı var")

    if "@" in url or len(url) > 120:
        score += 1
        reasons.append("URL yapısı olağan dışı")

    return score, reasons
```

Araç yalnızca sezgisel işaretler üretir; kısa veya HTTPS kullanan bir adres de zararlı olabilir. Güvenli yaklaşım, bağlantıya basmak yerine kurumun adresini tarayıcıya elle yazmak veya resmî uygulamayı açmaktır.

## Zihinsel güvenlik duvarı

Etkili savunma, çalışanlara “dikkatli olun” demekten fazlasını gerektirir. Kurumlar çok faktörlü kimlik doğrulama kullanmalı, ödeme ve parola sıfırlama taleplerini ikinci kanaldan doğrulamalı, şüpheli mesaj bildirimini kolaylaştırmalı ve yalnızca izinli eğitim simülasyonları yapmalıdır.

Bireysel düzeyde ise **dur, doğrula, sonra hareket et** kuralı güçlüdür. Mesaj aciliyet yaratıyorsa kısa bir mola verin; göndereni bağımsız bir kanaldan doğrulayın; alan adını harf harf kontrol edin ve doğrulama kodunu kimseyle paylaşmayın. Çünkü sosyal mühendisliğin asıl panzehiri kusursuz hafıza değil, baskı anında otomatikleşmiş güvenli davranıştır.
