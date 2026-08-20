---
layout: post
title: "CI/CD Pipeline Tasarımı: Commit'ten Canlıya Otomatik Yolculuk"
math: true
categories: 
  - Proje
tags: 
  - cı/cd
  - devops
  - github actions
image: /img/cicd-pipeline-tasarimi-54.png
---

Bir geliştiricinin `git push` komutundan sonra kahvesini yudumlarken testlerin çalışması, güvenlik kontrollerinin yapılması ve uygulamanın güvenle dağıtılması kulağa sihir gibi gelir. Aslında bunun adı CI/CD pipeline tasarımıdır. İyi kurulmuş bir pipeline, tekrarlanan insan işlerini otomatikleştirir; hataları erken yakalar ve sürüm alma stresini öngörülebilir bir sürece dönüştürür.

``

CI, yani **Continuous Integration (Sürekli Entegrasyon)**, küçük kod değişikliklerini ana kod tabanıyla sık sık birleştirme pratiğidir. Her birleşimde proje derlenir ve otomatik test edilir. CD ise bağlama göre **Continuous Delivery** veya **Continuous Deployment** anlamına gelir. İlki üretime gönderilecek paketi her an hazır tutar; ikincisi onay beklemeden üretime otomatik dağıtım yapar.

Pipeline'ı bir kalite kontrol bandı gibi düşünebiliriz. Her aşama bir öncekinin çıktısını doğrular. Bir aşama başarısız olursa süreç durur; böylece problemli kodun canlı ortama ulaşma olasılığı azalır. Basitçe teslimat güvenini aşağıdaki çarpanlarla modelleyebiliriz:

$$Güven = Test\ Kapsamı \times Kontrol\ Kalitesi \times Geri\ Alma\ Kapasitesi$$

Bu formül akademik bir ölçüm değildir; önemli mesaj şudur: yalnızca çok test yazmak yetmez. Güvenlik taraması, sürümleme, izleme ve geri alma planı da zincirin parçalarıdır.

| Aşama | Amaç | Başarısız olursa |
|---|---|---|
| Lint ve build | Sözdizimi, stil ve derleme sorunlarını bulmak | Geliştirici hızlı geri bildirim alır |
| Unit test | Fonksiyonların davranışını doğrulamak | Kod değişikliği engellenir |
| Entegrasyon testi | Servislerin birlikte çalışmasını denemek | Ortam veya API uyumsuzluğu görünür |
| Paketleme | Değişmez dağıtım artefaktı üretmek | Sürüm yayınlanmaz |
| Deploy | Artefaktı hedef ortama taşımak | Önceki sürüme dönülür |

![cicd-pipeline-tasarimi-54](/img/cicd-pipeline-tasarimi-54.svg)


Örnek olarak Node.js tabanlı bir servis için GitHub Actions kullanabiliriz. Aşağıdaki iş akışı, `main` dalına yapılan her gönderimde kodu kurar, test eder, Docker imajı üretir ve kayıt defterine yollar. Gerçek projede kayıt defteri kimlik bilgileri kesinlikle repository secret olarak saklanmalıdır.

```yaml
name: CI-CD
on:
  push:
    branches: [main]

jobs:
  test-and-package:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - name: Docker imajını oluştur
        run: docker build -t ghcr.io/acme/api:${{ github.sha }} .
      - name: Registry'e gönder
        run: docker push ghcr.io/acme/api:${{ github.sha }}
```

Buradaki kritik karar, imajı `latest` yerine commit SHA ile etiketlemektir. Çünkü aynı imajı test, staging ve üretim ortamlarında çalıştırmak isteriz. Bu yaklaşıma **build once, deploy many** denir: bir kez üretilen artefakt, değiştirilmeden farklı ortamlara taşınır. Böylece staging'de doğrulanan şeyin üretimdeki şeyle aynı olması sağlanır.

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Manuel dağıtım | İlk kurulum hızlıdır | İnsan hatası ve izlenebilirlik kaybı |
| Continuous Delivery | Üretim onayı kontrol altındadır | Onay noktası gecikme yaratabilir |
| Continuous Deployment | En hızlı geri bildirim döngüsü | Güçlü test ve gözlemleme zorunludur |

Dağıtımdan sonra iş bitmez. Health check, hata oranı, gecikme ve kaynak tüketimi izlenmelidir. Canary deployment ile trafiğin örneğin %5'i yeni sürüme yönlendirilir; metrikler kötüleşirse otomatik rollback tetiklenir. Ayrıca veritabanı migration'larını geriye uyumlu tasarlamak önemlidir: önce yeni alanı ekleyin, uygulamayı geçirin, eski alanı daha sonraki sürümde kaldırın.

Sonuç olarak başarılı bir CI/CD pipeline, sadece YAML dosyası değildir; ekip alışkanlıkları, test stratejisi ve operasyonel disiplinin kodlanmış hâlidir. Küçük bir lint-test-build zinciriyle başlayın, sonra güvenlik taraması, staging onayı ve gözlemlenebilirlik katmanlarını ekleyin. Pipeline ne kadar görünür ve tekrar üretilebilir olursa, dağıtımlar da o kadar sıkıcı olur; DevOps dünyasında sıkıcı, harika bir iltifattır.
