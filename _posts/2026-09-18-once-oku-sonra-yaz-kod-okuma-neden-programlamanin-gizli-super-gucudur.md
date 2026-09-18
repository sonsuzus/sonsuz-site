---
layout: post
title: "Önce Oku, Sonra Yaz: Kod Okuma Neden Programlamanın Gizli Süper Gücüdür?"
math: true
categories: 
  - Bilgi
tags: 
  - kod okuma
  - programlama
  - yazılım geliştirme
  - temiz kod
  - öğrenme
  - kod inceleme
toc: true
---

Programlama öğrenirken verilen ilk öğüt genellikle “Bol bol kod yaz” olur. Elbette klavyeyle arayı iyi tutmak önemlidir; fakat yalnızca kod yazarak ilerlemek, konuşmayı öğrenmek için sürekli monolog yapmaya benzer. Başkalarının kodlarını okumak ise farklı kelimeleri, anlatım biçimlerini ve problem çözme yollarını görmemizi sağlar. Bu nedenle kod okumanın kod yazmaktan önce gelmesi gerektiği fikri, tartışılmayı hak eden güçlü bir yaklaşımdır.

``

## Kod okumak neden farklı bir beceridir?

Kod yazarken zihnimizdeki çözümü bilgisayarın anlayacağı bir biçime dönüştürürüz. Kod okurken bunun tersini yaparız: Karşımızdaki sembollerden yazarın niyetini çıkarmaya çalışırız. Bu iki süreç kabaca şöyle gösterilebilir:

$$
Yazma: Niyet \rightarrow Algoritma \rightarrow Kod
$$

$$
Okuma: Kod \rightarrow Algoritma \rightarrow Niyet
$$

İkinci yol çoğu zaman daha zordur; çünkü değişken adları kötü olabilir, bağlam eksik olabilir veya yıllar önce verilmiş teknik kararlarla karşılaşabiliriz. Gerçek yazılım projelerinde geliştiricilerin zamanının önemli bölümü sıfırdan kod üretmek yerine mevcut kodu anlamaya ayrılır. Yani iş hayatındaki programcı, yalnızca bir “yazar” değil, aynı zamanda dikkatli bir dedektiftir.

| Kod yazma odaklı öğrenme | Kod okuma odaklı öğrenme |
|---|---|
| Kendi çözüm alışkanlıklarını pekiştirir | Alternatif çözümleri gösterir |
| Hızlı üretim hissi verir | Analiz ve sabır geliştirir |
| Hataları deneyerek öğretir | Hataları önceden tanımayı öğretir |
| Sözdizimine ağırlık verir | Tasarım ve niyete ağırlık verir |

## Küçük bir okuma deneyi

Aşağıdaki JavaScript fonksiyonuna bakalım:

```javascript
function calculateTotal(items) {
  return items
    .filter(item => item.active)
    .reduce((total, item) => total + item.price, 0);
}
```

Bu kodu hemen çalıştırmak yerine satır satır okuyalım. Fonksiyon bir ürün listesi alıyor, yalnızca `active` değeri doğru olanları seçiyor ve fiyatlarını topluyor. `filter` veri kümesini daraltırken `reduce` kalan elemanları tek bir sayıya indiriyor. Kodun yaptığı işlem matematiksel olarak şöyle ifade edilebilir:

$$
T = \sum_{i=1}^{n} a_i p_i
$$

Burada $a_i$, ürün aktifse $1$, değilse $0$; $p_i$ ise ürünün fiyatıdır. Böyle bir okuma, yalnızca fonksiyonların adını ezberletmez. Veri akışını ve işlemlerin neden bu sırayla yapıldığını da öğretir.

Şimdi aynı işin daha kapalı yazılmış hâlini düşünelim:

```javascript
function x(a) {
  return a.reduce((s, v) => v.active ? s + v.price : s, 0);
}
```

İkinci sürüm daha kısa olabilir, ancak ilk bakışta anlaşılması daha zordur. Kod okuyarak “az satır” ile “iyi kod” kavramlarının aynı olmadığını keşfederiz. Okunabilirlik, gelecekteki geliştiricilere bırakılan teknik bir nezakettir.

## Peki gerçekten önce mi gelmeli?

Kod okumayı tamamen kod yazmanın önüne koymak da kusursuz bir yöntem değildir. Yüzme kitapları okuyarak yüzücü olunamayacağı gibi, yalnızca depo gezerek programcı olunmaz. En verimli model döngüseldir:

1. Küçük bir kod parçasını oku.
2. Ne yaptığını kendi cümlelerinle açıkla.
3. Kodu çalıştır ve tahminini sınamaya çalış.
4. Aynı çözümü kendin yeniden yaz.
5. İki sürümü karşılaştır.

Bu yaklaşımı basitçe $Öğrenme = Okuma + Uygulama + GeriBildirim$ biçiminde düşünebiliriz. Bileşenlerden biri eksildiğinde öğrenme yüzeysel kalır.

## Kod okuma kası nasıl geliştirilir?

Başlangıçta devasa açık kaynak projelerine dalmak yerine küçük kütüphaneler, örnek uygulamalar ve test dosyaları seçilmelidir. Fonksiyonun adına bakıp sonucunu tahmin etmek, değişkenlerin izini kâğıt üzerinde sürmek ve anlaşılmayan satırlara yorum eklemek oldukça etkilidir. Git geçmişini incelemek de kodun yalnızca nasıl çalıştığını değil, neden değiştirildiğini gösterir.

Sonuç olarak kod okumak, kod yazmanın rakibi değildir; onun hazırlık sahasıdır. İyi metinler okumadan güçlü bir yazar olmak ne kadar zorsa, farklı kod tabanlarını incelemeden olgun bir geliştirici olmak da o kadar zordur. Klavyeye koşmadan önce birkaç dakika durup kodu dinlemek, uzun vadede daha hızlı ve daha bilinçli yazmamızı sağlar.
