---
layout: post
title: "Zarlar Masada: Oyun Tasarımında Belirsizlik, Şans ve Strateji Dengesi"
math: true
categories: 
  - Bilgi
tags: 
  - oyun tasarımı
  - zar mekanikleri
  - olasılık
  - strateji
  - rastgelelik
  - game design
toc: true
image: /img/zarlar-masada-oyun-61.png
---

![zarlar-masada-oyun-61](/img/zarlar-masada-oyun-61.svg)


Bir zar masaya yuvarlandığında yalnızca sayı üretmez; gerilim, umut ve bazen de dramatik bir başarısızlık yaratır. Ancak iyi bir oyun tasarımında şans, oyuncunun kararlarını anlamsızlaştıran başıboş bir kaos değildir. Zar mekanikleri stratejiyle doğru biçimde birleştiğinde oyuncuya riskleri değerlendirme, planını uyarlama ve unutulmaz hikâyeler oluşturma fırsatı verir.

``

## Belirsizlik neden eğlencelidir?

Sonucu tamamen bilinen bir hamle, çoğu zaman çözülmesi gereken mekanik bir işleme dönüşür. Belirsizlik ise oyuncuya “Bunu şimdi denemeli miyim?” sorusunu sordurur. Tasarım açısından zarlar üç temel işlev üstlenebilir:

- **Gerilim yaratmak:** Kritik sonucun atış anına kadar bilinmemesi.
- **Tekrar oynanabilirliği artırmak:** Her oyunda farklı durumların ortaya çıkması.
- **Uyarlanabilir stratejiyi teşvik etmek:** Oyuncunun kötü veya iyi sonuçlara göre plan değiştirmesi.

Adil, altı yüzlü bir zar için herhangi bir sonucun olasılığı şöyledir:

$$P(x)=\frac{1}{6}$$

Bir zarın beklenen değeri ise:

$$E[X]=\frac{1+2+3+4+5+6}{6}=3.5$$

Elbette hiçbir atışta 3,5 gelmez. Beklenen değer, çok sayıda atışın ortalamasını ifade eder. Oyun ekonomisini dengelerken tek bir dramatik atıştan ziyade uzun vadeli ortalamalar bu nedenle önemlidir.

## Rastgelelik türleri

Her zar sistemi oyuncuya aynı deneyimi sunmaz. Rastgeleliğin ne zaman devreye girdiği, stratejik derinliği doğrudan etkiler.

| Yaklaşım | Rastgelelik zamanı | Oyuncu deneyimi | Örnek karar |
|---|---|---|---|
| Girdi rastgeleliği | Karardan önce | Planlama ve uyarlama | Zarları at, sonuçları işçilere dağıt |
| Çıktı rastgeleliği | Karardan sonra | Gerilim ve risk | Saldırıyı seç, isabet için zar at |
| Kontrollü rastgelelik | Karar sırasında | Risk yönetimi | Zar yenilemek için kaynak harca |
| Saf rastgelelik | Oyuncudan bağımsız | Düşük kontrol | Zar sonucu doğrudan kazananı belirlesin |

Girdi rastgeleliği genellikle daha stratejik algılanır; çünkü oyuncu sonucu gördükten sonra seçim yapar. Çıktı rastgeleliğinde ise oyuncu önce karar verir ve sonucuna katlanır. Bu yaklaşım heyecanlıdır, fakat uzun süren bir planı tek atışla yok ederse haksızlık hissi doğurabilir.

## Şansı yönetilebilir yapmak

Stratejik derinlik, rastgeleliği tamamen kaldırmakla değil, oyuncuya onu yönetebileceği araçlar vermekle oluşur. Yeniden zar atma, sonuç değiştirme, zar havuzu kurma veya güvenli seçeneği tercih etme gibi mekanikler karar alanını genişletir.

Örneğin oyuncu, başarı için en az 5 atmak zorunda olsun. Tek zarla başarı olasılığı:

$$P(başarı)=\frac{2}{6}=\frac{1}{3}$$

Bir kez yeniden atma hakkı varsa başarısızlık iki kez art arda gerçekleşmelidir:

$$P(başarı)=1-\left(\frac{4}{6}\right)^2=\frac{5}{9}$$

Böylece yeniden atma hakkı yalnızca bir bonus değil, saklanması veya harcanması gereken stratejik bir kaynağa dönüşür.

## Basit bir zar simülasyonu

Aşağıdaki JavaScript kodu, farklı zar sistemlerini binlerce kez çalıştırarak başarı oranını ölçer. Bu tür simülasyonlar, kâğıt üzerindeki olasılıkları doğrulamak ve karmaşık mekanikleri test etmek için kullanışlıdır.

```javascript
function zarAt(yuz = 6) {
  return Math.floor(Math.random() * yuz) + 1;
}

function testEt(deneme, yenidenAtabilir) {
  let basari = 0;

  for (let i = 0; i < deneme; i++) {
    let sonuc = zarAt();

    // İlk sonuç başarısızsa oyuncu hakkını kullanır.
    if (sonuc < 5 && yenidenAtabilir) {
      sonuc = zarAt();
    }

    if (sonuc >= 5) basari++;
  }

  return basari / deneme;
}

console.log(testEt(100000, false));
console.log(testEt(100000, true));
```

## İyi denge için tasarım ilkeleri

Oyuncunun önemli kararları, tek bir kötü zarla tamamen silinmemelidir. Büyük sonuçlar mümkünse birden fazla atışın, kaynak yönetiminin ve önceki tercihlerin birleşiminden doğmalıdır. Ayrıca olasılıklar oyuncuya açıkça gösterilmeli; “yüzde 80 başarı” ifadesi ile belirsiz bir “yüksek ihtimal” aynı psikolojik etkiyi yaratmaz.

İdeal zar mekaniği, oyuncuya hem umut hem sorumluluk verir. Oyuncu kaybettiğinde yalnızca zarı suçluyorsa sistem fazla rastgeledir; her sonucu önceden hesaplayabiliyorsa sistem fazla deterministiktir. Eğlence, plan ile sürprizin tokalaştığı o küçük belirsizlik alanında yaşar.
