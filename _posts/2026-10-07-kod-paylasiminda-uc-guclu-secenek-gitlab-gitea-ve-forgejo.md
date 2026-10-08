---
layout: post
title: "Kod Paylaşımında Üç Güçlü Seçenek: GitLab, Gitea ve Forgejo"
math: true
categories: 
  - Bilgi
tags: 
  - gitlab
  - gitea
  - forgejo
  - git
  - devops
  - kod-paylaşımı
toc: true
image: /img/kod-paylasiminda-uc-23.png
---

Bir yazılım projesinde kodu bilgisayarınızda saklamak kolaydır; asıl macera ekip büyüdüğünde başlar. Sürümler, incelemeler, hatalar ve otomasyon süreçleri derken sıradan bir Git deposundan fazlasına ihtiyaç duyulur. GitLab, Gitea ve Forgejo bu ihtiyacı karşılayan üç güçlü platformdur; ancak benzer görünen bu araçların hedefleri ve işletme maliyetleri farklıdır.
``
## Önce temel kavram: Git platformu ne yapar?

Git, dağıtık bir sürüm kontrol sistemidir. Her geliştirici deponun geçmişini kendi bilgisayarında tutabilir; commit oluşturabilir, dal açabilir ve değişiklikleri bir uzak sunucuya gönderebilir. GitLab, Gitea ve Forgejo ise Git'in üzerine kullanıcı yönetimi, web arayüzü, kod inceleme, sorun takibi ve otomasyon gibi katmanlar ekler.

Bir platform seçimini basitleştirmek için yaklaşık bir uygunluk puanı tanımlayabiliriz:

$$S = 0.30K + 0.25Y + 0.25D + 0.20T$$

Burada $K$ kurulum kolaylığını, $Y$ düşük kaynak kullanımını, $D$ DevOps özelliklerini ve $T$ topluluk uyumunu temsil eder. Katsayılar sabit değildir; örneğin kapsamlı CI/CD isteyen bir kurum $D$ değerinin ağırlığını artırmalıdır.

## Üç platformun karakteri

| Özellik | GitLab | Gitea | Forgejo |
|---|---|---|---|
| Ana yaklaşım | Hepsi bir arada DevOps | Hafif Git sunucusu | Topluluk odaklı hafif forge |
| Kaynak ihtiyacı | Yüksek | Düşük | Düşük |
| CI/CD | Yerleşik ve kapsamlı | Actions desteği | Actions desteği |
| Kurulum | Görece karmaşık | Oldukça kolay | Oldukça kolay |
| Uygun senaryo | Kurumsal ekipler | Kişisel veya küçük ekip | Bağımsız, açık topluluklar |

**GitLab**, depo barındırmanın yanında kapsamlı CI/CD, güvenlik taraması, paket kayıtları ve proje planlama araçları sunar. Tek platformla bütün yazılım yaşam döngüsünü yönetmek isteyen ekipler için güçlüdür. Bunun bedeli daha fazla RAM, işlemci ve bakım ihtiyacıdır. Küçük bir ev sunucusunda çalıştırılabilir olsa da rahat bir deneyim için kaynak planlaması gerekir.

**Gitea**, Go ile yazılmış hafif bir uygulamadır. Tek çalıştırılabilir dosya, SQLite desteği ve sade yönetim ekranı sayesinde hızlıca ayağa kalkar. GitHub benzeri arayüz isteyen küçük ekipler, öğrenciler ve kişisel laboratuvarlar için oldukça pratiktir.

**Forgejo**, Gitea kökenli, topluluk yönetimini ve özgür yazılım ilkelerini öne çıkaran bir platformdur. Kullanım deneyimi Gitea'ya çok yakındır. Teknik farklılıkların yanında yönetişim modeli önemlidir: Projenin ticari kararlar yerine topluluk tarafından şekillendirilmesini isteyenler Forgejo'yu tercih edebilir.

## Docker ile hızlı bir Gitea kurulumu

Aşağıdaki dosya Gitea'yı kalıcı veri alanıyla çalıştırır. `ports` bölümü web arayüzünü 3000, SSH erişimini ise 2222 numaralı port üzerinden sunar.

```yaml
services:
  gitea:
    image: gitea/gitea:latest
    container_name: gitea
    restart: unless-stopped
    ports:
      - 3000:3000
      - 2222:22
    volumes:
      - ./gitea-data:/data
```

Dosyayı `compose.yml` adıyla kaydettikten sonra sistemi başlatmak için şu komut yeterlidir:

```bash
docker compose up -d
```

Ardından tarayıcıdan `http://localhost:3000` adresine giderek veritabanı ve yönetici hesabı ayarlanabilir. Forgejo kurulumu da neredeyse aynıdır; yalnızca imaj `codeberg.org/forgejo/forgejo:latest` olarak değiştirilir.

## Hangisini seçmeli?

Kapsamlı boru hatları, güvenlik kontrolleri ve merkezi DevOps yönetimi gerekiyorsa GitLab mantıklı seçimdir. Düşük kaynak tüketimiyle hızlı bir özel Git sunucusu istiyorsanız Gitea öne çıkar. Aynı hafifliği topluluk merkezli bir yönetişim modeliyle arıyorsanız Forgejo daha uygundur.

Son karar yalnızca özellik sayısına göre verilmemelidir. Yedekleme, güncelleme sıklığı, ekip deneyimi ve sunucu kapasitesi de değerlendirilmelidir. En büyük platform her zaman en iyi platform değildir; bazen birkaç yüz megabayt bellekle çalışan küçük bir Forgejo sunucusu, ekibin bütün ihtiyacını sessizce karşılar.

![kod-paylasiminda-uc-23](/img/kod-paylasiminda-uc-23.svg)

