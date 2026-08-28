---
layout: post
title: "Docker Compose ile Çoklu Servis Orkestrasyonu: Tek Dosyada Uyumlu Konteynerler"
math: true
categories: 
  - Program
tags: 
  - Docker Compose
  - Konteyner
  - Orkestrasyon
  - DevOps
---

Modern bir uygulama nadiren tek başına çalışır: API’nin veritabanına, arka plan işlerinin kuyruk sistemine, tüm ekibin de tutarlı bir geliştirme ortamına ihtiyacı vardır. Docker Compose, bu parçaları tek tek `docker run` komutlarıyla başlatmak yerine, aralarındaki ilişkiyi bildirime dayalı bir YAML dosyasında tanımlamanızı sağlar. Sonuç, “benim makinemde çalışıyordu” cümlesini daha az duyduğunuz, tekrarlanabilir bir çalışma düzenidir.

``

## Compose neden orkestrasyon hissi verir?

Compose tam ölçekli bir Kubernetes alternatifi değildir; özellikle tek makinedeki geliştirme, test ve küçük dağıtımlar için tasarlanmıştır. Buna rağmen servisleri, ağları, kalıcı diskleri ve ortam değişkenlerini birlikte yöneterek küçük bir orkestratör gibi davranır. Temel fikir şudur: uygulamanın mimarisi kodun yanında sürümlenir.

Bir sistemde servis bağımlılığını yönlü bir grafik olarak düşünebilirsiniz. Bir API’nin PostgreSQL ve Redis’e ihtiyaç duyduğu durumda ilişki şöyledir:

$$API \rightarrow \{PostgreSQL, Redis\}$$

Bu ifade, API’nin her iki servise de erişmesi gerektiğini anlatır. Ancak erişilebilirlik ile hazır olma durumu aynı şey değildir. Konteynerin çalışıyor olması, veritabanının bağlantı kabul etmeye hazır olduğu anlamına gelmez. Bu küçük ama kritik ayrım, güvenilir Compose dosyalarının kalbidir.

| Kavram | Ne sağlar? | Tipik kullanım |
|---|---|---|
| `services` | Çalışan bileşenlerin tanımı | API, PostgreSQL, Redis |
| `networks` | Servisler arası güvenli iletişim | `db:5432` ile bağlantı |
| `volumes` | Kalıcı veri saklama | Veritabanı dosyaları |
| `depends_on` | Başlatma/bağımlılık sırası | API’den önce DB |
| `healthcheck` | Gerçek hazır olma kontrolü | `pg_isready` testi |

## Uygulanabilir bir üçlü: API, PostgreSQL ve Redis

Aşağıdaki örnek, Node.js tabanlı bir API’yi PostgreSQL ve Redis ile aynı ağda ayağa kaldırır. `api` servisi, diğer servislerin sağlık kontrolü başarılı olduktan sonra başlar.

```yaml
services:
  api:
    build: ./api
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgres://app:secret@db:5432/appdb
      REDIS_URL: redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
      interval: 5s
      timeout: 3s
      retries: 10

  cache:
    image: redis:7-alpine

volumes:
  postgres_data:
```

Buradaki önemli ayrıntı servis adlarıdır. Compose varsayılan olarak bir ağ oluşturur ve her servis adını bu ağ içinde DNS adı hâline getirir. Dolayısıyla API, `localhost` yerine `db` ve `cache` isimleriyle bağlantı kurar. Konteyner içindeki `localhost` yalnızca o konteynerin kendisidir; bu, başlangıç seviyesinde en sık yapılan hatalardan biridir.

## Başlatma sırası, dayanıklılık ve günlük rutin

`depends_on`, bağımlı servislerin önce oluşturulmasına yardım eder; fakat uygulamanızın geçici ağ hatalarına karşı yeniden deneme mantığına sahip olması yine de iyi bir fikirdir. Sağlık kontrolü bu boşluğu azaltır, yeniden deneme ise üretim dünyasının sürprizlerine karşı emniyet kemeridir.

| Komut | Görevi |
|---|---|
| `docker compose up -d --build` | İmajları oluşturur ve servisleri arka planda başlatır |
| `docker compose logs -f api` | Sadece API günlüklerini canlı izler |
| `docker compose ps` | Servis ve sağlık durumlarını gösterir |
| `docker compose down -v` | Ortamı ve ilişkili volume’leri temizler |

Gizli bilgileri YAML içine gömmek yerine `.env` dosyası veya platformunuzun secret mekanizmasını kullanın. Ayrıca geliştirmede kaynak kodunu volume olarak bağlamak pratikken, üretimde değişmez imajlar tercih edilmelidir. Compose’un asıl gücü tek komutta başlamak değil; ekibin herkes için aynı bağımlılık grafiğini, aynı ağ kurallarını ve aynı veri yaşam döngüsünü çalıştırabilmesidir. Küçük bir YAML dosyasıyla karmaşık bir sistemi anlaşılır, taşınabilir ve tekrar kurulabilir hâle getirirsiniz.
