---
layout: post
title: "Görev Takibinde Üç Güçlü Seçenek: Vikunja, Taiga ve Redmine"
math: true
categories: 
  - Program
tags: 
  - görev yönetimi
  - vikunja
  - taiga
  - redmine
  - açık kaynak
  - proje yönetimi
toc: true
image: /img/gorev-takibinde-uc-27.png
---

Yapılacak işler büyüyüp renkli yapışkan notlar monitörün kenarından taşmaya başladığında bir görev takip sistemi kullanmanın zamanı gelmiş demektir. Açık kaynak dünyasında Vikunja, Taiga ve Redmine bu soruna farklı açılardan yaklaşır: Vikunja sadeliği, Taiga çevik geliştirme deneyimi, Redmine ise kapsamlı proje yönetimi yetenekleriyle öne çıkar.
``

## Görev takip sisteminin temel mantığı

Bir görev takip sistemi yalnızca dijital yapılacaklar listesi değildir. Temel amaç, işi küçük ve ölçülebilir parçalara ayırarak sorumlulukları, öncelikleri ve ilerlemeyi görünür hâle getirmektir. En basit modelde bir görev şu bileşenlerle gösterilebilir:

$$G = (a, s, o, t, e)$$

Burada $a$ görev açıklamasını, $s$ sorumlu kişiyi, $o$ önceliği, $t$ teslim tarihini ve $e$ mevcut durumu ifade eder. Projenin tamamlanma oranı ise kabaca şöyle hesaplanabilir:

$$İlerleme = \frac{Tamamlanan\ Görev}{Toplam\ Görev} \times 100$$

Elbette gerçek hayatta her görev aynı büyüklükte değildir. Beş dakikalık bir yazım düzeltmesiyle üç günlük API geliştirmesini eşit saymak yanıltıcı olabilir. Taiga’nın hikâye puanları ve Redmine’ın tahmini süreleri bu noktada daha gerçekçi ölçüm sağlar.

## Üç aracın karakteri

| Özellik | Vikunja | Taiga | Redmine |
|---|---|---|---|
| Temel yaklaşım | Yapılacaklar ve listeler | Scrum ve Kanban | Kapsamlı proje yönetimi |
| Öğrenme eğrisi | Düşük | Orta | Orta-yüksek |
| Arayüz | Modern ve sade | Görsel ve çevik | Geleneksel ve yoğun |
| En uygun ekip | Bireyler, küçük ekipler | Yazılım ve ürün ekipleri | Kurumsal, teknik ekipler |
| Öne çıkan özellik | Hızlı görev düzenleme | Sprint ve backlog | İş akışı, rol ve eklentiler |

### Vikunja: hızlı ve ferah

Vikunja, Trello ile klasik yapılacaklar uygulamalarının arasında konumlanır. Liste, Kanban, tablo ve Gantt görünümleri sunar. Tekrarlanan görevler, etiketler, öncelikler ve ekip paylaşımı sayesinde kişisel kullanımdan küçük ekip projelerine kadar rahatça ölçeklenebilir.

En büyük avantajı, kullanıcıyı ayar denizinde boğmadan işe başlatmasıdır. “Sunucuyu kur, kullanıcıyı aç, görevleri ekle” akışı oldukça pürüzsüzdür. Ancak ayrıntılı Scrum raporları veya çok katmanlı kurumsal yetkilendirme arayanlar için yetersiz kalabilir.

### Taiga: çevik ekiplerin oyun alanı

Taiga özellikle Scrum ve Kanban kullanan ekipler için tasarlanmıştır. Ürün backlog’u, sprint, kullanıcı hikâyesi, epic ve story point gibi çevik geliştirme kavramları uygulamanın merkezindedir. Bir kullanıcı hikâyesi “Kullanıcı olarak şifremi yenilemek istiyorum” biçiminde tanımlanabilir ve teknik görevlere bölünebilir.

Taiga’nın güçlü yanı, ürün hedefi ile günlük geliştirme işini aynı ekranda buluşturmasıdır. Buna karşılık yalnızca kişisel görevlerini takip etmek isteyen biri için sprint planlamak, market alışverişine Jira kurmak kadar iddialı olabilir.

### Redmine: İsviçre çakısı

Redmine; görev takibi, zaman kaydı, Gantt grafiği, wiki, dosya yönetimi, rol tabanlı yetkilendirme ve çoklu proje desteği sunar. Ruby on Rails tabanlıdır ve yıllardır kullanılan geniş bir eklenti ekosistemine sahiptir.

Arayüzü rakipleri kadar modern görünmeyebilir; fakat özelleştirilebilir iş akışları sayesinde “Geliştirici kapatabilir ama müşteri silemez” gibi ayrıntılı kurallar oluşturulabilir. Denetim izi, süreç disiplini ve farklı departmanların aynı sistemde çalışması önemliyse Redmine güçlü bir tercihtir.

## Docker ile örnek Vikunja kurulumu

Aşağıdaki yapı, verileri kalıcı bir dizinde saklayan basit bir Vikunja servisi başlatır:

```yaml
services:
  vikunja:
    image: vikunja/vikunja:latest
    ports:
      - "3456:3456"
    volumes:
      - ./vikunja-data:/app/vikunja/files
    environment:
      VIKUNJA_SERVICE_PUBLICURL: http://localhost:3456
```

Dosyayı `compose.yml` adıyla kaydedip `docker compose up -d` komutunu çalıştırdıktan sonra uygulamaya `http://localhost:3456` adresinden erişilebilir. Gerçek sunucuda HTTPS, düzenli yedekleme ve güvenli veritabanı yapılandırması ayrıca planlanmalıdır.

## Hangisini seçmeli?

Hızlı kurulum ve sade görev yönetimi için **Vikunja**, Scrum veya Kanban odaklı ürün geliştirme için **Taiga**, ayrıntılı yetkiler ve kurumsal süreçler için **Redmine** seçilebilir. En iyi araç, en fazla özelliğe sahip olan değil; ekibin düzenli olarak kullanacağı araçtır. Bu nedenle karar vermeden önce küçük bir deneme projesi kurmak, özellik listesini okumaktan daha değerli sonuç verir.

![gorev-takibinde-uc-27](/img/gorev-takibinde-uc-27.svg)

