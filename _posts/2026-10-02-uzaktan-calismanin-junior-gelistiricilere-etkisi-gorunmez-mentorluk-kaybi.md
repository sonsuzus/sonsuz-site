---
layout: post
title: "Uzaktan Çalışmanın Junior Geliştiricilere Etkisi: Görünmez Mentorluk Kaybı"
math: true
categories: 
  - Bilgi
tags: 
  - uzaktan çalışma
  - junior geliştirici
  - mentorluk
  - yazılım kariyeri
  - kod inceleme
  - takım kültürü
toc: true
image: /img/uzaktan-calismanin-junior-62.png
---

Uzaktan çalışma; esneklik, zaman tasarrufu ve dünyanın herhangi bir yerinden ekibe katılma özgürlüğü sunuyor. Ancak kariyerinin başındaki geliştiriciler için ofisle birlikte kaybolan önemli bir şey var: görünmez mentorluk. Yan masadaki konuşmayı duymak, kıdemli bir geliştiricinin hata ayıklama yaklaşımını izlemek veya öğle arasında teknik bir kararın nedenini sormak, resmi eğitim planlarında görünmeyen güçlü öğrenme fırsatlarıydı.


![uzaktan-calismanin-junior-62](/img/uzaktan-calismanin-junior-62.svg)

``

## Görünmez mentorluk nedir?

Görünmez mentorluk, takvimde toplantısı bulunmayan ve çoğunlukla kendiliğinden gerçekleşen bilgi aktarımıdır. Junior geliştirici yalnızca kendisine verilen cevabı değil; sorunun nasıl tanımlandığını, hangi varsayımların sorgulandığını ve deneyimli kişinin nerede durup düşündüğünü de öğrenir.

Bu öğrenme biçimini basitçe şöyle modelleyebiliriz:

$$
Öğrenme = Resmi\ Eğitim + Gözlem + Geri\ Bildirim + Tesadüfi\ Etkileşim
$$

Uzaktan ekiplerde resmi eğitim ve planlı geri bildirim korunabilir. Fakat gözlem ile tesadüfi etkileşim azalırsa toplam öğrenme hızı da düşer. Sorun, junior geliştiricinin daha az dokümantasyon okuması değil; hangi bilginin önemli olduğunu henüz bilememesidir.

| Öğrenme anı | Ofiste | Uzaktan çalışmada |
|---|---|---|
| Kod okuma | Yan yana, anlık sorularla | Ekran paylaşımı planlanırsa |
| Hata ayıklama | Süreç doğal biçimde izlenir | Genellikle yalnız yapılır |
| Teknik tartışma | Kulak misafiri olunabilir | Yalnızca davetliler katılır |
| Yardım isteme | Düşük sosyal eşik | Mesaj yazma baskısı oluşabilir |
| Geri bildirim | Hızlı ve bağlamsal | Pull request yorumlarına sıkışabilir |

## Sonuç değil, düşünme süreci öğretiyordu

Bir junior aşağıdaki kodu yazdığında kıdemli geliştirici yalnızca düzeltilmiş sürümü paylaşırsa önemli bir öğrenme fırsatı kaybolur:

```javascript
async function getUserName(id) {
  const response = await fetch(`/api/users/${id}`);
  const user = await response.json();
  return user.name;
}
```

Kod mutlu senaryoda çalışır. Fakat deneyimli geliştirici; ağ hatasını, başarısız HTTP durumunu, yanıt biçimini ve iptal mekanizmasını düşünür. Mentorluk, sadece `try/catch` eklemek değil, bu risklerin nasıl fark edildiğini göstermektir:

```javascript
async function getUserName(id, signal) {
  const response = await fetch(`/api/users/${id}`, { signal });

  if (!response.ok) {
    throw new Error(`Kullanıcı alınamadı: ${response.status}`);
  }

  const user = await response.json();
  return user?.name ?? "İsimsiz kullanıcı";
}
```

Bu sürüm HTTP durumunu denetler, isteğin iptal edilebilmesini sağlar ve eksik isim için güvenli bir varsayılan değer üretir. Asıl kazanım ise kod değil, kontrol listesinin junior geliştiricinin zihnine yerleşmesidir.

## Ekran arkasındaki psikolojik eşik

Ofiste “Bir dakikan var mı?” demek kolayken mesaj göndermek daha resmi hissedilebilir. Junior, sorusunun basit görünmesinden çekinir ve gereğinden uzun süre tek başına uğraşır. Bunu yaklaşık bir maliyet modeliyle ifade edebiliriz:

$$
Maliyet = Bekleme\ Süresi \times Belirsizlik + Bağlam\ Değiştirme
$$

Yardım geciktikçe yalnızca görev değil, özgüven de zarar görebilir. Üstelik yönetici ekranda sadece işin geç tamamlandığını görür; öğrenme darboğazını göremez.

## Görünmez mentorluğu yeniden tasarlamak

Uzaktan çalışma junior geliştiriciler için kaçınılmaz biçimde kötü değildir. Fakat organik öğrenmenin yerine bilinçli mekanizmalar kurulmalıdır:

- Haftalık eşli programlama oturumları düzenlenmeli.
- Kıdemli geliştiriciler hata ayıklarken ekran paylaşarak sesli düşünmeli.
- Pull request yorumlarında yalnızca “neyin” değil, “nedenin” açıklanması teşvik edilmeli.
- Junior geliştiricilere soru sormak için düşük baskılı sohbet kanalları sunulmalı.
- Teknik karar toplantıları kaydedilmeli ve kısa karar belgeleri hazırlanmalı.
- Düzenli bire bir görüşmelerde yalnızca çıktı değil, öğrenme engelleri konuşulmalı.

Uzaktan ekiplerin temel yanılgısı, iletişim araçlarının ofisin doğal öğrenme ortamını otomatik olarak taşıdığını sanmaktır. Oysa Slack koridor değildir, görüntülü görüşme de yan yana çalışmanın kendiliğindenliğini tek başına üretemez. Başarılı ekipler görünmez mentorluğun kaybolduğunu kabul eder ve onu görünür, erişilebilir ve sürdürülebilir bir sisteme dönüştürür.
