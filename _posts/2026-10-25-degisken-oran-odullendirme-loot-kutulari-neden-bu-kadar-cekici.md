---
layout: post
title: "Değişken Oran Ödüllendirme: Loot Kutuları Neden Bu Kadar Çekici?"
math: true
categories: 
  - Bilgi
tags: 
  - değişken oran
  - loot kutusu
  - dopamin
  - oyun tasarımı
  - davranış bilimi
  - bağımlılık mekanikleri
toc: true
image: /img/degisken-oran-odullendirme-90.png
---

![degisken-oran-odullendirme-90](/img/degisken-oran-odullendirme-90.svg)


Bir sandığı açıyorsunuz: sıradan bir kılıç. Bir tane daha: yine sıradan. Tam bırakacakken ekranda altın renkli bir parıltı beliriyor ve nadir karakter çıkıyor! Loot kutularının çekiciliği yalnızca ödülün kendisinden değil, ödülün **ne zaman geleceğini bilememekten** doğar. Değişken oran ödüllendirme adı verilen bu mekanik; oyun tasarımını, davranış psikolojisini ve beynin ödül öğrenme sistemini aynı noktada buluşturur.
``

## Değişken oran ödüllendirme nedir?

Davranış biliminde ödüllendirme programları, bir davranışın hangi koşulda pekiştirileceğini açıklar. **Sabit oranlı** sistemde oyuncu, örneğin her 10 görevden sonra ödül kazanır. Değişken oranlı sistemdeyse ödül, öngörülemeyen sayıda denemeden sonra gelir.

Bir loot kutusundan nadir eşya çıkma olasılığı $p$ ise, ilk başarıya kadar gereken ortalama deneme sayısı yaklaşık olarak şöyledir:

$$E[N] = \frac{1}{p}$$

Örneğin nadir eşya olasılığı $p=0.02$ olduğunda beklenen değer 50 denemedir. Ancak bu, eşyanın kesinlikle 50. kutuda çıkacağı anlamına gelmez. İlk kutuda da çıkabilir, 150 kutu boyunca hiç çıkmayabilir. Belirsizliği güçlü kılan tam olarak bu dağılımdır.

| Ödül modeli | Oyuncunun beklentisi | Davranışsal etkisi |
|---|---|---|
| Sabit oran | Ödülün ne zaman geleceği bilinir | Planlı ve kontrollü tekrar |
| Değişken oran | Her deneme kazandırabilir | Israrlı tekrar davranışı |
| Sabit zaman | Belirli süre sonunda ödül | Düzenli geri dönüş |
| Değişken zaman | Ödül zamanı belirsizdir | Sık kontrol etme eğilimi |

## Dopamin yalnızca haz kimyasalı değildir

Dopamin çoğu zaman basitçe haz hormonu diye anlatılır; fakat daha doğru yaklaşım, onun **motivasyon, dikkat ve ödül öğrenmesiyle** ilişkili bir nörotransmiter olduğunu söylemektir. Beyin yalnızca ödüle değil, beklenen sonuç ile gerçekleşen sonuç arasındaki farka da tepki verir. Buna ödül tahmin hatası denir:

$$\delta = r - V$$

Burada $r$ alınan gerçek ödülü, $V$ ise beklenen değeri temsil eder. Sonuç beklenenden iyiyse $\delta$ pozitiftir ve beyin, ödülden önceki ipuçlarını öğrenmeye başlar. Sandığın sallanması, özel sesler, renkli animasyonlar ve kısa bekleme anı böylece güçlü beklenti sinyallerine dönüşebilir.

Önemli bir ayrım var: Dopamin, oyuncunun mutlaka bağımlı olduğu anlamına gelmez. Problemli davranış; kişisel yatkınlık, harcama kolaylığı, sosyal baskı, kayıp telafisi düşüncesi ve oyunun tasarımı gibi birçok etkenin birleşmesiyle gelişir.

## Rastgeleliği kodla görmek

Aşağıdaki JavaScript örneği, yüzde 2 olasılıkla nadir eşya veren basit bir kutu sistemini simüle eder:

```javascript
function kutuAc() {
  const nadirlikOlasiligi = 0.02;
  return Math.random() < nadirlikOlasiligi
    ? 'Nadir eşya'
    : 'Sıradan eşya';
}

let deneme = 0;
let sonuc;

do {
  deneme++;
  sonuc = kutuAc();
} while (sonuc !== 'Nadir eşya');

console.log(`Nadir eşya ${deneme}. kutuda çıktı.`);
```

Kod her çalıştırıldığında farklı sonuç üretir. Bu basit döngü, oyuncunun bir sonraki denemenin kazandırabileceği düşüncesiyle neden devam edebildiğini gösterir. Gerçek sistemlerde buna sınırlı süreli etkinlikler, yakın ıskalama efektleri ve ücretsiz başlangıç kutuları da eklenebilir.

## Tasarım ile manipülasyon arasındaki çizgi

Rastgele ödüller başlı başına kötü değildir; sürpriz ve tekrar oynanabilirlik sağlayabilir. Risk, gerçek para harcamasının belirsiz sonuçlarla birleştiği ve olasılıkların gizlendiği noktada büyür. Etik bir sistem; çıkma oranlarını açıkça göstermeli, harcama sınırları sunmalı, çocukları korumalı ve belirli sayıda denemeden sonra garanti ödül veren **pity sistemi** kullanmalıdır.

İyi oyun tasarımı oyuncuyu eğlendirmeyi hedefler; karanlık tasarım ise bilişsel zayıflıkları gelir aracına dönüştürür. Bir sonraki kutu gerçekten efsanevi eşya içerebilir—butonu tıklamadan önce sorulması gereken soru şudur: Kararı ben mi veriyorum, yoksa belirsizlik mi?
