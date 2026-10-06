---
layout: post
title: "Açık Kaynak Ticket Destek Sistemleri: Zammad, osTicket ve FreeScout Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - ticket
  - zammad
  - osticket
  - freescout
  - müşteri-desteği
  - açık-kaynak
toc: true
image: /img/acik-kaynak-ticket-22.png
---

Müşteri e-postaları kişisel gelen kutularında kayboluyor, aynı soruya üç çalışan birden cevap veriyor ve “Bu talep kimdeydi?” cümlesi ofisin sloganına dönüşüyorsa bir ticket destek sistemine ihtiyacınız var demektir. Zammad, osTicket ve FreeScout; talepleri merkezi bir yerde toplamak isteyen ekipler için öne çıkan açık kaynak çözümlerdir. Ancak benzer görünseler de kullanım deneyimi, teknik gereksinimler ve hedefledikleri ekipler bakımından önemli farklara sahiptir.
``
## Ticket sistemi nasıl çalışır?

Ticket sistemi; e-posta, web formu, telefon veya sosyal medya üzerinden gelen müşteri taleplerini benzersiz bir kayıt altında toplar. Her kaydın durumu, önceliği, sorumlusu ve işlem geçmişi bulunur. Böylece sıradan bir e-posta, takip edilebilir bir iş birimine dönüşür.

Bir destek masasının temel performansı şu basit oranla düşünülebilir:

$$
\text{Çözüm Oranı} = \frac{\text{Çözülen Ticket Sayısı}}{\text{Toplam Ticket Sayısı}} \times 100
$$

Bunun yanında ilk yanıt süresi ve ortalama çözüm süresi de önemlidir. Örneğin ortalama çözüm süresi:

$$
T_{ortalama} = \frac{\sum_{i=1}^{n} T_i}{n}
$$

şeklinde hesaplanır. İyi bir yazılım yalnızca mesajları saklamaz; bu metrikleri görünür kılarak darboğazları keşfetmenizi sağlar.

## Üç adayın karakteri

| Özellik | Zammad | osTicket | FreeScout |
|---|---|---|---|
| Kullanıcı deneyimi | Modern ve kapsamlı | Geleneksel ve işlevsel | E-posta kutusu kadar sade |
| Kurulum yükü | Orta-yüksek | Orta | Düşük-orta |
| Çoklu kanal | Güçlü | Temel/orta | Modüllere bağlı |
| Otomasyon | Gelişmiş | Kurallar ve filtreler | Daha sınırlı |
| Kaynak ihtiyacı | Görece yüksek | Orta | Düşük |
| Uygun ekip | Orta ve büyük ekipler | Klasik destek masaları | Küçük ve çevik ekipler |

![acik-kaynak-ticket-22](/img/acik-kaynak-ticket-22.svg)


### Zammad: Kontrol panelini sevenlere

Zammad; e-posta, telefon, sohbet ve çeşitli sosyal kanalları tek arayüzde birleştirebilir. Etiketler, roller, SLA kuralları, detaylı arama ve otomasyon seçenekleri güçlüdür. Arayüzü modern olsa da arka planda Elasticsearch gibi ek bileşenler kullanabildiği için sunucu ihtiyacı rakiplerinden daha yüksektir.

Karmaşık iş akışları bulunan, birden fazla departmanın aynı sistemi kullandığı yapılarda iyi sonuç verir. Buna karşılık yalnızca iki kişinin e-posta yanıtladığı küçük bir ekip için biraz “alışverişe tankla gitmek” olabilir.

### osTicket: Eski ama güvenilir usta

osTicket uzun süredir kullanılan, PHP tabanlı ve oldukça tanınmış bir çözümdür. Web formları, e-posta yönlendirme, departmanlar, hazır yanıtlar ve ticket filtreleri sunar. Görsel açıdan en heyecan verici seçenek değildir; fakat klasik yardım masası ihtiyaçlarını tahmin edilebilir biçimde karşılar.

PHP ve MySQL destekleyen standart barındırma ortamlarında çalışabilmesi önemli avantajdır. Kurumunuz “sürpriz istemiyorum, ticket açılsın ve doğru departmana gitsin” diyorsa osTicket mantıklı bir tercihtir.

### FreeScout: Paylaşımlı gelen kutusunun süper hâli

FreeScout, Help Scout benzeri sade bir deneyim sunan Laravel tabanlı bir uygulamadır. Kullanıcılar karmaşık ticket ekranları yerine alışık oldukları e-posta görünümüyle çalışır. Hafiftir ve küçük sunucularda rahatça işletilebilir.

Temel sürüm açık kaynak olsa da bazı gelişmiş özellikler ücretli modüllerle sağlanır. Bu nedenle ilk kurulum maliyeti düşük görünse bile ihtiyaç duyulacak modülleri önceden listelemek gerekir.

## Basit bir dağıtım örneği

FreeScout gibi PHP tabanlı bir sistemi ters proxy arkasında yayınlamak için Nginx tarafında aşağıdaki yönlendirme kullanılabilir:

```nginx
server {
    listen 80;
    server_name destek.example.com;

    location / {
        proxy_pass http://freescout:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Bu yapı, `destek.example.com` adresine gelen istekleri uygulama konteynerine aktarır. Gerçek kullanımda HTTPS sertifikası, düzenli veritabanı yedeği ve SMTP ayarları mutlaka eklenmelidir.

## Hangisini seçmeli?

Gelişmiş otomasyon, çoklu kanal ve ayrıntılı raporlama gerekiyorsa **Zammad** öne çıkar. Geleneksel, kararlı ve yaygın sunucularla uyumlu bir yardım masası aranıyorsa **osTicket** güçlü bir adaydır. Küçük ekip, sade arayüz ve paylaşımlı e-posta deneyimi öncelikliyse **FreeScout** daha hızlı benimsenir.

Son kararı özellik sayısına göre değil; günlük ticket hacmi, ekip büyüklüğü, sunucu kapasitesi ve bakım becerisine göre verin. En iyi destek sistemi, en uzun özellik listesini sunan değil, ekibin gerçekten düzenli kullandığı sistemdir.
