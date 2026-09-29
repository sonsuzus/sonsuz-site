---
layout: post
title: "Mikroservislerde Strangler Fig Pattern: Monoliti Adım Adım Dönüştürmek"
math: true
categories: 
  - Bilgi
tags: 
  - mikroservis
  - strangler-fig
  - monolit
  - yazılım-mimarisi
  - refactoring
  - devops
toc: true
image: /img/mikroservislerde-strangler-fig-38.png
---

![mikroservislerde-strangler-fig-38](/img/mikroservislerde-strangler-fig-38.svg)


Yıllardır çalışan bir monoliti tek gecede mikroservislere dönüştürmek, uçuş hâlindeki bir uçağın motorunu değiştirmeye benzer: Teorik olarak mümkündür, fakat kimse gönüllü olarak içinde oturmak istemez. **Strangler Fig Pattern**, büyük ve riskli bir yeniden yazım yerine eski sistemin işlevlerini küçük parçalar hâlinde yeni servislere taşıyarak kontrollü bir dönüşüm sağlar.
``

## Strangler Fig Pattern nedir?

Desen adını, bir ağacın çevresinde büyüyerek zamanla onun yerini alan strangler fig bitkisinden alır. Yazılım dünyasında “ağaç” monolitik uygulama, onu saran yeni yapı ise mikroservislerdir. Monolit aniden kapatılmaz; belirli yetenekleri yeni servislere aktarıldıkça sorumluluk alanı küçülür.

Yaklaşım üç temel aşamaya dayanır:

1. **Tanımla:** Monolit içindeki ayrıştırılabilir iş yeteneklerini belirle.
2. **Yönlendir:** İstekleri bir proxy veya API Gateway üzerinden eski ya da yeni sisteme gönder.
3. **Değiştir:** Yeni servis kararlı hâle geldiğinde monolitteki eski modülü devreden çıkar.

Bu yöntem riski zamana yayar. Basitleştirilmiş biçimde toplam geçiş riskini şöyle düşünebiliriz:

$$R_{toplam} = \sum_{i=1}^{n} P_i \times E_i$$

Burada $P_i$, bir geçiş adımının hata olasılığını; $E_i$ ise hatanın etkisini temsil eder. Küçük adımlar genellikle etki alanını daralttığı için tek seferlik “big bang” dönüşümünden daha yönetilebilirdir.

| Özellik | Baştan yeniden yazım | Strangler Fig |
|---|---|---|
| Teslimat süresi | Uzun süre sonuç üretmeyebilir | Her adım değer üretebilir |
| Geri dönüş | Zor ve pahalı | Servis bazında kolay |
| Risk | Tek noktada yoğunlaşır | Küçük parçalara dağılır |
| Eski sistem | Son güne kadar merkezde | Zamanla küçülür |
| Operasyon | Başlangıçta daha sade | Geçişte daha karmaşık |

## İlk servis nasıl seçilir?

İlk aday, ne sistemin kalbi kadar kritik ne de hiçbir şey öğretmeyecek kadar önemsiz olmalıdır. Bildirim gönderme, ürün kataloğu veya raporlama gibi sınırları belirgin modüller iyi başlangıç noktalarıdır. Ödeme sistemiyle başlamak ise yüzme öğrenirken okyanusa atlamaya benzeyebilir.

Önceliklendirme için basit bir puan kullanılabilir:

$$Öncelik = \frac{İş\ Değeri \times Ayrıştırılabilirlik}{Teknik\ Risk + Bağımlılık}$$

Yüksek iş değeri ve düşük bağımlılık, güçlü bir aday anlamına gelir. Bununla birlikte kod yapısından önce **domain sınırları** incelenmelidir. Domain-Driven Design yaklaşımındaki bounded context kavramı, servis sınırlarını belirlemek için yararlıdır.

## Trafiği yeni servise yönlendirmek

İstemcilerin hangi sistemin eski, hangisinin yeni olduğunu bilmemesi gerekir. Bu ayrımı API Gateway veya ters proxy yapabilir. Örneğin aşağıdaki Nginx yapılandırması ürün isteklerini yeni servise, diğer trafiği monolite yollar:

```nginx
location /api/products/ {
    proxy_pass http://product-service:8080/;
}

location / {
    proxy_pass http://legacy-monolith:8080/;
}
```

Bu katman yalnızca yönlendirme yapmaz; kademeli yayın, kimlik doğrulama, oran sınırlama ve gözlemlenebilirlik de sağlayabilir. İlk aşamada trafiğin yalnızca yüzde 5’i yeni servise gönderilerek hata oranları karşılaştırılabilir.

## Veri meselesi: Asıl düğüm burada

Kodu ayırmak kolay, ortak veritabanını ayırmak zordur. Yeni servisin doğrudan monolit tablolarına sürekli erişmesi, görünmez bir dağıtık monolit oluşturur. Geçiş sırasında API tabanlı erişim, olay yayınlama veya geçici veri çoğaltma tercih edilebilir.

| Yöntem | Avantaj | Risk |
|---|---|---|
| Ortak veritabanı | Hızlı başlangıç | Güçlü bağımlılık |
| API ile erişim | Net sahiplik | Ek gecikme |
| Olay tabanlı senkronizasyon | Gevşek bağlılık | Eventual consistency |

Eventual consistency kullanılıyorsa idempotency, tekrar deneme ve mesaj sıralaması tasarımın parçası olmalıdır. “Mesaj iki kez gelmez” varsayımı, üretim ortamının sevdiği şakalardan biridir.

## Başarıyı ölçmek ve tuzaklardan kaçınmak

Her taşıma adımında hata oranı, gecikme, işlem hacmi ve iş metrikleri izlenmelidir. Dağıtık tracing ve merkezi loglama olmadan sorun aramak samanlıkta iğne değil, farklı veri merkezlerine dağılmış iğneler aramaktır.

En yaygın hata, monoliti küçültmeden yalnızca çevresine servis eklemektir. Eski kod kaldırılmıyor, sahiplik belirlenmiyor ve servisler aynı veritabanına bağlanıyorsa sistem dönüşmez; sadece daha karmaşık olur. Her başarılı geçişin sonunda eski endpoint, kod ve tablo bağımlılıkları gerçekten temizlenmelidir.

Strangler Fig Pattern sihirli değnek değil, kontrollü bir modernizasyon stratejisidir. Doğru servis sınırları, ölçülebilir geçişler ve güvenli geri dönüş planlarıyla monolit bir gecede yıkılmaz; işlevlerini sessizce yeni mimariye teslim ederek emekliye ayrılır.
