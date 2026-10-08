---
layout: post
title: "Uptime Takip Sistemi Kurmak: Uptime Kuma, Statping-ng ve Gatus Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - uptime
  - monitoring
  - devops
  - uptime-kuma
  - statping-ng
  - gatus
toc: true
image: /img/uptime-takip-sistemi-98.png
---

Bir web sitesinin çalışıyor görünmesi, gerçekten sağlıklı olduğu anlamına gelmez. Ana sayfa açılırken ödeme API’si hata veriyor, DNS yanıtları gecikiyor veya TLS sertifikası sessizce sona yaklaşıyor olabilir. Uptime takip sistemleri; servisleri düzenli aralıklarla kontrol eder, sonuçları kaydeder ve sorun oluştuğunda ekibe bildirim gönderir. Bu yazıda popüler üç açık kaynak seçeneği, Uptime Kuma, Statping-ng ve Gatus üzerinden kendi gözetleme kulenizi kuracağız.


![uptime-takip-sistemi-98](/img/uptime-takip-sistemi-98.svg)

``

## Uptime ölçümü nasıl çalışır?

Bir monitör, hedef servise belirli aralıklarla istek gönderir. HTTP kontrolünde durum kodu, yanıt süresi ve içerik doğrulanabilir. TCP kontrolü portun erişilebilirliğini, ICMP kontrolü ise sunucunun ağa yanıt verip vermediğini ölçer.

Belirli bir dönemde uptime oranı şu şekilde hesaplanır:

$$
Uptime\,(\%) = \frac{Toplam\ Süre - Kesinti\ Süresi}{Toplam\ Süre} \times 100
$$

Örneğin 30 günlük bir ayda 43 dakika kesinti yaşayan servisin erişilebilirliği yaklaşık $99{,}9\%$ olur. Kontrol aralığı da önemlidir: Beş dakikada bir yapılan kontrol, iki dakikalık kesintiyi hiç yakalamayabilir. Kısa aralıklar daha hassastır ancak daha fazla ağ trafiği ve kayıt üretir.

Sistemin yanlış alarm vermemesi için genellikle art arda birkaç başarısız kontrol beklenir. Üç denemeden sonra alarm üretmek, geçici paket kayıplarının gece yarısı telefonunuzu çaldırmasını önler.

## Üç aracın kısa karşılaştırması

| Özellik | Uptime Kuma | Statping-ng | Gatus |
|---|---|---|---|
| Yapılandırma | Web arayüzü | Web arayüzü ve API | YAML dosyası |
| Kullanım kolaylığı | Çok yüksek | Yüksek | Orta |
| Git ile yönetim | Sınırlı | Sınırlı | Çok güçlü |
| Durum sayfası | Var | Var | Var |
| İdeal kullanıcı | Küçük ve orta ekip | Durum sayfası isteyen ekip | DevOps ve GitOps ekipleri |

**Uptime Kuma**, şık paneli ve kolay kurulumu sayesinde hızlı başlangıç şampiyonudur. HTTP, TCP, DNS, ping ve Docker container kontrollerini destekler. Telegram, Slack, Discord ve e-posta gibi pek çok bildirim kanalı sunar.

**Statping-ng**, servis takibiyle herkese açık durum sayfasını bir arada isteyenler için uygundur. Kullanıcılar planlı bakımları ve geçmiş olayları görebilir. Ancak proje sürümünü seçerken güncel bakım durumunu ve açık sorunları incelemek akıllıca olur.

**Gatus**, arayüzde tıklamak yerine yapılandırmayı kod olarak saklar. Pull request ile kontrol eklemek, değişiklik geçmişini görmek ve aynı ayarı farklı ortamlara taşımak isteyen ekiplerin gözdesidir.

## Uptime Kuma kurulumu

Docker ile birkaç dakikada çalışan bir sistem oluşturabiliriz:

```yaml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    volumes:
      - ./kuma-data:/app/data
    ports:
      - "3001:3001"
    restart: unless-stopped
```

Bu dosya verileri `kuma-data` dizininde kalıcı tutar ve paneli 3001 numaralı porttan yayımlar. `docker compose up -d` komutundan sonra paneli açıp yönetici hesabı oluşturabilir, ardından “Add New Monitor” üzerinden hedeflerinizi ekleyebilirsiniz. İnternete açarken ters proxy, HTTPS ve güçlü kimlik doğrulama kullanmayı unutmayın.

## Gatus ile yapılandırma tabanlı takip

Aşağıdaki örnek, API’nin hem başarılı durum kodu döndürmesini hem de 500 milisaniyeden hızlı yanıt vermesini bekler:

```yaml
endpoints:
  - name: production-api
    group: backend
    url: "https://api.example.com/health"
    interval: 30s
    conditions:
      - "[STATUS] == 200"
      - "[RESPONSE_TIME] < 500"
```

Bu yaklaşımda sağlık şartları açıkça belgelenir. Dosyayı Git deposuna koyarak yapılan her eşik değişikliğini inceleyebilirsiniz. Gatus ayrıca yanıt gövdesi, sertifika süresi ve DNS gibi kontrolleri de koşullara bağlayabilir.

## Hangisini seçmelisiniz?

Ev laboratuvarı, kişisel projeler veya hızlı kurulum için **Uptime Kuma** en pratik seçimdir. Markalı ve ziyaretçilere yönelik bir durum sayfası öncelikliyse **Statping-ng** değerlendirilebilir. Altyapınız GitOps mantığıyla yönetiliyor ve kontrollerin kod incelemesinden geçmesini istiyorsanız **Gatus** daha doğal hissettirir.

Hangi aracı seçerseniz seçin, takip sistemini izlediği sunucudan farklı bir makinede çalıştırın. Aksi hâlde sunucu çöktüğünde hem uygulama hem de alarm mekanizması ortadan kaybolur; dijital bekçi de bina ile birlikte uykuya dalar!
