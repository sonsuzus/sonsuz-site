---
layout: post
title: "x86’dan ARM’a: Docker Buildx ile Çok Mimarili İmaj Derleme"
math: true
categories: 
  - Program
tags: 
  - docker
  - buildx
  - arm
toc: true
---

Bir projeyi x86 bilgisayarınızda sorunsuz çalıştırmanız, onun ARM tabanlı bir bulut sunucusunda da doğrudan çalışacağı anlamına gelmez. İşlemci komut setleri arasındaki fark, özellikle derlenmiş uygulamalarda ve yerel bağımlılıklarda kendini gösterir. Neyse ki Docker Buildx; x86 geliştirme ortamından ayrılmadan ARM64 uyumlu, hatta birden fazla mimariyi destekleyen imajlar üretmemizi sağlar.

``

## Mimari farkı neden önemli?

x86-64 ve ARM64 işlemciler aynı işi farklı makine komutlarıyla gerçekleştirir. JavaScript veya Python gibi yorumlanan dillerde bile çalışma zamanı, sistem kütüphaneleri ve yerel eklentiler belirli bir mimari için derlenmiştir. Örneğin x86 için hazırlanmış bir ikili dosya, ARM sunucuda çalıştırıldığında `exec format error` hatası verebilir.

Bir uygulamanın toplam çalışma süresini kabaca şöyle düşünebiliriz:

$$T_{toplam} = T_{hesaplama} + T_{bellek} + T_{girdi/çıktı}$$

ARM sunucular enerji verimliliği ve yüksek çekirdek sayısıyla özellikle paralel işlerde avantaj sağlayabilir. Ancak gerçek kazanç, uygulamanın iş yüküne ve bağımlılıklarının ARM desteğine bağlıdır.

| Özellik | x86-64 | ARM64 |
|---|---|---|
| Yaygın kullanım | Masaüstü, klasik sunucu | Bulut, mobil, enerji verimli sunucu |
| Komut seti yaklaşımı | Daha karmaşık komutlar | Daha sade komutlar |
| Docker platform adı | `linux/amd64` | `linux/arm64` |
| Eski yazılım desteği | Genellikle güçlü | Bağımlılığa göre değişebilir |
| Enerji verimliliği | Donanıma bağlı | Çoğunlukla avantajlı |

## Buildx nasıl çalışır?

Buildx, Docker’ın BuildKit altyapısını kullanır. Farklı mimariler için derleme yaparken üç yöntemden yararlanabilir: QEMU ile işlemci emülasyonu, mimariye özel uzak derleme düğümleri veya kaynak kodun çapraz derlenmesi. Emülasyon kolaydır fakat yerel derlemeye göre yavaş olabilir. Çapraz derleme ise destekleyen dillerde daha hızlıdır.

Önce yeni bir builder oluşturalım:

```bash
docker buildx create --name multiarch --driver docker-container --use
docker buildx inspect --bootstrap
```

Bu komutlar, BuildKit kullanan `multiarch` isimli bir derleyici oluşturur ve gerekli bileşenleri başlatır. Linux ortamında QEMU desteği yoksa aşağıdaki kayıt işlemi gerekebilir:

```bash
docker run --privileged --rm tonistiigi/binfmt --install all
```

Docker Desktop çoğu zaman bu desteği hazır getirir. Ayrıcalıklı konteyner çalıştırıldığı için komutu yalnızca güvendiğiniz imajlarla kullanmanız önemlidir.

## Çok mimarili Dockerfile hazırlamak

Go uygulaması üzerinden çapraz derleme yapan örnek bir Dockerfile şöyle olabilir:

```dockerfile
FROM --platform=$BUILDPLATFORM golang:1.24-alpine AS builder
ARG TARGETOS
ARG TARGETARCH
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=$TARGETOS GOARCH=$TARGETARCH \
    go build -o /out/server ./cmd/server

FROM alpine:3.21
COPY --from=builder /out/server /usr/local/bin/server
EXPOSE 8080
ENTRYPOINT ["server"]
```

`BUILDPLATFORM`, derleme işleminin yürütüldüğü sistemi; `TARGETOS` ve `TARGETARCH` ise üretilecek imajın hedefini belirtir. Çok aşamalı yapı sayesinde derleme araçları son imaja taşınmaz. Böylece imaj daha küçük ve saldırı yüzeyi daha dar olur.

Node.js veya Python projelerinde yerel modüller bulunuyorsa bağımlılık kurulumu hedef platforma ait aşamada yapılmalıdır. x86 üzerinde oluşturulmuş `node_modules` veya sanal ortam klasörünü ARM imajına kopyalamak, oldukça yaratıcı hata mesajları üretmenin kestirme yoludur!

## İmajı derlemek ve yayımlamak

Her iki mimariyi tek etiket altında kayıt deposuna gönderebiliriz:

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t registry.example.com/demo/server:1.0.0 \
  --push .
```

Buildx burada iki imaj ve bunları birleştiren manifest listesi üretir. Sunucu, `docker pull` sırasında kendi mimarisine uygun imajı otomatik seçer. Sonucu doğrulamak için şu komut kullanılabilir:

```bash
docker buildx imagetools inspect registry.example.com/demo/server:1.0.0
```

Yalnızca yerel ARM imajı gerekiyorsa `--platform linux/arm64 --load` kullanılabilir. Çok platformlu sonuçlar klasik Docker imaj deposuna aynı anda yüklenemediğinden, çoklu derlemelerde genellikle `--push` tercih edilir.

Son olarak taban imajınızın ARM64 varyantına sahip olduğunu kontrol edin, sürümleri sabitleyin ve mümkünse CI sisteminde gerçek bir ARM düğümüyle test çalıştırın. Buildx mimari geçişi kolaylaştırır; fakat uygulamanın doğru davranmasını doğrulamak hâlâ testlerin görevidir.
