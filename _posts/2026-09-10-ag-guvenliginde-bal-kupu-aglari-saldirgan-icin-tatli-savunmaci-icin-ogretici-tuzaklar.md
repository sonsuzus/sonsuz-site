---
layout: post
title: "Ağ Güvenliğinde Bal Küpü Ağları: Saldırgan İçin Tatlı, Savunmacı İçin Öğretici Tuzaklar"
math: true
categories: 
  - Proje
tags: 
  - honeypot
  - ağ güvenliği
  - siber güvenlik
toc: true
---

Bir saldırgan ağınıza girdiğinde onu hemen engellemek her zaman en öğretici seçenek değildir. Bazen kontrollü bir ortam hazırlayıp hangi servisleri yokladığını, hangi komutları kullandığını ve nasıl hareket ettiğini izlemek daha değerlidir. Honeypot ağları tam olarak bunu yapar: Gerçek sistemlere benzeyen fakat üretim kaynaklarından kesin biçimde ayrılmış sahte hedeflerle saldırganın dikkatini üzerine çeker.

``

## Honeypot tam olarak nedir?

Honeypot, normal kullanıcıların ziyaret etmesi beklenmeyen bir sunucu, servis veya kimliktir. Bu nedenle honeypot üzerindeki hemen her etkileşim şüpheli kabul edilebilir. Birden fazla honeypot, sahte istemci ve izleme bileşeni birlikte kullanıldığında yapı **honeynet** adını alır.

Temel fikir, saldırgan açısından inandırıcı; savunmacı açısından gözlemlenebilir bir ortam oluşturmaktır. Sahte SSH servisi, taklit edilmiş yönetim paneli, gerçeğe benzeyen dosya adları ve kullanılmayan API uçları bu ortamın parçaları olabilir. Ancak sistem gerçekten savunmasız bırakılmamalı; yalnızca öyle görünmelidir.

| Yaklaşım | Etkileşim düzeyi | Toplanan veri | Risk |
|---|---:|---:|---:|
| Düşük etkileşimli honeypot | Sınırlı servis taklidi | Temel tarama ve parola denemeleri | Düşük |
| Yüksek etkileşimli honeypot | Gerçekçi işletim sistemi | Komutlar ve saldırı zinciri | Yüksek |
| Üretim sunucusu izlemesi | Gerçek kullanıcı trafiği | Geniş fakat gürültülü veri | Çok yüksek |

## Risk ve sinyal mantığı

Honeypot seçimi basit bir risk modeliyle değerlendirilebilir:

$$R = P(E) \times I(E)$$

Burada $P(E)$ honeypot ortamından kaçış olasılığını, $I(E)$ ise kaçışın oluşturacağı etkiyi temsil eder. Yüksek etkileşim daha fazla istihbarat üretse de olasılığı veya etkiyi artırabilir. Bu yüzden amaç en gerçekçi sistemi kurmak değil, kabul edilebilir risk altında yeterli sinyali toplamaktır.

Uyarı kalitesi için de $S = T / (T + F)$ düşünülebilir. $T$ anlamlı olayları, $F$ yanlış pozitifleri gösterir. Normal kullanıcının erişemediği bir bal küpünde $F$ genellikle düşük olduğundan uyarılar değerlidir.

## Güvenli mimari

Sağlam bir honeynet en az dört bölüme ayrılmalıdır:

1. **Tuzak katmanı:** Sahte SSH, HTTP veya veritabanı servisleri.
2. **İzolasyon katmanı:** Ayrı VLAN, güvenlik grubu ya da sanal ağ.
3. **Kayıt katmanı:** Değiştirilemez veya uzaktaki merkezi günlük deposu.
4. **Yönetim katmanı:** Yalnızca güvenilir yönetici ağından erişilen kontrol alanı.

En önemli kural çıkış trafiğini sınırlamaktır. Ele geçirilen honeypot başka sistemlere saldırmak için kullanılamamalıdır. Varsayılan politika çıkışı reddetmeli; yalnızca günlük aktarımı ve zorunlu güncellemeler izin listesine alınmalıdır.

Aşağıdaki Python örneği, yalnızca laboratuvar ortamında bağlantı meta verisi kaydeden basit bir sahte TCP servisi oluşturur:

```python
import socket
from datetime import datetime

HOST, PORT = '0.0.0.0', 2222

with socket.socket() as server:
    server.bind((HOST, PORT))
    server.listen(5)
    while True:
        client, address = server.accept()
        with client:
            event = f'{datetime.utcnow().isoformat()} {address}\n'
            with open('honeypot.log', 'a', encoding='utf-8') as log:
                log.write(event)
            client.sendall(b'SSH-2.0-LabServer\r\n')
```

Kod, 2222 numaralı portu dinler, bağlanan adresi zaman damgasıyla kaydeder ve sahte bir SSH karşılama mesajı gönderir. Kimlik bilgisi toplamamak ve servisi internete doğrudan açmadan önce yasal onay almak önemlidir.

## İzleme ve müdahale

Kaydedilecek veriler arasında kaynak IP, zaman, hedef port, oturum süresi ve gönderilen komutların güvenli özetleri bulunabilir. Parola veya kişisel veri toplamak yerine veri minimizasyonu uygulanmalıdır. SIEM üzerinde aynı kaynaktan hızlı port taraması, tekrarlanan oturumlar veya beklenmeyen protokol kullanımı için kurallar oluşturulabilir.

Son olarak honeypot bir güvenlik duvarının yerine geçmez. O, alarm üreten bir gözlem aracıdır. Düzenli sıfırlama, güncel imajlar, merkezi kayıt, çıkış filtreleme ve belgelenmiş müdahale planı olmadan tatlı görünen bu tuzak, savunmacının başını ağrıtan gerçek bir kovana dönüşebilir.
