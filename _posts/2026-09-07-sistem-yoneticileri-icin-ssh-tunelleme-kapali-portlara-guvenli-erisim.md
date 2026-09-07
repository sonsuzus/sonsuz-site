---
layout: post
title: "Sistem Yöneticileri İçin SSH Tünelleme: Kapalı Portlara Güvenli Erişim"
math: true
categories: 
  - Bilgi
tags: 
  - ssh
  - sistem yönetimi
  - ağ güvenliği
toc: true
---

SSH tünelleme, doğrudan internete açılmaması gereken veritabanı, yönetim paneli ve iç ağ servislerine şifreli bir kanal üzerinden erişmenin pratik yoludur. Buradaki amaç güvenlik politikalarını izinsiz biçimde delmek değil; yetkili olduğunuz sistemlerde, güvenlik duvarının izin verdiği SSH bağlantısını kontrollü bir geçit olarak kullanmaktır. Kısacası SSH, yalnızca uzak terminal değil, aynı zamanda cebinizde taşıdığınız şifreli bir ağ borusudur.

``

## Tünelin Arkasındaki Mantık

Normal bir TCP bağlantısı istemci, hedef adres ve hedef porttan oluşur. SSH tünelinde uygulamanın trafiği önce SSH istemcisine gelir, şifrelenir, SSH sunucusuna taşınır ve oradan gerçek hedefe yönlendirilir.

Bunu basitleştirerek şöyle gösterebiliriz:

$$
C_{uygulama} \rightarrow E_{SSH}(veri) \rightarrow SSH_{sunucu} \rightarrow Hedef
$$

Burada $E_{SSH}$, verinin SSH oturumu içinde şifrelenmesini temsil eder. Dinleme portu genellikle yerel bilgisayarda açıldığından, uygulama uzak servisi `localhost` üzerinde çalışıyormuş gibi görür.

SSH üç temel yönlendirme modeli sunar:

| Yöntem | Parametre | Dinleme noktası | Tipik kullanım |
|---|---|---|---|
| Yerel yönlendirme | `-L` | Yerel bilgisayar | Uzak veritabanına erişmek |
| Uzak yönlendirme | `-R` | SSH sunucusu | Yerel servisi uzaktan erişilebilir yapmak |
| Dinamik yönlendirme | `-D` | Yerel bilgisayar | SOCKS proxy oluşturmak |

## Yerel Port Yönlendirme

Bir iç ağdaki PostgreSQL sunucusunun `db.internal:5432` adresinde bulunduğunu düşünelim. Bu port dış dünyaya kapalı, fakat `admin@gateway.example.com` üzerinden geçiş yetkiniz var:

```bash
ssh -L 15432:db.internal:5432 admin@gateway.example.com
```

Komut, yerel bilgisayardaki `15432` portunu açar. PostgreSQL istemcisini şu şekilde bağlayabilirsiniz:

```bash
psql -h 127.0.0.1 -p 15432 -U uygulama
```

Akış şu hale gelir:

```text
localhost:15432 -> SSH geçidi -> db.internal:5432
```

Tünelin yalnızca yerel makineden kullanılmasını garanti etmek için açıkça loopback adresi belirtmek daha güvenlidir:

```bash
ssh -L 127.0.0.1:15432:db.internal:5432 admin@gateway.example.com
```

## Uzak ve Dinamik Yönlendirme

Uzak yönlendirme, yerel makinenizdeki bir servisi SSH sunucusu tarafında yayımlar. Örneğin yetkili bir destek oturumunda yerel `8080` servisini uzak sunucunun `18080` portuna bağlayabilirsiniz:

```bash
ssh -R 18080:127.0.0.1:8080 admin@gateway.example.com
```

Bu özellik yanlış yapılandırılırsa servisi beklenenden geniş bir ağa açabilir. Sunucudaki `GatewayPorts` ayarı ve dinleme adresi mutlaka incelenmelidir.

Dinamik yönlendirme ise tek hedef yerine SOCKS proxy üretir:

```bash
ssh -D 127.0.0.1:1080 admin@gateway.example.com
```

SOCKS5 destekleyen bir uygulama `127.0.0.1:1080` adresini proxy olarak kullanabilir. DNS sorgularının yerel ağdan sızmaması için uygulamada uzak DNS çözümleme seçeneği tercih edilmelidir.

## Kullanışlı Seçenekler

Yalnızca tünel açıp kabuk çalıştırmamak için `-N`, komutu arka plana almak için `-f` kullanılabilir:

```bash
ssh -fN \
  -o ExitOnForwardFailure=yes \
  -o ServerAliveInterval=30 \
  -L 127.0.0.1:15432:db.internal:5432 \
  admin@gateway.example.com
```

`ExitOnForwardFailure`, port açılamazsa bağlantının sessizce devam etmesini önler. `ServerAliveInterval` ise kopmuş oturumların fark edilmesini kolaylaştırır.

## Güvenlik Kontrol Listesi

- Parola yerine güçlü SSH anahtarları ve mümkünse MFA kullanın.
- Sunucu anahtarını doğrulayın; `StrictHostKeyChecking` denetimini kapatmayın.
- Tünelleri `0.0.0.0` yerine `127.0.0.1` üzerinde dinletin.
- `AllowTcpForwarding`, `PermitOpen` ve kullanıcı bazlı SSH kurallarıyla hedefleri sınırlayın.
- Tünel kullanımını loglayın ve değişiklik yönetimine dahil edin.
- Kurum politikasında izin verilmeyen ağlara tünel açmayın.

SSH tünelleme doğru sınırlarla kullanıldığında kapalı portları açmak yerine erişimi şifreli, kimliği doğrulanmış ve denetlenebilir bir kanalın içine alır. Böylece saldırı yüzeyini büyütmeden yönetim konforu kazanırsınız.
