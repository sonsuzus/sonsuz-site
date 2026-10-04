---
layout: post
title: "Yazılım Ekiplerinde Bikeshedding: Düğme Renginde Kaybolmak"
math: true
categories: 
  - Bilgi
tags: 
  - bikeshedding
  - yazılım geliştirme
  - takım dinamikleri
  - teknik kararlar
  - proje yönetimi
  - parkınson yasası
toc: true
image: /img/yazilim-ekiplerinde-bikeshedding-43.png
---

Bir ekip düşünün: Dağıtık veritabanı mimarisi beş dakikada onaylanıyor, fakat yönetim panelindeki düğmenin mavi mi yeşil mi olacağı kırk dakika tartışılıyor. İlk bakışta komik görünen bu durum, yazılım ekiplerinde oldukça yaygın bir örgütsel davranıştır. Adı **bisiklet kulübesi etkisi**, yani *bikeshedding* olan bu eğilim, insanların karmaşık konular yerine kolayca fikir üretebildikleri önemsiz ayrıntılara daha fazla zaman ayırmasını açıklar.

![yazilim-ekiplerinde-bikeshedding-43](/img/yazilim-ekiplerinde-bikeshedding-43.svg)

``

## Kavram nereden geliyor?

Bikeshedding, C. Northcote Parkinson'ın verdiği hayali bir komite örneğine dayanır. Komite, son derece pahalı ve karmaşık bir nükleer reaktörü kısa sürede onaylar. Çünkü üyelerin çoğu konuyu anlayamaz ve bilgisiz görünmemek için sessiz kalır. Ardından çalışanların bisikletleri için yapılacak kulübenin malzemesi tartışılır. Herkes ahşap, boya ve maliyet hakkında fikir yürütebildiğinden toplantı uzar.

Yazılım dünyasındaki karşılığı oldukça tanıdıktır: CAP teoremi, veri tutarlılığı veya bölümlendirme stratejisi sessizlikle karşılanırken isimlendirme, girinti genişliği ya da düğme rengi herkesi bir anda uzman yapar.

Bu davranışı basit bir modelle ifade edebiliriz:

$$
T_d \propto \frac{K}{C}
$$

Burada $T_d$ tartışma süresini, $K$ katılımcıların kendilerini konu hakkında yetkin hissetme düzeyini, $C$ ise konunun gerçek karmaşıklığını temsil eder. Model bilimsel bir yasa değildir; ancak paradoksu güzel özetler: Konu kolaylaştıkça katılım ve yorum sayısı artabilir.

## Neden önemsiz ayrıntılara çekiliyoruz?

Karmaşık bir mimari kararı değerlendirmek bilişsel emek, deneyim ve belirsizlikle mücadele gerektirir. Buna karşılık renk seçmek hızlıdır, somuttur ve kişiye katkıda bulunduğu hissini verir. Ayrıca basit konularda yanlışlanma riski daha düşüktür. “Bu shard stratejisi darboğaz oluşturabilir” demek teknik sorumluluk doğururken “Yeşil daha modern görünüyor” demek neredeyse risksizdir.

| Konu türü | Katılım düzeyi | Hata riski | Tipik sonuç |
|---|---:|---:|---|
| Veritabanı mimarisi | Düşük | Yüksek | Hızlı ve yüzeysel onay |
| API isimlendirmesi | Yüksek | Orta | Uzun yorum zinciri |
| Düğme rengi | Çok yüksek | Düşük | Saatler süren tartışma |

Sorun yalnızca zaman kaybı değildir. Kritik kararlar yeterince sorgulanmaz, uzmanların sesi görünürlük uğruna yapılan yorumlarda kaybolur ve ekipte “çok konuştuk, demek ki iyi karar verdik” yanılsaması oluşur.

## Bikeshedding nasıl azaltılır?

İlk adım, kararları **etki** ve **geri döndürülebilirlik** açısından sınıflandırmaktır. Yüksek etkili ve değiştirilmesi zor kararlar daha fazla inceleme almalıdır. Düşük etkili, kolayca geri alınabilir tercihler ise bir kişiye devredilebilir.

$$
Öncelik = Etki \times GeriDönüşMaliyeti
$$

Örneğin ekip, pull request tartışmalarında küçük yorumları otomatik olarak ayıran basit bir kontrol kullanabilir:

```python
def karar_seviyesi(etki, geri_donus_maliyeti):
    skor = etki * geri_donus_maliyeti
    if skor >= 16:
        return "Mimari inceleme gerekli"
    if skor >= 6:
        return "Kısa ekip değerlendirmesi"
    return "Karar sahibine bırak"

print(karar_seviyesi(5, 4))
```

Bu kod, kararın önemini iki sayısal değişken üzerinden görünür kılar. Elbette insan muhakemesinin yerini tutmaz; amacı her küçük tercihin bütün ekibi meşgul etmesini engelleyen ortak bir dil oluşturmaktır.

Toplantılarda gündem maddelerine süre sınırı koymak, karar sahibini önceden belirlemek ve mimari önerileri yazılı RFC belgeleriyle paylaşmak da faydalıdır. Otomatik biçimlendiriciler, tasarım sistemleri ve kodlama standartları ise tekrar tekrar tartışılan zevk konularını teknik olarak kapatır.

Son olarak ekip üyeleri kendilerine şu soruyu sormalıdır: **Bu yorum ürünün güvenilirliğini, maliyetini veya kullanıcı deneyimini anlamlı biçimde değiştiriyor mu?** Cevap hayırsa düğmeyi şimdilik mavi bırakıp veritabanına dönmenin zamanı gelmiş olabilir.
