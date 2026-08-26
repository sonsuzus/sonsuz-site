---
layout: post
title: "Branch Prediction: İşlemciler Kodun Geleceğini Nasıl Tahmin Ediyor?"
math: true
categories: 
  - Bilgi
tags: 
  - işlemci
  - performans
  - branch prediction
toc: true
---

Modern bir işlemci, bir programdaki talimatları sırayla ve sabırla bekleyerek çalıştırmaz; adeta aceleci bir satranç oyuncusu gibi bir sonraki hamleyi önceden kestirmeye çalışır. Dallanma tahmini (branch prediction), `if`, `while`, `for` ve fonksiyon dönüşleri gibi karar noktalarında hangi kod yolunun izleneceğini tahmin eden donanım tekniğidir. Doğru tahminler işlem hattını dolu tutar, yanlış tahminler ise pahalı bir geri sarma etkisi yaratır.
``

## Sorun: İşlem hattı karar beklemeyi sevmez

İşlemciler talimatları **pipeline** adı verilen aşamalı bir düzende işler: getirme, çözümleme, yürütme ve sonuç yazma gibi adımlar aynı anda farklı talimatlar üzerinde çalışır. Ancak koşullu bir dallanma geldiğinde işlemci şu soruyla karşılaşır: “Sonraki talimat `if` bloğunda mı, yoksa `else` bloğunda mı?”

Koşulun sonucu henüz hazır değilse işlemci bekleyebilir. Fakat beklemek, işlem hattındaki boş koltuklar gibidir: donanım çalışabilecek durumdayken iş yapamaz. Bunun yerine işlemci bir yön seçer ve o yöndeki talimatları **spekülatif** olarak yürütmeye başlar.

Bir tahmin hatasının yaklaşık maliyeti şöyle modellenebilir:

$$\text{Kayıp çevrim} \approx D + R$$

Burada $D$, yanlış yolda ilerleyen pipeline derinliğini; $R$ ise doğru hedefe dönme ve yeni talimatları getirme maliyetini temsil eder. Derin ve yüksek frekanslı işlem hatlarında bu bedel onlarca saat çevrimine ulaşabilir.

| Yaklaşım | Karar biçimi | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| Dallanma yok | Sonucu bekler | Basit ve kesin | Pipeline sık sık durur |
| Statik tahmin | Örneğin “geri atlamayı al” | Düşük donanım maliyeti | Programın gerçek davranışını öğrenmez |
| Dinamik tahmin | Geçmiş sonuçlardan öğrenir | Yüksek doğruluk | Ek tablo ve karmaşıklık gerektirir |

## Tahminci geçmişten ne öğrenir?

En basit dinamik tasarımlardan biri, her dallanma için bir bit tutar: son sefer dallanma alındıysa yine alınacağını varsayar. Ne var ki döngünün sonunda bu yöntem genellikle iki kez yanılır: döngüden çıkışta ve sonraki girişte.

Bu nedenle yaygın çözüm **2 bitlik doyumlu sayaçtır**. Sayaç dört durumda gezerek tek bir istisnanın tahmini hemen tersine çevirmesini engeller:

| Sayaç durumu | Sayısal değer | Tahmin |
|---|---:|---|
| Güçlü alınmaz | 0 | Alınmaz |
| Zayıf alınmaz | 1 | Alınmaz |
| Zayıf alınır | 2 | Alınır |
| Güçlü alınır | 3 | Alınır |

Dallanma alınırsa sayaç 3'e doğru, alınmazsa 0'a doğru ilerler. Bu küçük “hafıza”, özellikle çoğu turda devam eden döngülerde çok etkilidir. İşlemciler bu sayaçları çoğunlukla **Branch History Table (BHT)** içinde saklar. Daha gelişmiş tahminciler ise global geçmişi, dallanmanın adresini ve hatta farklı dallanmalar arasındaki ilişkiyi birleştirir.

Aşağıdaki C örneğinde `i < n` kontrolü, son tur hariç çoğu kez doğru olduğundan tahminci için kolay bir hedeftir:

```c
long toplam(const int *veri, int n) {
    long sonuc = 0;

    for (int i = 0; i < n; i++) {
        if (veri[i] >= 0) {
            sonuc += veri[i];
        }
    }
    return sonuc;
}
```

Döngü koşulu düzenlidir; fakat `veri[i] >= 0` verinin dağılımına bağlıdır. Pozitif ve negatif değerler rastgele karışıyorsa tahmin oranı düşebilir. Bu durumda yalnızca algoritmanın $O(n)$ karmaşıklığı değil, verinin işlemciye ne kadar “öngörülebilir” göründüğü de pratik performansı etkiler.

## Yanlış tahminde ne olur?

İşlemci tahmin ettiği yolun talimatlarını geçici olarak çalıştırabilir; ancak sonuçları programın görünür durumuna hemen yazmaz. Dallanma sonucu ortaya çıktığında tahmin doğruysa iş tamamlanmış sayılır. Yanlışsa yanlış yoldaki spekülatif işler temizlenir, işlem hattı boşaltılır ve doğru hedeften yeniden başlanır. Buna **branch misprediction penalty** denir.

Dallanma tahmini, kodu her zaman “dalsız yazın” çağrısı değildir. Okunabilirlik ilk sırada kalmalıdır. Ancak sıcak döngülerde rastgele koşulları azaltmak, veriyi gruplayarak daha düzenli hale getirmek veya derleyicinin vektörleştirebildiği yapıları tercih etmek ölçülebilir fark yaratabilir. Kısacası işlemci geleceği gerçekten bilmez; geçmiş davranışlardan hızlı, istatistiksel ve çoğu zaman şaşırtıcı derecede başarılı bir bahis oynar.
