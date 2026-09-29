---
layout: post
title: "BGP Hijacking: İnternet Trafiğini Kıtalararası Kaçırmak"
math: true
categories: 
  - Bilgi
tags: 
  - bgp
  - ağ güvenliği
  - internet altyapısı
  - siber güvenlik
  - yönlendirme
  - rpki
toc: true
image: /img/bgp-hijacking-internet-50.png
---

Bir web sitesine bağlanırken paketlerinizin en kısa ve güvenilir rotayı izlediğini düşünürsünüz. Oysa internetin omurgasında, ağların birbirine verdiği “Bu adreslere benim üzerimden ulaşabilirsin” sözleri önemli rol oynar. Bu sözlerden biri yanlış veya kötü niyetliyse trafik beklenmedik bir ülkeye sapabilir. İşte **BGP hijacking**, yani BGP rota kaçırma, bu güven ilişkisini hedef alır.
``

## İnternetin mahalleler arası navigasyonu

**Border Gateway Protocol (BGP)**, interneti meydana getiren bağımsız ağlar arasında rota bilgisi taşır. Bu ağların her biri bir **Otonom Sistem** olarak adlandırılır ve bir ASN numarasıyla tanımlanır. İnternet servis sağlayıcıları, bulut şirketleri ve büyük kurumlar kendi otonom sistemlerini işletebilir.

Bir BGP duyurusu kabaca “`203.0.113.0/24` öneğine ASN 64500 üzerinden ulaşılır” der. Yönlendiriciler aldıkları duyuruları politika, yol uzunluğu ve önek özgüllüğü gibi ölçütlerle değerlendirir. Basitleştirilmiş bir maliyet modeli şöyle gösterilebilir:

$$S(r)=w_lL(r)+w_pP(r)+w_oO(r)$$

Burada $L(r)$ AS yol uzunluğunu, $P(r)$ yerel tercihi, $O(r)$ ise diğer politika ölçütlerini temsil eder. Gerçek BGP karar süreci bundan daha ayrıntılıdır; ayrıca “en kısa yol” her zaman fiziksel olarak en kısa mesafe değildir.

| Özellik | Normal BGP duyurusu | Şüpheli duyuru |
|---|---|---|
| Kaynak ASN | Önek sahibiyle uyumlu | Beklenmeyen bir ağ |
| AS yolu | Alışılmış sağlayıcıları içerir | Aniden değişir veya kısalır |
| Önek | Bilinen kapsam | Daha özgül alt önek olabilir |
| Coğrafi rota | Genellikle tutarlı | Trafik başka kıtaya sapabilir |

## Kaçırma neden işe yarıyor?

BGP başlangıçta karşılıklı güvenen az sayıdaki kurum için tasarlanmıştı. Klasik kullanımında bir ağın gerçekten duyurduğu IP aralığının sahibi olduğunu kriptografik olarak kanıtlaması zorunlu değildi. Yanlış yapılandırılmış ya da kötü niyetli bir ağ, başkasına ait öneği ilan edebilir.

BGP’de daha özgül önek çoğunlukla tercih edilir. Örneğin meşru ağ bir `/16` duyururken başka bir ağ bunun içindeki `/24` bloğunu duyurursa ilgili trafik `/24` rotasına yönelebilir. IPv4’te önek büyüklüğü:

$$N=2^{32-p}$$

formülüyle hesaplanır. Buradaki $p$ önek uzunluğudur; `/24` için $N=256$ adrestir. Bu özellik normal trafik mühendisliğinde yararlıdır, fakat sahte duyuruların etkisini de artırabilir.

Kaçırılan trafik saldırgan ağda sonlandırılabilir veya gerçek hedefe aktarılabilir. İkinci durumda kullanıcı bağlantısının çalıştığını görebilirken trafik olağandışı bir güzergâhtan geçer. Şifreleme içerikleri korusa da trafik analizi, kesinti ve yanlış sertifika yapılandırmaları hâlâ risk oluşturur.

## Savunmacı gözle rota değişimini izlemek

Aşağıdaki Python örneği, önceden kaydedilmiş rota gözlemlerinde aynı önek için beklenmeyen kaynak ASN’leri işaretler. Bu kod BGP’ye duyuru göndermez; yalnızca savunma amaçlı günlük analizi yapar.

```python
expected_origins = {
    "203.0.113.0/24": {64500},
    "198.51.100.0/24": {64510, 64511}
}

observations = [
    ("203.0.113.0/24", 64500),
    ("203.0.113.0/24", 64496),
    ("198.51.100.0/24", 64511)
]

for prefix, origin in observations:
    allowed = expected_origins.get(prefix, set())
    if origin not in allowed:
        print(f"UYARI: {prefix} için beklenmeyen origin ASN {origin}")
```

Gerçek sistemlerde yalnızca kaynak ASN’ye bakmak yeterli değildir. AS yolu değişimleri, duyurunun görüldüğü bölge, önek uzunluğu ve olayın süresi birlikte değerlendirilmelidir. Route collector verileri ve küresel ölçüm noktaları bu amaçla kullanılır.

## RPKI: “Bu öneği kim duyurabilir?”

**Resource Public Key Infrastructure (RPKI)**, IP öneği sahibinin hangi ASN’ye duyuru yetkisi verdiğini kriptografik kayıtlarla belirtmesini sağlar. Ağlar **Route Origin Authorization** kayıtları oluşturur; operatörler de **Route Origin Validation** ile rotaları geçerli, geçersiz veya bilinmeyen şeklinde sınıflandırır.

| Savunma | Sağladığı fayda | Sınırı |
|---|---|---|
| RPKI/ROV | Yetkisiz kaynak ASN’yi engeller | AS yolunun tamamını doğrulamaz |
| Rota izleme | Anormallikleri erken bildirir | Tek başına engelleme yapmaz |
| Önek filtreleme | Hatalı duyuruları azaltır | Güncel kayıt gerektirir |
| Çoklu bağlantı | Kesintiye dayanıklılık sağlar | Yanlış politika riski taşır |

BGP hijacking, internetin “merkezsiz ama güvene dayalı” karakterinin çarpıcı sonucudur. Çözüm tek bir güvenlik ürünü değil; RPKI yaygınlığı, dikkatli filtreleme, sürekli izleme ve operatörler arası hızlı koordinasyondur. İnternet kablolarla küreselleşir, fakat doğru rotada kalması ortak sorumlulukla mümkün olur.

![bgp-hijacking-internet-50](/img/bgp-hijacking-internet-50.svg)

