---
layout: post
title: "Nginx Reverse Proxy: Trafiği Doğru Servise Yönlendirme Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - nginx
  - reverse proxy
  - devops
toc: true
---

Modern bir web uygulaması çoğu zaman tek bir sunucudan ibaret değildir: arayüz, API, kimlik doğrulama ve dosya servisleri farklı süreçlerde hatta farklı makinelerde çalışabilir. Nginx reverse proxy, istemcinin tek bir alan adına yaptığı isteği uygun arka uç (backend) servisine ileterek bu karmaşıklığı görünmez kılar. Tarayıcı `example.com/api/users` adresini görür; Nginx ise isteği örneğin `localhost:3000` üzerindeki API uygulamasına taşır.

``

## Reverse proxy mantığı

Proxy, iki taraf arasındaki aracı katmandır. **Forward proxy** istemci adına dış dünyaya istek gönderirken, **reverse proxy** sunucu tarafında konumlanır ve istemcinin hangi uygulamayla konuşacağını belirler. Temel akış şöyledir:

$$İstemci \rightarrow Nginx \rightarrow Uygulama\ Servisi \rightarrow Nginx \rightarrow İstemci$$

Nginx, URL yolu, alan adı, HTTP metodu veya header bilgilerine göre yönlendirme kuralı seçebilir. Böylece frontend için `/`, API için `/api/`, medya için `/uploads/` gibi düzenli bir kapı oluşturulur. Ayrıca TLS sertifikasını Nginx'te sonlandırmak, uygulamaların yalnızca yerel ağdaki HTTP trafiğiyle ilgilenmesini sağlar.

| Özellik | Doğrudan backend erişimi | Nginx reverse proxy |
|---|---|---|
| Dışarı açılan portlar | Her servis için ayrı port | Genellikle yalnızca 80/443 |
| TLS yönetimi | Her serviste ayrı ayar | Merkezi sertifika yönetimi |
| URL yönlendirme | Uygulama içinde | Nginx `location` kurallarıyla |
| Ölçekleme | İstemciyi değiştirmek gerekebilir | Upstream havuzuna yeni sunucu eklenir |

## Temel yapılandırma

Aşağıdaki örnekte React benzeri statik arayüz `/` altında, Node.js API ise `/api/` altında yayınlanır. `proxy_pass` hedef servisi tanımlar; `proxy_set_header` satırları ise backend'in gerçek istemci ve protokol bilgisini görmesini sağlar.

```nginx
server {
    listen 80;
    server_name example.com;

    root /var/www/frontend;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:3000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Buradaki en eğlenceli, ama hata üretmeye en yatkın ayrıntı sondaki `/` işaretidir. `location /api/` ile birlikte `proxy_pass http://127.0.0.1:3000/;` kullanıldığında Nginx, `/api/` önekini kaldırır. Yani `/api/users`, backend'e `/users` olarak gider. Eğer backend rotaları gerçekten `/api/users` bekliyorsa, `proxy_pass http://127.0.0.1:3000;` biçiminde sondaki eğik çizgiyi kaldırmak gerekir.

| İstek | `proxy_pass ...:3000/` sonucu | `proxy_pass ...:3000` sonucu |
|---|---|---|
| `/api/users` | `/users` | `/api/users` |
| `/api/health` | `/health` | `/api/health` |

## Birden fazla backend ve yük dağıtımı

Trafik büyüdüğünde tek API süreci dar boğaz olabilir. `upstream` bloğu, Nginx'e bir servis havuzu tanımlar. Varsayılan yaklaşım round-robin'dir; yaklaşık olarak her sunucunun aldığı yük $L_i$ kapasitesi eşitse $L_i \approx L/n$ olur.

```nginx
upstream api_cluster {
    server 10.0.0.11:3000;
    server 10.0.0.12:3000;
    server 10.0.0.13:3000;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://api_cluster;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Canlı ortamda `proxy_connect_timeout`, `proxy_read_timeout` ve hata sayfaları gibi ayrıntıları da belirlemek önemlidir. WebSocket kullanılıyorsa ayrıca `Upgrade` ve `Connection` header'ları iletilmelidir. Son olarak her değişiklikten önce `nginx -t` ile sözdizimini doğrulayın, ardından `nginx -s reload` ile kesintisiz yapılandırma yenilemesi yapın. Doğru tasarlanmış reverse proxy, uygulamalarınızın kapısındaki sakin ama son derece yetenekli trafik polisidir.
