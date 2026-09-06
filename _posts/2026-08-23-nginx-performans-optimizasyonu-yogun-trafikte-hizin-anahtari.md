---
layout: post
title: "NGINX Performans Optimizasyonu: Yoğun Trafikte Hızın Anahtarı"
math: true
categories: 
  - Bilgi
tags: 
  - ngınx
  - performans
  - web sunucusu
  - devops
image: /img/nginx-performans-optimizasyonu-67.png
---

Yoğun trafikli bir web uygulamasında sorun çoğu zaman yalnızca sunucu işlemcisinin yetersiz olması değildir. Asıl mesele, her isteğin ne kadar kaynak tükettiği, bağlantıların nasıl yönetildiği ve statik içeriklerin uygulama katmanına uğramadan ne kadar hızlı servis edildiğidir. NGINX; olay güdümlü mimarisi, reverse proxy yetenekleri ve düşük bellek tüketimi sayesinde bu problemlerin çözümünde güçlü bir araçtır.

``

NGINX'in performans avantajını anlamak için bağlantı modeline bakmak gerekir. Geleneksel süreç veya iş parçacığı tabanlı sunucular, çok sayıda eşzamanlı bağlantıda her istemci için ayrı kaynak ayırmaya eğilimlidir. NGINX ise **event loop** yaklaşımıyla binlerce bağlantıyı az sayıda worker süreci üzerinden izler. Basitleştirilmiş yük hesabı şöyle düşünülebilir:

$$\text{Eşzamanlılık} \approx \text{worker\_processes} \times \text{worker\_connections}$$

Örneğin 4 worker ve her worker için 8192 bağlantı tanımlandığında teorik üst sınır $4 \times 8192 = 32768$ bağlantıdır. Ancak bu sayı, işletim sistemi dosya tanımlayıcı limiti, upstream bağlantıları ve uygulamanın yanıt süresi gibi etkenlerle birlikte değerlendirilmelidir.

| Yaklaşım | Kaynak tüketimi | Yoğun trafikte davranış | Uygun kullanım |
|---|---:|---|---|
| Process/thread tabanlı sunucu | Bağlantı başına daha yüksek | Bağlam değiştirme maliyeti artabilir | Düşük-orta trafik |
| NGINX event-driven model | Düşük ve öngörülebilir | Çok sayıda bekleyen bağlantıyı iyi yönetir | API, statik dosya, proxy |
| Uygulama sunucusuna doğrudan erişim | Uygulamayı yorar | Statik istekler bile backend'e gider | Genellikle önerilmez |

![nginx-performans-optimizasyonu-67](/img/nginx-performans-optimizasyonu-67.svg)


İlk optimizasyon, worker ayarlarını gerçek donanıma göre yapılandırmaktır. `worker_processes auto` seçeneği NGINX'in CPU çekirdek sayısını algılamasına izin verir. `worker_connections` artırılırken Linux tarafındaki `ulimit -n` ve systemd `LimitNOFILE` değerleri de yükseltilmelidir; aksi durumda yapılandırma kâğıt üzerinde hızlı, pratikte sınırlı kalır.

```nginx
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 8192;
    use epoll;
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 30;
    keepalive_requests 1000;
}
```

Bu ayarlar Linux'ta `epoll` ile olayları verimli izler. `sendfile`, dosya içeriğini kullanıcı alanına gereksiz kopyalamadan gönderir. `keepalive`, aynı istemcinin tekrar eden isteklerinde TCP el sıkışma maliyetini azaltır. Ancak çok uzun keep-alive süreleri, yavaş istemcilerin bağlantıları gereğinden fazla tutmasına neden olabilir; bu yüzden 30 saniye dengeli bir başlangıç değeridir.

İkinci büyük kazanç statik dosyalar ve önbelleklemeden gelir. CSS, JavaScript, görsel ve font isteklerini uygulama sunucusuna yönlendirmek yerine NGINX doğrudan sunmalıdır. Tarayıcı önbelleği doğru kullanılırsa, tekrar ziyaretlerde ağ maliyeti neredeyse sıfıra yaklaşır.

```nginx
location /assets/ {
    alias /var/www/app/assets/;
    expires 30d;
    add_header Cache-Control "public, immutable";
    access_log off;
}

location /api/ {
    proxy_pass http://backend_pool;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

`immutable` yalnızca dosya adlarında sürüm veya içerik hash'i varsa güvenlidir: `app.a81f2.js` gibi. Dosya adı değişmeden içerik güncellenirse kullanıcılar eski sürümü görmeye devam edebilir. API tarafında ise NGINX reverse proxy olarak çalışır ve istemci IP'sini backend'e iletir.

| Optimizasyon | Kazanç | Dikkat edilmesi gereken |
|---|---|---|
| Gzip/Brotli sıkıştırma | Daha az bant genişliği | CPU maliyeti ve zaten sıkışık dosyalar |
| Statik içerik cache'i | Daha az backend isteği | Cache invalidation stratejisi |
| Upstream keepalive | Backend TCP maliyetini düşürür | Backend bağlantı limitleri |
| Rate limiting | Ani yükte sistemi korur | Meşru trafiği engellememeli |

Son olarak performans ayarları ölçümsüz yapılmamalıdır. `stub_status`, erişim logları, p95/p99 gecikme değerleri ve yük testleri birlikte izlenmelidir. Hedef yalnızca saniyede daha fazla istek işlemek değil; hata oranını artırmadan, kuyrukları büyütmeden ve kullanıcı deneyimini koruyarak sürdürülebilir hız elde etmektir.
