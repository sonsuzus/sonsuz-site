---
layout: post
title: "Docker Multi-Stage Build ile Küçük, Güvenli ve Hızlı İmajlar"
math: true
categories: 
  - Bilgi
tags: 
  - docker
  - multi-stage build
  - devops
  - konteyner
  - node.js
image: /img/docker-multi-stage-13.png
---

Docker imajları, uygulamanın taşınabilir paketleridir; ancak pakete derleyici, kaynak kod, test araçları ve geçici dosyalar da girerse taşıması pahalı bir bavula dönüşür. Multi-stage build, derleme ortamını çalışma ortamından ayırarak bu bavulu sadeleştirir. Temel fikir basittir: Uygulamayı ilk aşamada üretin, yalnızca ortaya çıkan çalıştırılabilir çıktıyı ikinci aşamaya taşıyın. Böylece üretim imajı, geliştiricinin bütün atölyesini değil, müşterinin gerçekten kullanacağı ürünü içerir.

``

Klasik tek aşamalı Dockerfile yaklaşımında `npm install`, derleme araçları ve kaynak dosyalar aynı imajda kalır. Bu durum disk alanını artırdığı gibi saldırı yüzeyini de genişletir. Örneğin bir Node.js projesinde TypeScript derlemek için gereken paketler, uygulamanın JavaScript çıktısını çalıştırmak için gerekli olmayabilir. Multi-stage yapı, Dockerfile içindeki her `FROM` satırını ayrı bir aşama olarak ele alır. Bir aşama, önceki aşamadan dosya almak için isimlendirilebilir.

Teorik olarak toplam imaj maliyetini şöyle düşünebiliriz:

$$S_{final} = S_{runtime} + S_{artifact} + S_{production\ dependencies}$$

Tek aşamalı modelde ise yaklaşık olarak $S_{single}=S_{final}+S_{source}+S_{compiler}+S_{devDependencies}$ olur. Amaç, çalıştırma için zorunlu olmayan terimleri final imajdan çıkarmaktır. Katman önbelleği de bu tasarımın önemli oyuncusudur: Sık değişmeyen bağımlılık tanımlarını önce kopyalamak, her kod değişikliğinde bağımlılıkların yeniden indirilmesini engeller.

| Özellik | Tek aşamalı build | Multi-stage build |
|---|---|---|
| Kaynak kod | Final imajda kalabilir | Genellikle yalnızca çıktı kalır |
| Derleme araçları | Çalışma zamanına taşınır | Builder aşamasında kalır |
| Güvenlik yüzeyi | Daha geniş | Daha dar |
| İmaj boyutu | Çoğunlukla büyük | Genellikle daha küçük |
| Hata ayıklama | Her araç içeride olabilir | Ayrı debug hedefi gerekebilir |

![docker-multi-stage-13](/img/docker-multi-stage-13.svg)


Aşağıdaki örnek, TypeScript tabanlı bir Node.js uygulamasını iki aşamada paketler. İlk aşama derler, ikinci aşama yalnızca üretim bağımlılıklarını ve `dist` klasörünü taşır:

```dockerfile
# Derleme aşaması
FROM node:22-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Çalışma zamanı aşaması
FROM node:22-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production

COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force

COPY --from=builder /app/dist ./dist

USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

Burada `AS builder`, ilk aşamaya okunabilir bir isim verir. Kritik satır `COPY --from=builder /app/dist ./dist` ifadesidir: Docker, builder imajının tamamını değil, yalnızca derlenmiş uygulama çıktısını final aşamaya kopyalar. `npm ci --omit=dev` ise geliştirme bağımlılıklarını ikinci aşamada kurmaz. `USER node` seçimi de süreçlerin root yetkisiyle çalışmasını önleyerek ek bir güvenlik katmanı sağlar.

Her dosyayı körlemesine kopyalamamak için `.dockerignore` kullanmak şarttır. `node_modules`, `.git`, test raporları, yerel ortam dosyaları ve loglar build bağlamına bile girmemelidir. Bu, hem build gönderimini hızlandırır hem de yanlışlıkla gizli bilgi taşınması riskini azaltır.

| Dosya veya araç | Builder | Runtime |
|---|---:|---:|
| TypeScript derleyicisi | Evet | Hayır |
| Kaynak `.ts` dosyaları | Evet | Hayır |
| Derlenmiş `dist` çıktısı | Evet | Evet |
| Geliştirme bağımlılıkları | Evet | Hayır |
| Üretim bağımlılıkları | Gerekirse | Evet |

Son olarak imajı yalnızca boyut üzerinden değerlendirmeyin. `docker image inspect`, güvenlik tarayıcıları ve gerçek başlangıç süresi birlikte ölçülmelidir. Multi-stage build sihirli bir küçültme düğmesi değildir; doğru runtime tabanı, temiz bağımlılıklar ve bilinçli kopyalama ile etkisini gösterir. Yine de derleme atölyesi ile servis sahnesini ayırmak, Dockerfile tasarımında en yüksek getirili alışkanlıklardan biridir.
