---
layout: post
title: "Çevik Metodolojilerin İllüzyonu: Scrum Mikro-Yönetimin Yeni Adı mı?"
math: true
categories: 
  - Bilgi
tags: 
  - agile
  - scrum
  - mikro-yönetim
  - yazılım geliştirme
  - takım kültürü
  - proje yönetimi
toc: true
image: /img/cevik-metodolojilerin-illuzyonu-34.png
---

Agile, uzun planların ve ağır onay mekanizmalarının yerine esneklik, iş birliği ve otonomi getirme vaadiyle doğdu. Ne var ki bazı şirketlerde bu fikir; günlük sorgular, saatlik performans takibi ve geliştiricileri yarıştıran puan tablolarıyla bambaşka bir şeye dönüşüyor. Böyle ortamlarda Scrum, çevikliği sağlayan bir çerçeve olmaktan çıkıp takımın üzerine giydirilmiş renkli bir mikro-yönetim kostümüne benzeyebiliyor.

``

## Sorun Agile mı, uygulama biçimi mi?

Agile Manifesto süreçlerden çok insanları, kapsamlı dokümantasyondan çok çalışan yazılımı ve değişmez planlardan çok değişime yanıt vermeyi önemser. Scrum ise bu değerleri hayata geçirmek için roller, etkinlikler ve geri bildirim döngüleri sunan bir çerçevedir. Teoride amaç, yöneticinin takımı daha yakından izlemesi değil; takımın kendi çalışma biçimini görünür kılarak iyileştirmesidir.

Kırılma noktası, görünürlüğün denetime dönüştüğü yerde ortaya çıkar. Sprint panosu geliştiricinin işini düzenlemesine değil de yöneticinin “Kim kaç kart kapattı?” sorusuna hizmet ediyorsa araç ile amaç yer değiştirmiştir.

| Sağlıklı çeviklik | Çevik görünümlü mikro-yönetim |
|---|---|
| Daily, takımın koordinasyonu içindir | Daily, yöneticiye hesap verme toplantısıdır |
| Tahminler planlama amacı taşır | Story point performans puanı sayılır |
| Takım işi nasıl yapacağına karar verir | Yönetici görevleri kişilere dağıtır |
| Retrospektif güvenli öğrenme alanıdır | Retrospektif suçlu arama seansıdır |
| Hata, süreç hakkında veri sağlar | Hata, bireysel başarısızlık kabul edilir |

![cevik-metodolojilerin-illuzyonu-34](/img/cevik-metodolojilerin-illuzyonu-34.svg)


## Ölçümler nasıl tuzağa dönüşür?

Story point, işin göreli karmaşıklığını ve belirsizliğini tahmin etmek için kullanılabilir. Saat değildir, evrensel bir üretkenlik birimi hiç değildir. A takımının 30 puanı ile B takımının 50 puanını karşılaştırmak, iki farklı termometreyle ölçülen değerleri yarıştırmaya benzer.

Basit bir çeviklik modeli şöyle düşünülebilir:

$$B = O / (C + W)$$

Burada $B$ gerçek çevikliği, $O$ takım otonomisini, $C$ koordinasyon maliyetini ve $W$ gereksiz izleme yükünü temsil eder. Toplantılar ve raporlar arttıkça payda büyür. Otonomi aynı kalırsa organizasyon daha fazla Scrum etkinliği yapmasına rağmen daha az çevik hâle gelebilir.

Ölçümün hedefe dönüşmesi Goodhart Yasası’nı da devreye sokar: “Bir ölçüt hedef olduğunda iyi bir ölçüt olmaktan çıkar.” Geliştiriciler puanla değerlendiriliyorsa kartlar yapay biçimde büyütülebilir, kolay işler tercih edilebilir veya teknik borç görünmez hâle getirilebilir. Gösterge paneli yeşildir; ürün ise usulca duman çıkarmaktadır.

Aşağıdaki örnek, tek başına velocity yerine daha dengeli sinyaller üretir:

```python
def takim_sinyali(teslimat, hata, bekleme, memnuniyet):
    # Yüksek teslimat kadar kaliteyi ve takım deneyimini de önemser.
    kalite = teslimat / max(1, hata)
    akis = 1 / max(1, bekleme)
    return round(kalite * akis * memnuniyet, 2)

sonuc = takim_sinyali(18, 3, 2, 0.85)
print(sonuc)
```

Bu kod gerçek hayatta kullanılacak kusursuz bir performans formülü değildir. Tam tersine, tek boyutlu ölçümlerin yetersizliğini gösterir. Teslimat sayısı yükselirken hata, bekleme süresi veya takım memnuniyeti kötüleşiyorsa “başarı” ilan etmek erkendir. Ayrıca bu tür sonuçlar bireyleri sıralamak için değil, sistemde konuşulması gereken sorunları keşfetmek için kullanılmalıdır.

## Daily toplantısı küçük bir mahkeme olmamalı

“Dün ne yaptın, bugün ne yapacaksın?” kalıbı yanlış tonla kullanıldığında yoklamaya dönüşebilir. Sağlıklı bir daily daha çok “Hedefe ulaşmamızı ne engelliyor ve bugün nasıl birlikte ilerleyeceğiz?” sorusuna odaklanır. Scrum Master da takım polisi değil, engelleri kaldıran ve öz yönetimi koruyan kolaylaştırıcıdır.

Bir organizasyon kendini değerlendirmek için şu soruları sorabilir:

- Geliştiriciler teknik kararları gerçekten verebiliyor mu?
- Tahminler son tarih baskısının bahanesi olarak mı kullanılıyor?
- Retrospektifte yöneticiler olmadan rahatça konuşulabiliyor mu?
- Ölçümler insanları değerlendirmek için mi, sistemi iyileştirmek için mi tutuluyor?
- Sprint hedefi mi önemli, yoksa herkesin sürekli meşgul görünmesi mi?

Agile’ın illüzyonu, ritüelleri uygulayınca otomatik olarak çevik olunacağı inancıdır. Daily yapmak, Jira kullanmak ve sprintlere isim vermek kolaydır; güven inşa etmek ve karar yetkisini takıma bırakmak zordur. Scrum mikro-yönetimin yeni adı olmak zorunda değildir. Fakat otonomi yoksa Scrum kelimeleri, eski kontrol kültürünün üzerine yapıştırılmış modern etiketlerden ibaret kalır.
