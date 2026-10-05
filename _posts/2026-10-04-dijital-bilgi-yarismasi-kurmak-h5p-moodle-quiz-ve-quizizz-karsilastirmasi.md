---
layout: post
title: "Dijital Bilgi Yarışması Kurmak: H5P, Moodle Quiz ve Quizizz Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - h5p
  - moodle
  - quizizz
  - e-öğrenme
  - bilgi-yarışması
  - oyunlaştırma
toc: true
image: /img/dijital-bilgi-yarismasi-30.png
---

Bir bilgi yarışması hazırlamak dışarıdan yalnızca birkaç soru yazıp “Başlat” düğmesine basmak gibi görünebilir. Oysa iyi bir quiz sistemi; ölçme kuramı, geri bildirim tasarımı, oyunlaştırma ve teknik entegrasyonun birleşimidir. H5P, Moodle Quiz ve Quizizz aynı hedefe farklı yollardan ulaşır: H5P etkileşimli içerikte, Moodle ayrıntılı değerlendirmede, Quizizz ise canlı ve eğlenceli yarışmalarda öne çıkar.
``

## Önce quiz mantığını anlayalım

Bir quizin temel görevi, kullanıcının verdiği yanıtı önceden tanımlanmış bir değerlendirme kuralıyla karşılaştırmaktır. En basit puan modeli şöyledir:

$$P = \frac{D}{T} \times 100$$

Burada $D$ doğru yanıt sayısını, $T$ toplam soru sayısını ve $P$ başarı yüzdesini gösterir. Ancak yanlış cevapların rastgele işaretlenmesini azaltmak istersek ceza ekleyebiliriz:

$$P = \max\left(0, \frac{D - \lambda Y}{T} \times 100\right)$$

$Y$ yanlış sayısı, $\lambda$ ise yanlış cevap ceza katsayısıdır. Örneğin $\lambda=0.25$ seçilirse dört yanlış bir doğruyu götürür. Platform seçerken yalnızca soru ekranına değil, bu tür puanlama kurallarını destekleyip desteklemediğine de bakılmalıdır.

## Üç platformun karakteri

| Özellik | H5P | Moodle Quiz | Quizizz |
|---|---|---|---|
| Temel yaklaşım | Etkileşimli içerik | Akademik ölçme | Oyunlaştırılmış yarışma |
| Kurulum | Eklenti veya servis | Moodle içinde | Bulut tabanlı |
| Soru çeşitliliği | Yüksek | Çok yüksek | Orta-yüksek |
| Ayrıntılı puanlama | Orta | Çok güçlü | Kolay ve hızlı |
| Canlı yarışma | Sınırlı | Ek araç gerektirebilir | Çok güçlü |
| Raporlama | Entegrasyona bağlı | Ayrıntılı | Görsel ve pratik |
| En uygun kullanım | Ders içeriği | Sınav ve değerlendirme | Sınıf içi etkinlik |

### H5P: İçeriğin içine quiz yerleştirmek

H5P, etkileşimli video, sunum, sürükle-bırak ve dallanan senaryo gibi içerikler üretir. Örneğin öğrenci bir eğitim videosunu izlerken video durdurulup soru gösterilebilir. Böylece değerlendirme, öğrenme sürecinden kopmaz.

H5P’nin güçlü yanı yeniden kullanılabilir içeriklerdir. WordPress, Drupal veya Moodle üzerinde çalışabilir. Buna karşılık ayrıntılı sınav güvenliği ve karmaşık notlandırma gerektiğinde tek başına yeterli olmayabilir.

### Moodle Quiz: Ölçme ve değerlendirme laboratuvarı

Moodle Quiz; soru bankası, kategori, rastgele soru seçimi, süre sınırı, çoklu deneme ve ayrıntılı geri bildirim sunar. Soruların sırası ve seçenekleri karıştırılabilir. Bu nedenle resmi sınavlar veya dönem sonu değerlendirmeleri için güçlüdür.

Ayrıca soru kalitesi, madde güçlüğüyle incelenebilir:

$$G = \frac{N_d}{N}$$

$N_d$ soruyu doğru cevaplayanların, $N$ ise soruyu görenlerin sayısıdır. $G$ değeri 1’e yaklaştıkça soru kolaylaşır. Moodle’ın raporları, “Bu soru neden herkesin kâbusu oldu?” sorusuna veriyle cevap verebilir.

### Quizizz: Yarışma başlasın!

Quizizz; puan tablosu, süre bonusu, avatarlar ve anlık geri bildirimle katılımı yükseltir. Öğrenciler aynı anda yarışabilir veya etkinliği kendi hızlarında tamamlayabilir. Kurulumu hızlıdır; bağlantı ya da katılım kodu paylaşmak çoğu zaman yeterlidir.

Ancak hız bonusu kullanılırken dikkat edilmelidir. Çok yüksek bonus, bilgiyi değil hızlı tıklamayı ödüllendirebilir. Puanı dengeli hesaplayan basit bir JavaScript örneği şöyledir:

```javascript
function puanHesapla(dogru, toplam, kalanSaniye, sure) {
  const basari = (dogru / toplam) * 80;
  const hizBonusu = (kalanSaniye / sure) * 20;
  return Math.round(basari + hizBonusu);
}
```

Bu fonksiyon doğruluğa 80, hıza en fazla 20 puanlık ağırlık verir. Böylece hızlı olmak avantaj sağlar ama doğru bilmenin önüne geçmez.

## Hangisini seçmelisiniz?

Ders materyalinin içine etkileşim eklemek istiyorsanız **H5P**, güvenilir sınavlar ve gelişmiş raporlama arıyorsanız **Moodle Quiz**, enerjik bir sınıf yarışması düzenleyecekseniz **Quizizz** daha uygundur. Hibrit kullanım da mümkündür: Konuyu H5P ile öğretip Moodle ile ölçebilir, ünite sonunda Quizizz ile eğlenceli tekrar yapabilirsiniz. En iyi sistem en fazla konfeti patlatan değil, öğrenme hedefini en doğru ölçendir.

![dijital-bilgi-yarismasi-30](/img/dijital-bilgi-yarismasi-30.svg)

