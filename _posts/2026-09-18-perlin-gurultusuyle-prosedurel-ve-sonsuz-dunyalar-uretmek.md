---
layout: post
title: "Perlin Gürültüsüyle Prosedürel ve Sonsuz Dünyalar Üretmek"
math: true
categories: 
  - Bilgi
tags: 
  - prosedürel üretim
  - perlin gürültüsü
  - oyun geliştirme
  - sonsuz dünya
  - javascript
  - algoritma
toc: true
---

Bir oyun dünyasını kare kare elle tasarlamak romantik görünebilir; ta ki milyonuncu ağacı yerleştirmeniz gerekene kadar! Prosedürel üretim, içeriği önceden saklamak yerine matematiksel kurallarla ihtiyaç anında oluşturur. Perlin gürültüsü ise rastgeleliğin kaotik görüntüsünü yumuşatarak dağlar, vadiler, adalar ve biyomlar üretmemizi sağlayan en kullanışlı araçlardan biridir.
``
## Rastgelelik neden yeterli değil?

Her hücreye bağımsız bir rastgele yükseklik verirsek komşu noktalar arasında sert sıçramalar oluşur. Sonuç, doğal bir arazi yerine televizyon parazitine benzer. Perlin gürültüsünde yakın koordinatlar benzer değerler üretir. Buna **uzamsal süreklilik** denir.

| Yöntem | Komşu değerler | Görsel sonuç | Kullanım alanı |
|---|---|---|---|
| Bağımsız rastgelelik | İlişkisiz | Parazitli ve keskin | Eşya düşürme, zar atma |
| Perlin gürültüsü | Yumuşak geçişli | Organik ve doğal | Arazi, bulut, mağara |
| Sabit desen | Tamamen öngörülebilir | Tekrarlı | Hazır bölümler, bulmacalar |

Perlin algoritması, ızgara köşelerine sözde rastgele gradyan vektörleri atar. Bir noktanın değeri; köşelere olan uzaklıklar, gradyanlarla yapılan skaler çarpımlar ve yumuşak interpolasyon kullanılarak hesaplanır. Klasik yumuşatma fonksiyonu şöyledir:

$$f(t)=6t^5-15t^4+10t^3$$

Bu fonksiyon hücre sınırlarındaki geçişlerin göze batmasını engeller. Aynı koordinat ve aynı **seed** kullanıldığında sonuç daima aynıdır. Böylece devasa dünyayı diskte tutmak yerine yalnızca seed değerini saklayabiliriz.

## Oktavlarla ayrıntı eklemek

Tek bir gürültü katmanı çoğu zaman fazla pürüzsüz görünür. Farklı ölçeklerdeki katmanları toplamak, yani fraktal Brown hareketi kullanmak, araziye hem kıtalar hem küçük tepeler kazandırır:

$$H(x,y)=N(x,y)+0.5N(2x,2y)+0.25N(4x,4y)$$

Burada frekans her oktavda artarken genlik azalır. Frekansın artış oranına **lacunarity**, genliğin azalış oranına **persistence** denir. Çok fazla oktav daha iyi dünya anlamına gelmez; bazen yalnızca CPU'nuzu dramatik biçimde ısıtır.

## Dünyayı parçalara bölmek

Sonsuz dünyanın tamamı aynı anda üretilemez. Harita, örneğin $32\times32$ hücrelik **chunk** parçalarına ayrılır. Oyuncuya yakın parçalar oluşturulur, uzaktakiler bellekten kaldırılır. Dikiş oluşmaması için gürültü yerel değil, küresel koordinatlarla örneklenmelidir.

```js
const CHUNK_SIZE = 32;

function createChunk(chunkX, chunkY, noise2D) {
  const tiles = [];

  for (let y = 0; y < CHUNK_SIZE; y++) {
    const row = [];
    for (let x = 0; x < CHUNK_SIZE; x++) {
      const worldX = chunkX * CHUNK_SIZE + x;
      const worldY = chunkY * CHUNK_SIZE + y;

      let height = 0;
      let amplitude = 1;
      let frequency = 0.008;
      let totalAmplitude = 0;

      for (let octave = 0; octave < 5; octave++) {
        height += noise2D(worldX * frequency, worldY * frequency)
          * amplitude;
        totalAmplitude += amplitude;
        amplitude *= 0.5;
        frequency *= 2;
      }

      height /= totalAmplitude;
      row.push(selectTerrain(height));
    }
    tiles.push(row);
  }
  return tiles;
}

function selectTerrain(height) {
  if (height < -0.25) return "derin_su";
  if (height < -0.05) return "kumsal";
  if (height < 0.45) return "ova";
  if (height < 0.7) return "tepe";
  return "karli_dag";
}
```

Kod, beş oktavı birleştirerek yüksekliği normalize eder ve eşiklere göre arazi türü seçer. `noise2D` fonksiyonu seed destekleyen bir Perlin kütüphanesinden gelebilir. Chunk koordinatları küresel konuma çevrildiği için komşu parçalar kusursuz birleşir.

## Performans ve dünya tutarlılığı

Üretilen chunk'ları koordinat anahtarlı bir önbellekte tutmak yeniden hesaplamayı azaltır. Oyuncunun yaptığı değişiklikler ise seed'den tekrar üretilemeyeceği için ayrıca kaydedilmelidir. Negatif koordinatlarda chunk hesabı yapılırken truncation yerine `Math.floor` kullanmak da önemlidir.

Perlin gürültüsü tek başına nehirlerin mantıklı akmasını veya şehirlerin uygun yerlere kurulmasını garanti etmez. Ancak erozyon, nem haritası, sıcaklık gürültüsü ve biyom kurallarıyla birleştirildiğinde birkaç sayıdan keşfedilmeyi bekleyen etkileyici bir dünya doğabilir.
