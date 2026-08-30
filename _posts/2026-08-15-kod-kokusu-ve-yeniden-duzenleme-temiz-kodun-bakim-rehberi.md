---
layout: post
title: "Kod Kokusu ve Yeniden Düzenleme: Temiz Kodun Bakım Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - kod kokusu
  - refactoring
  - temiz kod
toc: true
image: /img/kod-kokusu-ve-24.png
---

Bir yazılım ilk gününde pırıl pırıl görünebilir; asıl sınavı ise üçüncü özellik isteği, acil hata düzeltmesi ve ekip değişikliği geldiğinde verir. Kod kokuları, programın mutlaka hatalı olduğunu değil, tasarımın gelecekte pahalılaşabileceğini söyleyen uyarı işaretleridir. Yeniden düzenleme (refactoring), dışarıdan gözlemlenen davranışı değiştirmeden bu iç yapıyı iyileştirme disiplinidir. Amaç daha kısa kod yazmak değil; değişime daha güvenle cevap verebilen kod üretmektir.
``

## Kod kokusu neden önemlidir?

Bakım maliyeti yalnızca satır sayısıyla ölçülmez. Bir değişikliğin etkilediği modül sayısı, kodun anlaşılması için gereken zihinsel yük ve test eksikliği maliyeti büyütür. Basit bir düşünce modeliyle bakım riskini şöyle ifade edebiliriz:

$$R \approx C \times B \times (1 - T)$$

Burada $C$ bağımlılık karmaşıklığını, $B$ değişiklik kapsamını, $T$ ise test güvenini temsil eder. Test oranı yükseldikçe risk azalır; ancak yoğun bağımlılık ve devasa sınıflar bu kazancı hızla tüketebilir. Kod kokusu, bu değişkenlerden birinin kontrol dışına çıkmaya başladığını haber verir.

| Kod kokusu | Tipik belirti | Olası sonuç | Yaygın iyileştirme |
|---|---|---|---|
| Uzun metot | Bir metot hem doğrular hem hesaplar hem kaydeder | Okuma ve test zorluğu | Extract Method |
| Yinelenen kod | Aynı koşullar farklı dosyalarda yaşar | Tutarsız düzeltmeler | Extract Method / ortak soyutlama |
| Büyük sınıf | Tek sınıf birçok iş sorumluluğu taşır | Yüksek bağlılık | Extract Class |
| Uzun parametre listesi | Çağrıda 5-6 değer taşınır | Yanlış sıra, düşük okunabilirlik | Parameter Object |
| Özellik kıskançlığı | Metot sürekli başka nesnenin verisini kullanır | Yanlış sorumluluk dağılımı | Move Method |

![kod-kokusu-ve-24](/img/kod-kokusu-ve-24.svg)


## Kokuyu teşhis etmek: “çalışıyor” yeterli değildir

Örneğin aşağıdaki metot çalışır; fakat indirim hesabı, kargo kuralı ve veritabanı işlemini tek yerde toplar. Bu durum Tek Sorumluluk İlkesi'ni zorlar. Bir kural değiştiğinde metodu değiştirme olasılığı artar. Bir sınıfın değişme nedeni sayısı $n$ ise, ideal hedef genellikle $n \rightarrow 1$ yönünde ilerlemektir.

```javascript
function tamamla(sepet, kullanici, db) {
  let toplam = sepet.reduce((sum, urun) => sum + urun.fiyat, 0);

  if (kullanici.premium) toplam *= 0.9;
  if (toplam < 500) toplam += 49.9;

  db.orders.insert({ kullaniciId: kullanici.id, toplam });
  return toplam;
}
```

Bu koddaki sorun matematiksel işlem değildir; farklı politika ve altyapı ayrıntılarının birbirine yapışmasıdır. Önce güvenlik ağı kurulur: mevcut davranışı kapsayan testler yazılır. Ardından küçük, geri alınabilir adımlarla ayrıştırma yapılır.

```javascript
function urunToplami(sepet) {
  return sepet.reduce((sum, urun) => sum + urun.fiyat, 0);
}

function indirimliTutar(tutar, kullanici) {
  return kullanici.premium ? tutar * 0.9 : tutar;
}

function kargoEkle(tutar) {
  return tutar < 500 ? tutar + 49.9 : tutar;
}

function tamamla(sepet, kullanici, siparisDeposu) {
  const toplam = kargoEkle(indirimliTutar(urunToplami(sepet), kullanici));
  siparisDeposu.kaydet({ kullaniciId: kullanici.id, toplam });
  return toplam;
}
```

Burada `Extract Method` uygulanmıştır. Hesaplama parçaları tek başına test edilebilir, isimleri niyeti açıklar ve kargo kuralı değiştiğinde veritabanı koduna dokunmak gerekmez. Yine de aşırı parçalamaktan kaçının: üç satırlık, yalnızca bir kez kullanılan ve anlam katmayan metotlar kodun akışını gizleyebilir.

## Güvenli refactoring döngüsü

Yeniden düzenleme bir “büyük temizlik günü” değil, sürekli bir alışkanlıktır. En güvenli döngü şudur: küçük kokuyu seç, karakterizasyon testiyle mevcut davranışı sabitle, tek dönüşüm uygula, testleri çalıştır ve değişikliği gözden geçir. Her adımda sistemin davranışı korunmalıdır. Derleyicinin, linter'ın ve otomatik testlerin yeşil kalması; refactoring'in emniyet kemeridir.

Önceliklendirme yaparken en çirkin koddan değil, en sık değişen ve hata maliyeti yüksek bölgeden başlayın. Kod kokuları mahkeme kararı değil, tartışma davetidir. Doğru bağlamda uzun bir metot kabul edilebilir; fakat değişiklik korkusu oluştuysa kod size çoktan bir şey anlatmaya başlamıştır.
