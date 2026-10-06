---
layout: post
title: "Kendi Not Bulutunu Kur: Joplin Server, Trilium ve SilverBullet Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - not-alma
  - joplin
  - trilium
  - silverbullet
  - self-hosted
  - docker
toc: true
image: /img/kendi-not-bulutunu-54.png
---

Notlarımız artık yalnızca alışveriş listelerinden ibaret değil; proje fikirleri, kod parçaları, toplantı kayıtları ve kişisel bilgi arşivimiz aynı yerde yaşıyor. Bulut servislerine teslim olmak istemeyenler için Joplin Server, Trilium ve SilverBullet üç güçlü seçenek sunuyor. Fakat aynı problemi çözmeye çalışsalar da yaklaşımları oldukça farklı: biri senkronizasyon merkezi, biri kişisel bilgi ağacı, diğeri ise programlanabilir bir Markdown çalışma alanı.


![kendi-not-bulutunu-54](/img/kendi-not-bulutunu-54.svg)

``

## Önce problemi tanımlayalım

Bir not sisteminin değerini yalnızca not sayısıyla ölçemeyiz. Aradığımız şey; bilgiye hızlı erişmek, cihazlar arasında tutarlılık sağlamak ve veriyi uzun yıllar kullanılabilir biçimde saklamaktır. Basit bir değerlendirme modeli şöyle kurulabilir:

$$
P = 0.30E + 0.25S + 0.20G + 0.15O + 0.10K
$$

Burada $E$ erişilebilirlik, $S$ senkronizasyon, $G$ genişletilebilirlik, $O$ veri sahipliği ve $K$ kullanım kolaylığıdır. Katsayılar kişisel önceliklere göre değişebilir. Örneğin mobil kullanım önemliyse senkronizasyonun ağırlığını artırmak mantıklıdır.

## Üç farklı yaklaşım

**Joplin Server**, doğrudan bir not düzenleyici değildir. Joplin masaüstü ve mobil istemcileri arasında senkronizasyon sağlayan sunucu bileşenidir. Çevrimdışı çalışma, uçtan uca şifreleme ve güçlü mobil uygulamalar isteyenler için avantajlıdır.

**Trilium**, hiyerarşik notlar ve notlar arası ilişkiler üzerine kuruludur. Bir not birden fazla konumda bulunabilir; özellikler, bağlantılar ve görselleştirmeler sayesinde kişisel bir wiki oluşturulabilir. Orijinal Trilium projesinin devamı için günümüzde topluluk tarafından geliştirilen **TriliumNext Notes** sürümüne bakmak daha doğru olacaktır.

**SilverBullet** ise Markdown dosyalarını merkezine alan, tarayıcı üzerinden çalışan ve Lua tabanlı betiklerle genişletilebilen programlanabilir bir not ortamıdır. Not tutarken sistemi kendi kurallarınıza göre dönüştürmek istiyorsanız oldukça eğlencelidir.

| Özellik | Joplin Server | Trilium | SilverBullet |
|---|---|---|---|
| Temel yaklaşım | İstemci senkronizasyonu | Bilgi ağacı ve wiki | Programlanabilir Markdown |
| Mobil deneyim | Çok güçlü | Tarayıcı ağırlıklı | PWA/tarayıcı |
| Çevrimdışı kullanım | Güçlü | Sınırlı senaryolar | Yapılandırmaya bağlı |
| Veri biçimi | Joplin veri modeli | Veritabanı | Markdown dosyaları |
| Genişletilebilirlik | Eklentiler | Betikler ve özellikler | Lua, şablonlar, sorgular |
| Öğrenme eğrisi | Düşük-orta | Orta | Orta-yüksek |

## Docker ile hızlı başlangıç

Aşağıdaki örnek, SilverBullet’ı yerel ağda çalıştırır. `./space` klasörü notların tutulduğu dizindir; böylece konteyner silinse bile Markdown dosyaları korunur.

```yaml
services:
  silverbullet:
    image: ghcr.io/silverbulletmd/silverbullet:latest
    container_name: silverbullet
    restart: unless-stopped
    ports:
      - "3000:3000"
    volumes:
      - ./space:/space
    environment:
      - SB_USER=admin:guclu-bir-parola
```

Dosyayı `compose.yml` adıyla kaydettikten sonra sistemi başlatabilirsiniz:

```bash
docker compose up -d
docker compose logs -f silverbullet
```

İlk komut servisi arka planda çalıştırır, ikincisi ise başlangıç günlüklerini izler. İnternet üzerinden erişim verilecekse doğrudan port açmak yerine HTTPS sağlayan Caddy veya Nginx gibi bir ters vekil kullanılmalıdır. Düzenli yedekleme de unutulmamalıdır:

```bash
tar -czf "notes-$(date +%F).tar.gz" ./space
```

## Hangisini seçmelisiniz?

Telefon ve bilgisayar arasında sorunsuz senkronizasyon, çevrimdışı kullanım ve tanıdık bir uygulama deneyimi istiyorsanız **Joplin Server** öne çıkar. Büyük bir kişisel bilgi tabanı kuracak, notları hiyerarşi ve bağlantılarla yönetecekseniz **Trilium** daha uygundur. Dosyalarım sade Markdown olsun, sistemi sorgular ve betiklerle kendim şekillendireyim diyorsanız **SilverBullet** keyifli bir seçimdir.

En iyi sistem, en fazla özelliğe sahip olan değil, not eklerken sizi en az duraksatandır. Önce birkaç haftalık deneme arşivi oluşturun; arama, yedekleme ve mobil erişim akışlarını sınayın. Çünkü kullanılmayan kusursuz bir bilgi sistemi, düzenli kullanılan basit bir metin dosyasından daha değersizdir.
