---
layout: post
title: "WireGuard ile Modern VPN Altyapısı: Hız, Sadelik ve Güçlü Kriptografi"
math: true
categories: 
  - Bilgi
tags: 
  - wireguard
  - vpn
  - ağ güvenliği
toc: true
image: /img/wireguard-ile-modern-95.png
---

Modern bir VPN kurmak, eskiden sertifika zincirleri, karmaşık şifre paketleri ve sayfalarca yapılandırma dosyası demekti. WireGuard bu yaklaşımı bilinçli biçimde tersine çevirir: küçük kod tabanı, az sayıda kriptografik tercih ve UDP üzerinde çalışan yalın bir tünel. Sonuç; yönetimi kolay, yüksek performanslı ve özellikle sunucu-istemci ya da site-to-site senaryolarında çok güçlü bir sanal özel ağ altyapısıdır.
``

WireGuard'ın temel fikri, IP paketlerini bir ağ arayüzü üzerinden alıp güvenli biçimde UDP datagramlarına dönüştürmektir. Linux'ta genellikle `wg0` adlı bir sanal arayüz görürsünüz. İstemci bu arayüze gönderdiği paketi şifreler; sunucu paketi doğrular, çözer ve hedef ağa iletir. Tünelin verimliliğini kabaca şu oranla düşünebiliriz:

$$\text{Verim} = \frac{\text{yararlı veri}}{\text{yararlı veri} + \text{tünel ek yükü}}$$

WireGuard, gereksiz protokol katmanlarını azaltarak ek yükü düşük tutmayı hedefler. Ancak gerçek hız; işlemci, MTU, internet hattı, NAT davranışı ve paket kaybı gibi faktörlerden de etkilenir.

## Neden minimal kod tabanı önemlidir?

Güvenlikte her satır kod potansiyel olarak yeni bir hata yüzeyi demektir. WireGuard'ın tasarımı, çok fazla seçenek sunmak yerine güvenli varsayılanlara odaklanır. Bu, “hiç hata olmaz” anlamına gelmez; fakat denetim, bakım ve tehdit modellemesini belirgin biçimde kolaylaştırır.

| Özellik | Geleneksel esnek VPN yaklaşımları | WireGuard yaklaşımı |
|---|---|---|
| Kriptografik seçim | Çok sayıda algoritma ve uyumluluk modu | Sınırlı, modern ve sabit araç seti |
| Yapılandırma | Sertifikalar, profiller, ek protokoller | Anahtarlar ve `AllowedIPs` odaklı yapı |
| Kod ve saldırı yüzeyi | Daha geniş olabilir | Bilinçli olarak küçük tutulur |
| Bağlantı modeli | Çoğu zaman oturum merkezli | Anahtar-temelli eş eşleme |

WireGuard; anahtar değişimi için Curve25519, simetrik şifreleme için ChaCha20-Poly1305 ve karma işlevleri için BLAKE2s gibi güncel bileşenlerden yararlanır. Bu tercihler, yapılandırmada eski ya da zayıf bir şifre takımının yanlışlıkla seçilmesi riskini azaltır. Gizlilik açısından kritik fikir şudur: Şifreli kanalın güvenliği yalnızca anahtar algoritmasına değil, anahtarların gizliliğine de bağlıdır.

$$K_{public} = f(K_{private})$$

Açık anahtar paylaşılabilir; özel anahtar ise asla paylaşılmamalı, sürüm kontrol sistemine eklenmemeli ve mümkünse dosya izinleriyle korunmalıdır.

## Temel sunucu yapılandırması

Aşağıdaki örnek, `10.8.0.0/24` tünel ağı kullanan basit bir sunucu arayüzünü gösterir. Özel anahtar yer tutucusunu gerçek anahtarınızla değiştirmelisiniz.

```ini
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.8.0.1/24
ListenPort = 51820
PrivateKey = SUNUCU_OZEL_ANAHTARI

[Peer]
PublicKey = ISTEMCI_ACIK_ANAHTARI
AllowedIPs = 10.8.0.2/32
```

Buradaki `AllowedIPs` yalnızca bir erişim listesi değildir; WireGuard için hangi hedef IP'nin hangi eşe yönlendirileceğini de belirtir. Bu nedenle aynı IP aralığını birden fazla eşe tanımlamak yönlendirme karmaşasına yol açabilir. Arayüz, Linux üzerinde `wg-quick up wg0` komutuyla başlatılabilir.

İstemci tarafında ise `Endpoint`, sunucunun erişilebilir adresini belirtir. `PersistentKeepalive = 25`, NAT arkasındaki mobil veya ev bağlantılarında eşlemenin canlı kalmasına yardımcı olur.

```ini
[Interface]
Address = 10.8.0.2/32
PrivateKey = ISTEMCI_OZEL_ANAHTARI

[Peer]
PublicKey = SUNUCU_ACIK_ANAHTARI
Endpoint = vpn.ornekalanadi.com:51820
AllowedIPs = 10.8.0.0/24
PersistentKeepalive = 25
```

## Güvenli ve sürdürülebilir tasarım

Tam tünel ile bölünmüş tünel seçimi, performans kadar gizlilik kararidir. `AllowedIPs = 0.0.0.0/0, ::/0` tüm trafiği VPN'e gönderirken, yalnızca kurum ağı gibi belirli bir prefix tanımlamak bölünmüş tünel oluşturur.

| Model | Avantaj | Dikkat edilmesi gereken |
|---|---|---|
| Tam tünel | Ortak ağlarda daha bütüncül koruma | Sunucu bant genişliği ve DNS sızıntıları |
| Bölünmüş tünel | Daha düşük gecikme, az sunucu yükü | Yerel internet trafiği VPN dışındadır |

Son olarak, UDP portunu güvenlik duvarında sınırlayın, her cihaz için ayrı anahtar üretin, kullanılmayan eşleri silin ve düzenli güncelleme uygulayın. WireGuard'ın sadeliği güçlü bir başlangıçtır; gerçek güvenlik ise doğru yönlendirme, sağlam anahtar yönetimi ve dikkatli operasyonla tamamlanır.

![wireguard-ile-modern-95](/img/wireguard-ile-modern-95.svg)

