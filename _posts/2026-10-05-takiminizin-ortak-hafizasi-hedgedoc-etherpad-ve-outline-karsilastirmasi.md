---
layout: post
title: "Takımınızın Ortak Hafızası: HedgeDoc, Etherpad ve Outline Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - ortak-not
  - hedgedoc
  - etherpad
  - outline
  - self-hosted
  - markdown
toc: true
image: /img/takiminizin-ortak-hafizasi-56.png
---

Bir toplantıda herkesin aynı belgeye yazabildiğini, fikirlerin anında görünür olduğunu ve “son sürüm hangisiydi?” sorusunun tarihe karıştığını düşünün. Ortak not alma sistemleri tam olarak bunu sağlar. Ancak HedgeDoc, Etherpad ve Outline benzer görünseler de farklı ihtiyaçlara odaklanır: biri Markdown tutkunlarına, biri hızlı eş zamanlı düzenlemeye, diğeri ise kurumsal bilgi yönetimine göz kırpar.
``

## Ortak düzenleme nasıl çalışır?

Aynı belgeyi iki kişi eş zamanlı değiştirdiğinde sistemin çakışmaları çözmesi gerekir. Geleneksel dosyalarda son kaydeden kazanırken ortak editörler çoğunlukla **Operational Transformation (OT)** veya **CRDT** benzeri yaklaşımlar kullanır.

İki kullanıcının işlemlerini $o_a$ ve $o_b$ ile gösterelim. OT yaklaşımındaki temel amaç, işlemleri birbirine göre dönüştürerek şu yakınsamayı sağlamaktır:

$$
apply(apply(D, o_a), T(o_b, o_a)) = apply(apply(D, o_b), T(o_a, o_b))
$$

Burada $D$ başlangıç belgesi, $T$ ise bir işlemi diğerinin etkisine göre düzenleyen dönüşüm fonksiyonudur. Kısacası Ayşe başa bir kelime eklerken Mehmet sondaki cümleyi silebilir; sunucu her iki değişikliği de mantıklı bir sırada birleştirir. Kullanıcı açısından sonuç büyü gibidir, arka planda ise bolca algoritma çalışır.

## Üç aracın karakteri

| Özellik | HedgeDoc | Etherpad | Outline |
|---|---|---|---|
| Temel yaklaşım | Ortak Markdown editörü | Hızlı eş zamanlı metin düzenleme | Takım bilgi tabanı |
| En güçlü yanı | Teknik dokümantasyon | Toplantı ve beyin fırtınası | Düzenli, kalıcı kurumsal bilgi |
| Biçimlendirme | Markdown | Araç çubuklu sade editör | Zengin blok editörü |
| Organizasyon | Not ve bağlantı odaklı | Pad odaklı | Koleksiyonlar ve hiyerarşi |
| Self-host seçeneği | Var | Var | Var |
| Öğrenme eğrisi | Markdown bilenler için düşük | Çok düşük | Orta |

![takiminizin-ortak-hafizasi-56](/img/takiminizin-ortak-hafizasi-56.svg)


### HedgeDoc

HedgeDoc, kod parçaları, tablolar, MathJax formülleri ve diyagramlar içeren teknik notlarda parlar. Markdown metni ile önizlemeyi birlikte sunması geliştirici ekipleri için büyük avantajdır. Mimari karar kayıtları, ders notları ve teknik toplantı tutanakları için oldukça uygundur. Buna karşılık klasör tabanlı, kapsamlı bir şirket vikisi arıyorsanız tek başına biraz dağınık kalabilir.

### Etherpad

Etherpad’in sloganı adeta “bağlantıyı aç ve yazmaya başla”dır. Katılımcılar renklerle ayrılır, değişiklikler anında görünür ve sürüm geçmişi oynatılabilir. Eğitim oturumları, retrospektifler ve geçici çalışma belgeleri için idealdir. Ancak uzun vadeli bilgi mimarisi ve gelişmiş belge organizasyonu temel hedefi değildir.

### Outline

Outline, not editöründen çok düzenli bir bilgi merkezi gibi davranır. Belgeler koleksiyonlara ayrılabilir; arama, erişim izinleri ve bağlantılı içeriklerle şirket içi dokümantasyon oluşturulabilir. Kullanıcı deneyimi şıktır, fakat kurulumunda veritabanı, Redis ve kimlik doğrulama gibi bileşenler diğer seçeneklere göre daha fazla dikkat isteyebilir.

## Etherpad için örnek Docker Compose kurulumu

Aşağıdaki yapı, Etherpad’i PostgreSQL ile ayağa kaldıran orta ölçekli bir başlangıç örneğidir:

```yaml
services:
  etherpad:
    image: etherpad/etherpad:latest
    ports:
      - "9001:9001"
    environment:
      DB_TYPE: postgres
      DB_HOST: database
      DB_NAME: etherpad
      DB_USER: etherpad
      DB_PASS: guclu-bir-parola
    depends_on:
      - database

  database:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: etherpad
      POSTGRES_USER: etherpad
      POSTGRES_PASSWORD: guclu-bir-parola
    volumes:
      - etherpad_db:/var/lib/postgresql/data

volumes:
  etherpad_db:
```

Dosyayı `compose.yml` adıyla kaydedip `docker compose up -d` komutunu çalıştırdığınızda uygulama `http://localhost:9001` adresinde açılır. Gerçek ortamda parolaları kaynak dosyada tutmamak, HTTPS sağlayan bir ters vekil kullanmak ve düzenli yedek almak gerekir.

## Hangisini seçmeli?

Hızlı ve geçici ortak yazım için **Etherpad**, Markdown ağırlıklı teknik çalışmalar için **HedgeDoc**, kalıcı ve kategorize edilmiş şirket bilgisi için **Outline** daha güçlü seçimdir. Kararı kullanıcı sayısından önce iş akışına göre verin. En iyi araç en fazla özelliğe sahip olan değil, ekibin gerçekten açıp kullandığı araçtır.
