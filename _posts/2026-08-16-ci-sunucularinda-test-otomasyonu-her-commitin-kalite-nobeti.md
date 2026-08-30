---
layout: post
title: "CI Sunucularında Test Otomasyonu: Her Commit’in Kalite Nöbeti"
math: true
categories: 
  - Bilgi
tags: 
  - sürekli entegrasyon
  - test otomasyonu
  - devops
image: /img/ci-sunucularinda-test-80.png
---

Bir yazılım projesinde kaliteyi yalnızca sürüm yayınlanırken kontrol etmek, alarmı ev yanmaya başladıktan sonra kurmaya benzer. Sürekli Entegrasyon (CI) sunucuları bu yaklaşımı tersine çevirir: Geliştirici her kod değişikliğini merkezi depoya gönderdiğinde test paketi otomatik olarak çalışır, sorunları erken yakalar ve ekibe hızlı geri bildirim verir. Böylece kalite, sonradan eklenen pahalı bir denetim değil, geliştirme döngüsünün doğal bir parçası olur.


![ci-sunucularinda-test-80](/img/ci-sunucularinda-test-80.svg)

``

CI’ın temel mantığı, kod tabanını sürekli olarak **çalışabilir ve doğrulanmış** durumda tutmaktır. Bir commit geldiğinde sunucu bağımlılıkları temiz bir ortamda kurar, projeyi derler, statik analizleri çalıştırır ve testleri yürütür. Bu temiz ortam kritik önemdedir; geliştiricinin bilgisayarında çalışan ancak başka makinede bozulan “bende çalışıyordu” vakalarının etkisini azaltır.

Kaliteyi basitçe hataların üretime ulaşmama olasılığı olarak düşünebiliriz. Her test katmanı bir hatayı yakalama olasılığı taşıyorsa, bağımsız kontroller için toplam yakalama olasılığı yaklaşık olarak şöyle modellenebilir:

$$P(\text{yakalama}) = 1 - \prod_{i=1}^{n}(1-p_i)$$

Burada $p_i$, ilgili test katmanının hatayı bulma olasılığıdır. Birim test, entegrasyon testi ve uçtan uca test birbirinin yerine geçmez; farklı hata sınıflarına karşı savunma hattı oluştururlar. Ancak bu formül, testlerin gerçekten anlamlı senaryoları kapsadığı varsayımıyla değerlidir. Yüzlerce zayıf test, birkaç kritik davranışı sınayan iyi testten daha güvenilir olmayabilir.

| Test türü | Hedefi | Hızı | CI içindeki ideal kullanım |
|---|---|---:|---|
| Birim testi | Tek fonksiyon veya sınıf davranışı | Çok yüksek | Her commit’te mutlaka |
| Entegrasyon testi | Bileşenler, veritabanı ve servis ilişkileri | Orta | Her commit veya merge isteğinde |
| Uçtan uca test | Gerçek kullanıcı akışı | Düşük | Merge isteği ve gece çalıştırmaları |
| Statik analiz | Kod kokuları, güvenlik ve stil ihlalleri | Yüksek | Derleme aşamasında |

Başarılı bir boru hattı, testleri rastgele sıraya koymaz. En hızlı ve en sık hata yakalayan kontroller önce gelir. Böylece geliştirici, iki dakikada görülebilecek bir sözdizimi hatası için yirmi dakikalık tarayıcı testlerini beklemez. Bu yaklaşım “hızlı başarısız ol” ilkesidir. Örneğin bir Node.js projesinde temel aşamalar şöyle tanımlanabilir:

```yaml
stages:
  - lint
  - test
  - build

lint:
  script:
    - npm ci
    - npm run lint

unit_tests:
  stage: test
  script:
    - npm test -- --coverage

build:
  stage: build
  script:
    - npm run build
```

Bu yapılandırmada `npm ci`, kilit dosyasına göre tekrarlanabilir bağımlılık kurulumu yapar. Lint aşaması biçim ve olası hata kontrollerini erkenden keser; birim testleri davranışı doğrular; derleme ise dağıtılabilir çıktının üretilebildiğini kanıtlar. Gerçek projelerde buna güvenlik açığı taraması, konteyner imajı denetimi ve entegrasyon testleri de eklenebilir.

CI testlerinin asıl değeri yalnızca hata bulması değildir; ekip içi iletişimi de standartlaştırır. Başarısız bir pipeline, “hangi değişiklik, hangi kontrolü bozdu?” sorusuna somut yanıt verir. Merge isteğine yeşil kontrol zorunluluğu koymak, kişisel yorumlara dayalı kalite tartışmalarını ölçülebilir kurallara dönüştürür.

Yine de her şeyi her commit’te çalıştırmak doğru değildir. Uzun süren, kararsız veya dış servis bağımlılığı yüksek testler geliştiricilerin geri bildirimi görmezden gelmesine yol açabilir. Bu nedenle testler paralelleştirilmeli, flaky testler öncelikle düzeltilmeli ve ağır senaryolar zamanlanmış işlere ayrılmalıdır. Sağlıklı hedef, mutlak test sayısı değil; güvenilir, hızlı ve karar vermeyi kolaylaştıran bir geri bildirim döngüsüdür. CI sunucusu bu döngünün sessiz ama yorulmak bilmeyen kalite nöbetçisidir.
