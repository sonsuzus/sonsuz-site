---
layout: post
title: "Blue-Green Deployment ile Kesintisiz Sürüm Geçişleri"
math: true
categories: 
  - Bilgi
tags: 
  - DevOps
  - CI/CD
  - Blue-Green Deployment
---

Üretim ortamında yeni bir sürümü yayımlamak, yalnızca kodu sunucuya kopyalamaktan ibaret değildir: kullanıcı deneyimi, geri dönüş planı ve veri tutarlılığı aynı anda korunmalıdır. Blue-Green Deployment, iki eşdeğer ortam arasında trafiği kontrollü biçimde değiştirerek güncelleme anındaki kesintiyi neredeyse görünmez hâle getiren güçlü bir dağıtım stratejisidir.

``

Bu yaklaşımda **Blue** mevcut, kullanıcıların hizmet aldığı kararlı sürümü; **Green** ise yeni sürümün hazırlandığı paralel ortamı temsil eder. İsimler renkten çok roldür: Bir sonraki dağıtımda Green aktif olur, eski Blue ise geri dönüş adayı olarak bekler. Temel fikir, yeni sürümü canlı trafiğe maruz bırakmadan önce tamamen ayrı bir ortamda doğrulamaktır.

Trafik anahtarlama işlemi çoğunlukla yük dengeleyici, ters vekil (reverse proxy), DNS veya Kubernetes Service üzerinden yapılır. Başarılı geçişin hedefi, kullanıcının algıladığı kesintinin yaklaşık olarak sıfıra yaklaşmasıdır:

$$T_{kesinti} \approx T_{trafik\_yonlendirme}$$

Yani uygulamanın derlenmesi, imajın çekilmesi ve başlatılması kullanıcı trafiği üzerinde değil, pasif ortamda gerçekleşir. Aktif sürüme geçildiğinde yalnızca yönlendirme kuralı değişir.

| Özellik | Blue-Green | Rolling Update | Canary Release |
|---|---|---|---|
| Yeni sürümün maruziyeti | Bir anda tüm trafik | Kademeli pod/sunucu değişimi | Küçük kullanıcı yüzdesiyle başlar |
| Geri alma hızı | Çok yüksek | Orta | Yüksek |
| Altyapı maliyeti | Yüksek, iki ortam gerekir | Daha düşük | Orta |
| Gerçek trafikle risk ölçümü | Geçiş öncesi sınırlı | Kısmen | Çok güçlü |

## Süreç nasıl işler?

Önce Blue ortamı canlıdır. CI/CD hattı yeni uygulama sürümünü Green ortamına kurar; birim testleri, entegrasyon testleri, güvenlik taramaları ve smoke testleri burada çalışır. Green sağlıklıysa yük dengeleyicinin hedefi Blue'dan Green'e çevrilir. Metrikler beklenmedik hata, gecikme veya kaynak tüketimi göstermiyorsa eski ortam bir süre korunur. Sorun çıkarsa trafik saniyeler içinde tekrar Blue'ya döner. Bu, klasik "geri al" işlemlerinden çok daha güvenlidir; çünkü önceki sürüm hâlâ çalışmaktadır.

Aşağıdaki Nginx örneği, aktif upstream hedefini değiştirme fikrini basitleştirilmiş biçimde gösterir:

```nginx
upstream application {
    # Geçişten önce blue, geçişten sonra green aktif edilir.
    server blue-app:8080;
    # server green-app:8080;
}

server {
    listen 80;
    location / {
        proxy_pass http://application;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Bu yapılandırmada dağıtım sistemi önce `green-app` konteynerini ayağa kaldırır ve `/health` gibi bir uç noktadan kontrol eder. Ardından upstream içindeki aktif hedef değiştirilir ve Nginx yeniden yüklenir. Gerçek projelerde bunu elle düzenlemek yerine Kubernetes Service seçicileri, AWS ALB target group'ları veya bir servis mesh ile otomatikleştirmek daha doğrudur.

## En kritik konu: veritabanı

Blue-Green yalnızca uygulama katmanında kolaydır. Yeni sürüm veritabanı şemasını eski sürümün anlayamayacağı biçimde değiştirirse hızlı rollback tehlikeye girer. Bu nedenle **expand-contract** yaklaşımı kullanılır: önce geriye uyumlu kolon veya tablo eklenir, uygulama iki yapıyı da okuyabilir hâle getirilir, eski sürüm devreden çıktıktan sonra kullanılmayan alanlar kaldırılır.

Başarıyı yalnızca HTTP 200 oranıyla ölçmeyin. Geçiş öncesi ve sonrası hata oranını, p95 gecikmesini ve iş metriklerini karşılaştırın. Örneğin hata bütçesinin basit bir görünümü şöyledir:

$$Hata\ Oranı = \frac{Basarisiz\ Istekler}{Toplam\ Istekler} \times 100$$

Blue-Green Deployment; ödeme, e-ticaret ve kritik API'ler gibi geri dönüş süresinin önemli olduğu sistemlerde özellikle değerlidir. Karşılığında çift ortam maliyeti ve dikkatli veri migrasyonu disiplini ister. Doğru otomasyon, sağlık kontrolleri ve gözlemlenebilirlikle birleştiğinde ise sürüm günü heyecanını, kontrollü bir trafik yönlendirme işlemine dönüştürür.
