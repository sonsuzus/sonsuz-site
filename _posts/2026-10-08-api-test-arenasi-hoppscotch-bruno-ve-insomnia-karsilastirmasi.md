---
layout: post
title: "API Test Arenası: Hoppscotch, Bruno ve Insomnia Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - api
  - hoppscotch
  - bruno
  - insomnia
  - rest
  - yazılım-testi
toc: true
image: /img/api-test-arenasi-95.png
---

Bir API geliştirirken yalnızca endpoint’in çalışması yetmez; doğru durum kodunu, beklenen veriyi ve kabul edilebilir sürede yanıt verdiğini de doğrulamak gerekir. Postman dışında bir araç arıyorsanız Hoppscotch, Bruno ve Insomnia oldukça güçlü üç adaydır. Üstelik her biri API testine farklı bir pencereden bakar: biri hızlı ve web tabanlı, biri Git dostu, diğeri ise kapsamlı bir masaüstü çalışma alanıdır.


![api-test-arenasi-95](/img/api-test-arenasi-95.svg)

``

## API testi aslında neyi doğrular?

Bir istemci API’ye HTTP isteği gönderir; sunucu ise durum kodu, başlıklar ve gövde içeren bir yanıt üretir. Test aracının temel görevi bu alışverişi görünür ve tekrar edilebilir hâle getirmektir.

Örneğin bir kullanıcı endpoint’i için yalnızca `200 OK` almak yeterli değildir. Yanıt gövdesindeki `id` alanının bulunması, içerik türünün JSON olması ve sürenin belirlenen sınırı aşmaması da kontrol edilmelidir.

Performansı basitçe şöyle değerlendirebiliriz:

$$T_{toplam} = T_{ağ} + T_{sunucu} + T_{aktarım}$$

Bir test 400 ms sürüyorsa bunun tamamı sunucunun işlem süresi değildir. Ağ gecikmesi ve yanıt boyutu da sonucu etkiler. Çoklu isteklerde ortalama süre ise

$$\bar{T} = \frac{\sum_{i=1}^{n} T_i}{n}$$

formülüyle hesaplanabilir. Bu nedenle tek bir hızlı yanıt görüp zafer dansına başlamak yerine testi birkaç kez çalıştırmak daha sağlıklıdır.

## Üç aracın karakteri

| Özellik | Hoppscotch | Bruno | Insomnia |
|---|---|---|---|
| Çalışma biçimi | Web ve masaüstü | Masaüstü ve CLI | Masaüstü |
| Başlangıç hızı | Çok yüksek | Yüksek | Orta |
| Git uyumu | Sınırlı | Çok güçlü | Projeye göre değişir |
| Yerel dosya yaklaşımı | İkincil | Temel özellik | Kısmen |
| Otomasyon | Temel/orta | CLI ile güçlü | Eklenti ve CLI seçenekleri |
| İdeal kullanıcı | Hızlı deneme yapanlar | Kod odaklı ekipler | Geniş çalışma alanı isteyenler |

### Hoppscotch: Tarayıcıyı aç ve isteği gönder

Hoppscotch, kurulumla uğraşmadan REST, GraphQL ve WebSocket istekleri denemek isteyenler için idealdir. Arayüzü hafiftir; URL’yi, metodu ve gerekli başlıkları girerek saniyeler içinde sonuç alabilirsiniz. Özellikle eğitimlerde, hata ayıklamada ve geçici kontrollerde parıldar.

Ancak hassas token’larla çalışırken ekip politikalarını ve verinin nerede saklandığını incelemek gerekir. Tarayıcı kolaylığı, güvenlik değerlendirmesini ortadan kaldırmaz.

### Bruno: Koleksiyonlar da kod gibi yaşasın

Bruno, koleksiyonları düz metin dosyalarında saklayarak Git üzerinden sürümlemeyi kolaylaştırır. Böylece API değişiklikleri pull request içinde görülebilir; “Bu header’ı kim değiştirdi?” sorusu polisiye romana dönüşmez.

Örnek bir Bruno isteği şöyle görünebilir:

{% raw %}
```bru
meta {
  name: Kullanıcı Getir
  type: http
  seq: 1
}

get {
  url: {{baseUrl}}/users/42
  body: none
  auth: bearer
}

assert {
  res.status: eq 200
  res.body.id: eq 42
}
```
{% endraw %}

Bu dosya isteğin adresini tanımlar ve yanıtın durum koduyla kullanıcı kimliğini doğrular. CLI desteği sayesinde aynı koleksiyon CI/CD hattında da çalıştırılabilir.

### Insomnia: Düzenli ve kapsamlı çalışma masası

Insomnia; ortam değişkenleri, kimlik doğrulama yöntemleri, GraphQL desteği ve koleksiyon organizasyonuyla kapsamlı projelerde rahat bir deneyim sunar. Çok sayıda servisi olan ekipler için klasörlü yapı ve yeniden kullanılabilir değişkenler önemlidir.

Örneğin geliştirme ve üretim adreslerini ayrı ayrı yazmak yerine şu mantık kullanılabilir:

{% raw %}
```json
{
  "base_url": "https://api.example.com",
  "token": "{{ secret_token }}"
}
```
{% endraw %}

Böylece isteklerde `{{ base_url }}` kullanılır ve ortam değiştirirken her endpoint’i elle düzenlemek gerekmez. Token değerlerini repoya eklememek ise temel güvenlik kuralıdır.

## Hangisini seçmelisiniz?

Hızlı, kurulumsuz denemeler için **Hoppscotch**; koleksiyonları Git ile yönetmek ve testleri pipeline’a taşımak için **Bruno**; kapsamlı masaüstü deneyimi ve düzenli proje yönetimi için **Insomnia** öne çıkar. En iyi araç, en fazla düğmeye sahip olan değil, ekibinizin testleri düzenli çalıştırmasını sağlayandır. Küçük bir örnek API’yi üçünde de deneyin; ardından hız, paylaşım, güvenlik ve otomasyon ihtiyaçlarınıza göre karar verin.
