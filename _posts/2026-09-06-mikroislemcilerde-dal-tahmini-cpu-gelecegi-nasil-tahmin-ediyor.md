---
layout: post
title: "Mikroişlemcilerde Dal Tahmini: CPU Geleceği Nasıl Tahmin Ediyor?"
math: true
categories: 
  - Bilgi
tags: 
  - mikroişlemci
  - branch prediction
  - pipeline
toc: true
---

Modern işlemciler yalnızca komutları çalıştırmaz; bir sonraki komutun hangisi olacağını tahmin etmeye de çalışır. Özellikle `if`, `else`, döngü ve koşullu sıçrama içeren kodlarda kullanılan **dal tahmini (branch prediction)**, işlemcinin boru hattını dolu tutarak performansı artırır. Kısacası CPU, kodun geleceği hakkında küçük ama son derece hızlı bahisler oynar.

``

## Boru hattı neden tahmine ihtiyaç duyar?

Bir mikroişlemci komut yürütmeyi aşamalara ayırabilir: komutu getirme, çözümleme, çalıştırma ve sonucu yazma. Buna **pipeline**, yani boru hattı denir. Bir fabrikadaki üretim bandı gibi, farklı komutlar aynı anda farklı aşamalarda bulunur.

Basitleştirilmiş bir boru hattı şöyle gösterilebilir:

| Aşama | Görev |
|---|---|
| Fetch | Komutu bellekten getirir |
| Decode | Komutun anlamını çözer |
| Execute | İşlemi gerçekleştirir |
| Memory | Gerekirse belleğe erişir |
| Write Back | Sonucu yazmaçlara kaydeder |

Normal komutlarda sıradaki adres bellidir. Fakat aşağıdaki koşul işlemciyi bir yol ayrımına getirir:

```c
if (sicaklik > 80) {
    fan_ac();
} else {
    fan_kapat();
}
```

İşlemci, `sicaklik > 80` karşılaştırmasının sonucu henüz hesaplanmadan sonraki komutları getirmek ister. Beklerse pipeline içinde boşluklar oluşur. Bu kayıp genellikle **pipeline stall** olarak adlandırılır. Tahmin yaparsa seçtiği yoldaki komutları önceden boru hattına doldurabilir.

## Doğru ve yanlış tahminin maliyeti

Tahmin doğruysa hazırlanan komutlar çalışmaya devam eder ve zaman kazanılır. Yanlışsa spekülatif olarak getirilen komutlar iptal edilir, pipeline temizlenir ve doğru adresten yeniden doldurulur. Bu olaya **branch misprediction penalty** denir.

Ortalama dal maliyeti kabaca şöyle modellenebilir:

$$
C_{dal} = C_{temel} + (1-A) \times P
$$

Burada $A$ tahmin doğruluğu, $P$ yanlış tahmin cezasıdır. Örneğin doğruluk $A=0.95$ ve ceza $P=15$ çevrim ise ek maliyet:

$$
(1-0.95) \times 15 = 0.75 \text{ çevrim}
$$

Tahmin doğruluğundaki küçük bir artışın neden önemli olduğu buradan görülebilir.

| Durum | Pipeline sonucu | Performans etkisi |
|---|---|---|
| Doğru tahmin | Komutlar korunur | Yüksek verim |
| Yanlış tahmin | Komutlar temizlenir | Birkaç çevrim kayıp |
| Tahmin yapılmaması | Sonuç beklenir | Sürekli duraklama |

## Statik ve dinamik dal tahmini

**Statik tahmin**, çalışma geçmişini izlemeden sabit bir kural kullanır. Örneğin ileri yönlü dallar “alınmayacak”, döngülerdeki geri yönlü dallar “alınacak” kabul edilebilir. Donanımı basittir ancak değişken program davranışlarına kolayca uyum sağlayamaz.

**Dinamik tahmin** ise dalların geçmiş sonuçlarını kaydeder. Basit bir yaklaşım, her dal için bir veya iki bitlik sayaç tutmaktır. İki bitlik doygun sayaç; güçlü alınır, zayıf alınır, zayıf alınmaz ve güçlü alınmaz durumları arasında geçiş yapar. Tek bir sıra dışı sonuç böylece tahmini hemen tersine çeviremez.

| Yöntem | Geçmiş kullanımı | Karmaşıklık | Genel doğruluk |
|---|---:|---:|---:|
| Statik | Yok | Düşük | Orta |
| 1 bit sayaç | Son sonuç | Düşük | Orta |
| 2 bit sayaç | Yakın eğilim | Orta | Yüksek |
| Küresel/hibrit | Birden çok dal | Yüksek | Çok yüksek |

Modern işlemciler ayrıca **Branch Target Buffer** ile alınan dalın hedef adresini saklar. Küresel geçmiş tabloları, farklı dallar arasındaki ilişkileri öğrenebilir; hibrit tahminciler ise çeşitli yöntemlerden o an en başarılı olanı seçer.

## Yazılımcı açısından ne ifade eder?

Dal tahminini doğrudan yönetmek çoğu zaman mümkün değildir, ancak öngörülebilir koşullar yardımcı olabilir. Örneğin sıralı veriler üzerinde çalışan bir koşul, rastgele verilerdeki aynı koşuldan daha düzenli sonuç üretebilir:

```c
for (int i = 0; i < n; i++) {
    if (veri[i] >= esik) {
        toplam += veri[i];
    }
}
```

Bu kodda koşul sonuçları düzensizse tahminci daha sık yanılabilir. Yine de kodu sırf dalları azaltmak için karmaşıklaştırmak doğru değildir; derleyici optimizasyonları, önbellek davranışı ve okunabilirlik birlikte değerlendirilmelidir. En güvenilir yaklaşım, gerçek donanımda profil çıkarmaktır.

Dal tahmini, işlemcinin programı gerçekten bilmesi değil, geçmiş örüntülerden güçlü varsayımlar üretmesidir. Tahminci başarılı olduğunda pipeline akıcı çalışır; yanıldığında ise CPU yanlış sokağa girdiğini fark edip hızla geri döner.
