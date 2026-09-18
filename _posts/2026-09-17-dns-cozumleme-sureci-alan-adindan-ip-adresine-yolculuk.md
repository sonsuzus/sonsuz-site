---
layout: post
title: "DNS Çözümleme Süreci: Alan Adından IP Adresine Yolculuk"
math: true
categories: 
  - Bilgi
tags: 
  - dns
  - ağ
  - internet
  - ip adresi
  - domain
  - dnssec
toc: true
image: /img/dns-cozumleme-sureci-93.png
---

![dns-cozumleme-sureci-93](/img/dns-cozumleme-sureci-93.svg)


Tarayıcıya `example.com` yazdığınızda bilgisayarınızın bu ismin hangi sunucuyu temsil ettiğini öğrenmesi gerekir. Çünkü ağ cihazları alan adlarıyla değil, `93.184.216.34` gibi IP adresleriyle iletişim kurar. DNS (Domain Name System), internetin telefon rehberi gibi çalışarak insanların hatırlayabildiği isimleri makinelerin kullandığı adreslere dönüştürür.
``

## DNS neden gereklidir?

Teorik olarak ziyaret ettiğimiz her sitenin IP adresini ezberleyebilirdik. Fakat bir sunucunun adresi değişebilir, aynı alan adı birden fazla sunucuya yönlenebilir ve IPv6 adresleri oldukça uzundur. DNS, isim ile fiziksel ağ konumu arasına bir soyutlama katmanı ekler.

DNS hiyerarşik ve dağıtık bir sistemdir. Tek bir merkezi sunucu yerine kök sunucular, üst seviye alan adı sunucuları ve yetkili sunucular birlikte çalışır. Böylece sistem hem ölçeklenebilir hem de arızalara karşı dayanıklı olur.

| Kavram | Görevi | Örnek |
|---|---|---|
| İstemci | DNS sorgusunu başlatır | Dizüstü bilgisayar |
| Recursive resolver | Cevabı istemci adına araştırır | ISS veya `1.1.1.1` |
| Root sunucusu | Uygun TLD sunucusunu gösterir | Kök DNS ağı |
| TLD sunucusu | Alan adının yetkili sunucusunu bildirir | `.com`, `.org`, `.tr` |
| Yetkili sunucu | Nihai DNS kaydını döndürür | Alan adının DNS sağlayıcısı |

## Çözümleme adım adım nasıl gerçekleşir?

İlk olarak tarayıcı kendi DNS önbelleğine bakar. Kayıt bulunamazsa işletim sisteminin önbelleği ve `hosts` dosyası kontrol edilir. Hâlâ sonuç yoksa sorgu, yapılandırılmış recursive resolver'a gönderilir.

Resolver da önbelleğinde cevap bulamazsa şu yolculuğa çıkar:

1. **Kök DNS sunucusuna** `www.example.com` adresini sorar. Kök sunucu IP'yi bilmez; ancak `.com` TLD sunucularının adreslerini verir.
2. **`.com` TLD sunucusuna** gider. Bu sunucu, `example.com` için yetkili DNS sunucusunu bildirir.
3. **Yetkili DNS sunucusuna** sorgu gönderir. Yetkili sunucu ilgili `A` veya `AAAA` kaydını döndürür.
4. Resolver sonucu önbelleğe alır ve istemciye iletir. Tarayıcı artık hedef IP adresine TCP ya da QUIC bağlantısı kurabilir.

Bir `A` kaydı IPv4, `AAAA` kaydı ise IPv6 adresi taşır. `CNAME` başka bir alan adına takma ad verirken `MX` e-posta sunucularını belirtir.

## Önbellek ve TTL mantığı

Her DNS kaydında saniye cinsinden bir TTL (Time to Live) değeri bulunur. Resolver, kaydı bu süre boyunca yeniden sorgulamadan kullanabilir. Kayıt $t_0$ anında alınmış ve TTL değeri $T$ ise geçerlilik koşulu şöyledir:

$$t_{şimdi} - t_0 < T$$

Örneğin TTL değeri $3600$ olan bir kayıt yaklaşık bir saat saklanır. Yüksek TTL daha az sorgu ve hızlı cevap sağlar; ancak IP değişikliklerinin yayılmasını geciktirir.

| TTL tercihi | Avantaj | Dezavantaj |
|---|---|---|
| Düşük TTL | Değişiklikler hızlı yayılır | Daha fazla DNS sorgusu oluşur |
| Yüksek TTL | Daha iyi önbellek performansı | Eski kayıtlar uzun süre kalabilir |

## Komut satırında DNS'i gözlemlemek

`dig`, DNS yanıtlarını ayrıntılı biçimde incelemek için kullanışlıdır:

```bash
dig example.com A
```

Çıktıdaki `ANSWER SECTION`, döndürülen IP adresini ve TTL değerini gösterir. Tüm hiyerarşik yolculuğu görmek için şu komut kullanılabilir:

```bash
dig +trace example.com
```

Python ile basit bir çözümleme yapmak da mümkündür:

```python
import socket

alan_adi = "example.com"
ip_adresi = socket.gethostbyname(alan_adi)
print(f"{alan_adi} -> {ip_adresi}")
```

Bu kod işletim sisteminin resolver mekanizmasını kullanır; DNS protokolünü sıfırdan uygulamaz.

## Güvenlik tarafı

Klasik DNS yanıtları varsayılan olarak imzalı değildir. Sahte yanıt saldırılarına karşı DNSSEC, kayıtların kriptografik imzalarla doğrulanmasını sağlar. DoH ve DoT ise istemci ile resolver arasındaki DNS trafiğini şifreler. Kısacası tarayıcıdaki birkaç harf, önbelleklerden kök sunuculara uzanan oldukça hareketli bir ağ macerasının başlangıcıdır.
