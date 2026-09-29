---
layout: post
title: "Tersine Proxy Sızıntıları: Nginx Yanlış Yapılandırmalarının Bedeli"
math: true
categories: 
  - Bilgi
tags: 
  - nginx
  - reverse-proxy
  - siber-güvenlik
  - regex
  - dizin-aşma
  - devops
toc: true
image: /img/tersine-proxy-sizintilari-29.png
---

Tersine proxy, internetten gelen isteklerle uygulama sunucuları arasında duran güvenlik görevlisine benzer. Ancak bu görevliye yanlış talimat verirseniz yalnızca ziyaretçileri yönlendirmekle kalmaz; kaynak kodu, yedek dosyalarını veya yapılandırma sırlarını da servis edebilir. Nginx yapılandırmalarındaki tek bir regex karakteri ya da hatalı `alias` kullanımı, görünmez olması gereken dosyaları halka açık hâle getirebilir.

``

## Tersine proxy nasıl karar verir?

Nginx, gelen URI’yi `location` bloklarıyla eşleştirir. Genel olarak önce kesin eşleşmeler, ardından önek kuralları ve uygun durumlarda regex tabanlı kurallar değerlendirilir. Seçilen blok isteğin dosya sistemine mi, yoksa arka uç uygulamasına mı gönderileceğini belirler.

Örneğin `/api/users` isteği uygulama sunucusuna aktarılırken `/assets/logo.png` doğrudan diskten sunulabilir. Tehlike, URI ile gerçek dosya yolu arasındaki dönüşüm yanlış tanımlandığında başlar.

$$\text{Risk} = \text{Gerçekleşme Olasılığı} \times \text{Etki}$$

Kaynak kodu sızıntısında olasılık küçük görünse bile etki; veritabanı parolaları, API anahtarları ve iş mantığının açığa çıkması nedeniyle son derece yüksektir.

| Yapılandırma öğesi | Görevi | Tipik hata | Muhtemel sonuç |
|---|---|---|---|
| `proxy_pass` | İsteği arka uca iletir | URI son ekini yanlış dönüştürmek | Yetkisiz rotaya erişim |
| `alias` | URI’yi farklı dizine bağlar | Eğik çizgi uyumsuzluğu | Dizin sınırının aşılması |
| `root` | Belge kökünü belirler | Hassas dizini kök yapmak | Kaynak ve yedek dosyalarının sunulması |
| Regex `location` | Desene göre seçim yapar | Noktayı kaçırmamak veya deseni sabitlememek | Beklenmeyen dosyaların eşleşmesi |

![tersine-proxy-sizintilari-29](/img/tersine-proxy-sizintilari-29.svg)


## Bir karakter neden bu kadar önemli?

Regex içinde `.` karakteri “herhangi bir karakter” anlamına gelir. Gerçek bir nokta aranıyorsa `\.` kullanılmalıdır. Ayrıca `$` ile desenin dosya adının sonunda bittiği belirtilmezse `.php` metnini ortasında taşıyan beklenmedik yollar da eşleşebilir.

Aşağıdaki yaklaşım uzantıyı açıkça sınırlar ve dosyanın gerçekten var olup olmadığını denetler:

```nginx
location ~ \.php$ {
    try_files $uri =404;
    include fastcgi_params;
    fastcgi_pass unix:/run/php/php-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
}
```

Buradaki `try_files`, olmayan veya yanlış çözümlenen bir betiğin PHP işleyicisine gönderilmesini engeller. Yine de kullanıcı tarafından yazılabilir yükleme dizinlerinde PHP çalıştırmak ayrıca yasaklanmalıdır.

```nginx
location ^~ /uploads/ {
    location ~ \.php$ { return 403; }
    try_files $uri =404;
}
```

Bu blok, yüklenen bir dosya PHP uzantısı taşısa bile çalıştırılmasını önleyen savunma katmanıdır.

## `alias` ve dizin sınırı problemi

`alias`, özellikle eğik çizgi tutarlılığı gerektirir. Konum `/static/` ile bitiyorsa hedef dizinin de `/` ile bitmesi okunabilirliği ve doğru eşlemeyi güçlendirir:

```nginx
location /static/ {
    alias /srv/app/public/static/;
    autoindex off;
    try_files $uri =404;
}
```

Ancak `alias` ile `try_files` etkileşimi sürüme ve yerleşime göre dikkatle test edilmelidir. En güvenli yaklaşım, yalnızca herkese açık dosyaları ayrı bir dizinde tutmak ve uygulama kaynaklarını bu ağacın dışında bırakmaktır. Web kökü hiçbir zaman proje deposunun tamamı olmamalıdır.

## Sızıntıyı önleyen pratik kontroller

Yedekler, gizli dosyalar ve sürüm kontrol dizinleri açıkça reddedilebilir:

```nginx
location ~ /\. { deny all; }
location ~* \.(bak|old|swp|sql|env)$ { deny all; }
```

Dağıtımdan önce `nginx -t` yalnızca sözdizimini doğrular; güvenlik mantığını doğrulamaz. Bu yüzden staging ortamında beklenen ve reddedilmesi gereken URI’ler otomatik test edilmelidir. Erişim günlüklerinde kod dosyaları, `.env`, `.git` ve yedek uzantılarına yönelik istekler alarm üretmelidir.

Son olarak en az ayrıcalık ilkesini uygulayın: Nginx kullanıcısı kaynak depolarını ve sır dosyalarını okuyamıyorsa yapılandırma hatasının etkisi ciddi biçimde azalır. İyi güvenlik, tek bir kusursuz regex değil; dosya izinleri, izole web kökü, testler ve izleme gibi birbirini tamamlayan katmanlardan oluşur.
