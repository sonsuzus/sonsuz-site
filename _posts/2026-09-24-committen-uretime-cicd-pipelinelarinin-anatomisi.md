---
layout: post
title: "Commit’ten Üretime: CI/CD Pipeline’larının Anatomisi"
math: true
categories: 
  - Bilgi
tags: 
  - ci/cd
  - devops
  - otomasyon
  - docker
  - test
  - deployment
toc: true
---

Bir geliştirici kodunu depoya gönderdiğinde görünmez bir fabrika çalışmaya başlar: kaynak kod derlenir, testlerden geçirilir, paketlenir ve kontrollü biçimde kullanıcılarla buluşturulur. CI/CD pipeline adı verilen bu otomatik yolculuk, “Benim bilgisayarımda çalışıyordu!” cümlesini tarihe gömmeyi hedefleyen teknik aşamalar ile güvenlik kapılarından oluşur.
``

## CI ve CD gerçekte ne anlama gelir?

**Continuous Integration (CI)**, geliştiricilerin değişikliklerini sık aralıklarla ortak kod tabanına birleştirmesidir. Her commit sonrasında otomatik kontroller çalıştırılarak hatanın kaynağı henüz sıcakken bulunur.

**Continuous Delivery**, doğrulanmış sürümün üretime gönderilmeye her an hazır tutulmasıdır; üretim dağıtımı insan onayı gerektirebilir. **Continuous Deployment** ise bu son onayı da otomatikleştirir. Testleri geçen değişiklik doğrudan üretime ilerler.

| Yaklaşım | Otomatik test | Otomatik paketleme | Üretime geçiş |
|---|---:|---:|---|
| Continuous Integration | Evet | Genellikle | Kapsam dışı |
| Continuous Delivery | Evet | Evet | Manuel onaylı |
| Continuous Deployment | Evet | Evet | Tam otomatik |

Pipeline başarısını basitçe şu fikirle değerlendirebiliriz:

$$Güven = Test\ Kapsamı \times Tekrarlanabilirlik \times Gözlemlenebilirlik$$

Çarpanlardan biri sıfıra yaklaşıyorsa sisteme duyulan güven de hızla azalır. Yüzde yüz test kapsamı bile farklı ortamlarda farklı sonuç veren bir derleme sürecini kurtaramaz.

## Yolculuğun temel durakları

### 1. Commit ve tetikleme

Süreç, Git deposuna yapılan `push` veya açılan pull request ile başlar. Pipeline önce değişen dosyaları, dal kurallarını ve commit bilgisini inceler. Küçük ve sık commit’ler geri bildirim süresini kısaltır; devasa commit’ler ise hata avını polisiye romana dönüştürür.

### 2. Build ve bağımlılıklar

Kaynak kod çalıştırılabilir pakete dönüştürülür. Bağımlılık sürümleri kilit dosyalarıyla sabitlenmeli, derleme temiz bir ortamda tekrarlanabilmelidir. Docker bu noktada oldukça kullanışlıdır:

```dockerfile
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

Bu Dockerfile bağımlılıkları deterministik biçimde kurar, uygulamayı derler ve her ortamda aynı imajın çalıştırılmasını sağlar. Ortamı değil, aynı paketlenmiş ürünü taşırsınız.

### 3. Kalite ve güvenlik kapıları

Pipeline sırasıyla lint, birim testi, entegrasyon testi ve güvenlik taraması çalıştırabilir. Hızlı kontrollerin önce çalıştırılması önemlidir; iki saniyede bulunabilecek biçim hatası için yirmi dakikalık uçtan uca testi beklemek anlamsızdır.

| Test türü | Hız | Kapsadığı alan | Amaç |
|---|---:|---|---|
| Birim testi | Çok hızlı | Fonksiyon veya sınıf | İzole davranışı doğrulamak |
| Entegrasyon testi | Orta | Servisler ve veritabanı | Bileşen iletişimini sınamak |
| Uçtan uca test | Yavaş | Tüm sistem | Kullanıcı akışını doğrulamak |

Toplam geri bildirim süresi yaklaşık olarak

$$T_{pipeline}=T_{build}+T_{test}+T_{scan}+T_{deploy}$$

şeklinde düşünülebilir. Bağımsız işler paralel çalıştırıldığında toplam süre, sürelerin toplamından çok en uzun işin süresine yaklaşır.

### 4. Artifact ve dağıtım

Başarılı build sonucunda üretilen Docker imajı, JAR veya paket bir **artifact** deposuna sürüm numarasıyla kaydedilir. Aynı artifact test, staging ve üretim ortamlarında ilerletilmelidir; her ortam için yeniden build almak sürprizlere davetiye çıkarır.

Basitleştirilmiş bir GitHub Actions adımı şöyle olabilir:

{% raw %}
```yaml
- name: Testleri çalıştır
  run: npm test
- name: İmajı oluştur
  run: docker build -t uygulama:${{ github.sha }} .
```
{% endraw %}

Commit SHA kullanılması, üretimde çalışan imajın hangi kod değişikliğine ait olduğunu izlenebilir kılar.

## Üretimde güvenli iniş

Dağıtım yalnızca dosya kopyalamak değildir. **Rolling deployment** sunucuları sırayla günceller; **blue-green deployment** eski ve yeni ortam arasında trafik değiştirir; **canary deployment** ise yeni sürümü önce küçük bir kullanıcı grubuna sunar.

Pipeline üretime ulaşınca bitmez. Hata oranı, gecikme ve kaynak tüketimi izlenmeli; kritik eşikler aşılırsa otomatik rollback uygulanmalıdır. İyi bir CI/CD sistemi hızlı olmaktan önce güvenilir, ölçülebilir ve geri alınabilirdir. Amaç geliştiriciyi hız trenine bindirmek değil, commit’ten kullanıcıya uzanan yolu korkuluklarla güvenceye almaktır.
