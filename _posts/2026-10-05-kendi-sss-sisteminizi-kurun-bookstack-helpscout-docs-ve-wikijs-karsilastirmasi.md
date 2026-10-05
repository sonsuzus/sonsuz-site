---
layout: post
title: "Kendi SSS Sisteminizi Kurun: BookStack, HelpScout Docs ve Wiki.js Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - sss
  - wiki.js
  - bookstack
  - helpscout
  - dokümantasyon
  - self-hosted
toc: true
image: /img/kendi-sss-sisteminizi-44.png
---

Bir ürün büyüdükçe kullanıcıların soruları da çoğalır: “Şifremi nasıl değiştiririm?”, “Fatura nerede?” veya teknoloji dünyasının değişmez klasiği, “Neden çalışmıyor?” İyi tasarlanmış bir SSS sistemi, destek ekibinin tekrar eden taleplerle uğraşmasını azaltırken kullanıcıların cevaba saniyeler içinde ulaşmasını sağlar. BookStack, HelpScout Docs ve Wiki.js ise bu ihtiyaca farklı yaklaşımlar sunar.

``

## SSS sistemi yalnızca soru-cevap listesi değildir

Başarılı bir SSS altyapısı; içerik yönetimi, arama, yetkilendirme, sürüm takibi ve geri bildirim bileşenlerinden oluşur. Kullanıcı bir soruyu yazdığında sistem yalnızca kelimeleri eşleştirmemeli, mümkünse niyeti de anlamalıdır.

Basit bir arama sıralama puanı şu şekilde düşünülebilir:

$$S = 0.5T + 0.3C + 0.2P$$

Burada $T$ başlık benzerliğini, $C$ içerik eşleşmesini, $P$ ise sayfanın popülerliğini temsil eder. Başlık eşleşmesine daha yüksek ağırlık verilmesi, “şifre sıfırlama” aramasında doğrudan ilgili makalenin öne çıkmasını sağlar. Daha gelişmiş sistemlerde bu yapı, semantik arama ve vektör veritabanlarıyla güçlendirilebilir.

## Üç farklı yaklaşım

| Özellik | BookStack | HelpScout Docs | Wiki.js |
|---|---|---|---|
| Barındırma | Kendi sunucunuz | SaaS | Kendi sunucunuz |
| İçerik modeli | Raf, kitap, bölüm, sayfa | Koleksiyon ve makale | Klasör ve sayfa |
| Teknik bilgi ihtiyacı | Orta | Düşük | Orta |
| Yetkilendirme | Ayrıntılı roller | Ekip odaklı | Ayrıntılı roller |
| Özelleştirme | Orta | Sınırlı/kolay | Yüksek |
| İdeal kullanım | Kurum içi bilgi tabanı | Müşteri destek merkezi | Teknik wiki ve dokümantasyon |

![kendi-sss-sisteminizi-44](/img/kendi-sss-sisteminizi-44.svg)


**BookStack**, gerçek bir kütüphane mantığıyla çalışır. Düzenli ve hiyerarşik içerik isteyen ekipler için oldukça sezgiseldir. İnsan kaynakları rehberleri, şirket prosedürleri veya iç eğitim dokümanları için güçlü bir seçenektir.

**HelpScout Docs**, sunucu yönetmek istemeyen ekipleri hedefler. Kurulum, güncelleme ve bakım yükü düşüktür. HelpScout destek sistemiyle bütünleşmesi önemli bir avantajdır; ancak abonelik maliyeti ve özelleştirme sınırları dikkate alınmalıdır.

**Wiki.js**, modern arayüzü, Markdown desteği, kimlik doğrulama seçenekleri ve Git tabanlı iş akışlarıyla geliştirici ekiplerine göz kırpar. “Hem SSS hem teknik dokümantasyon olsun” diyorsanız en esnek adaylardan biridir.

## Docker ile Wiki.js kurulumu

Aşağıdaki örnek, Wiki.js ile PostgreSQL’i aynı Docker ağı içinde çalıştırır. Veritabanı dışarıya açılmadığı için yalnızca Wiki.js tarafından erişilebilir:

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: wiki
      POSTGRES_USER: wikijs
      POSTGRES_PASSWORD: guclu-bir-parola
    volumes:
      - db_data:/var/lib/postgresql/data

  wiki:
    image: ghcr.io/requarks/wiki:2
    depends_on:
      - db
    environment:
      DB_TYPE: postgres
      DB_HOST: db
      DB_PORT: 5432
      DB_USER: wikijs
      DB_PASS: guclu-bir-parola
      DB_NAME: wiki
    ports:
      - 3000:3000

volumes:
  db_data:
```

Dosyayı `compose.yml` adıyla kaydettikten sonra sistemi başlatabilirsiniz:

```bash
docker compose up -d
```

Ardından tarayıcıdan `http://localhost:3000` adresine giderek yönetici hesabını oluşturabilirsiniz. Gerçek ortamda parolaları dosyaya yazmak yerine Docker Secrets veya bir gizli anahtar yöneticisi kullanmanız gerekir. HTTPS için de Caddy ya da Nginx gibi bir ters vekil önerilir.

## Hangi alternatif seçilmeli?

Hızlı biçimde müşteriye açık bir yardım merkezi gerekiyorsa HelpScout Docs pratiktir. Kitap benzeri katı bir düzen ve kolay editör deneyimi aranıyorsa BookStack öne çıkar. Açık kaynak, Markdown, geniş kimlik doğrulama desteği ve yüksek özelleştirme önemliyse Wiki.js daha uygundur.

Docusaurus, GitBook, Outline ve MkDocs da değerlendirmeye alınabilir. Seçimi yalnızca özellik sayısına göre değil; aylık toplam maliyet, bakım süresi ve içerik üretim kolaylığı üzerinden yapmak daha sağlıklıdır. Basit bir karar puanı $D = fayda - maliyet - bakım$ şeklinde modellenebilir. Sonuçta en iyi SSS sistemi, en gösterişli olan değil, kullanıcıya doğru cevabı en az tıklamayla ulaştırandır.
