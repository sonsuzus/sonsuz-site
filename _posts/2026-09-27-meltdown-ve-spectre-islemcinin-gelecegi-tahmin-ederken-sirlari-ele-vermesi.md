---
layout: post
title: "Meltdown ve Spectre: İşlemcinin Geleceği Tahmin Ederken Sırları Ele Vermesi"
math: true
categories: 
  - Bilgi
tags: 
  - meltdown
  - spectre
  - işlemci
  - siber güvenlik
  - spekülatif yürütme
  - önbellek
  - yan kanal
toc: true
image: /img/meltdown-ve-spectre-68.png
---

Modern işlemciler yalnızca hızlı koşmaz; önlerindeki yolu tahmin ederek henüz gerekli olup olmadığı bilinmeyen komutları da çalıştırır. **Meltdown** ve **Spectre**, performans uğruna geliştirilen bu davranışın mimari olarak görünmeyen fakat ölçülebilen izler bırakabildiğini gösterdi. Sonuçta saldırgan, doğrudan okuyamadığı parolaları, anahtarları ve başka süreçlere ait verileri önbellek zamanlamalarını dinleyerek çıkarabilir.

``

## İşlemci neden geleceği tahmin eder?

Bir işlemci bellekten veri beklerken yüzlerce saat çevrimi kaybedebilir. Bu nedenle modern çekirdekler **sıra dışı yürütme** ve **spekülatif yürütme** kullanır. Örneğin bir dallanmanın sonucu henüz hesaplanmadıysa dallanma tahmincisi geçmiş davranışlara bakarak hangi yolun seçileceğini tahmin eder.

Tahmin doğruysa zaman kazanılır. Yanlışsa spekülatif işlemlerin mimari sonuçları iptal edilir. Ancak kritik ayrıntı şudur: Önbelleğe alınan veri gibi **mikromimari etkiler** tamamen geri alınmayabilir.

Basitleştirilmiş performans fikri şöyledir:

$$T_{ortalama} = pT_{isabet} + (1-p)T_{hata}$$

Burada $p$ tahmin doğruluğudur. Yüksek doğruluk ciddi hız kazandırır; fakat yanlış yol üzerinde geçici olarak yürütülen komutlar güvenlik sınırlarına dokunabilir.

## Önbellek nasıl muhbir olur?

İşlemci önbelleğindeki bir veriye erişmek ana belleğe erişmekten daha hızlıdır:

$$T_{cache} < T_{RAM}$$

Saldırgan verinin kendisini göremese bile belirli bir bellek bölgesine erişimin kaç nanosaniye sürdüğünü ölçebilir. Hızlı yanıt, ilgili satırın önbellekte olduğunu düşündürür. Böylece gizli bir bayt, farklı önbellek satırlarından birini seçmek için kullanılır ve değer zamanlama ölçümleriyle tahmin edilir.

Aşağıdaki kod, savunmasız desenin kavramsal ve çalıştırılabilir bir örneğidir; tek başına gerçek bir veri sızdırma saldırısı değildir:

```c
unsigned char public_data[16];
unsigned char probe[256 * 4096];
size_t public_size = 16;

unsigned char read_value(size_t index) {
    if (index < public_size) {
        unsigned char value = public_data[index];
        return probe[value * 4096];
    }
    return 0;
}
```

Tahminci, koşulun genellikle doğru olduğuna alıştırılmışsa sınır dışı bir `index` geldiğinde gövdeyi geçici olarak çalıştırabilir. Mimari sonuç daha sonra silinse de `value` tarafından seçilen `probe` satırı önbellekte kalabilir. Saldırgan 256 olası satırın erişim sürelerini karşılaştırarak baytı arar.

## Meltdown ve Spectre aynı şey mi?

| Özellik | Meltdown | Spectre |
|---|---|---|
| Temel sorun | Yetki kontrolünün geç etkili olması | Tahmin mekanizmasının yanıltılması |
| Tipik hedef | Çekirdek belleği ile kullanıcı alanı sınırı | Aynı süreç veya farklı güven alanları |
| Kullanılan mekanizma | Sıra dışı, geçici yürütme | Dallanma ve dolaylı hedef tahmini |
| Yazılımla azaltma | Sayfa tablolarını ayırma | Bariyerler, retpoline, kod düzenleme |
| Etkilenen tasarımlar | Özellikle bazı eski Intel işlemciler | Çok sayıda modern işlemci ailesi |

**Meltdown**, işlemcinin yetkisiz bellek okumasını hata üretmeden önce geçici olarak ilerletebilmesinden yararlanır. İşletim sistemi sonunda erişimi reddeder; fakat sır önbelleğe kodlanmış olabilir.

**Spectre** ise kurbanın yasal kodunu yanlış tahminlerle kandırır. Sınır kontrolü bulunsa bile işlemci geçici olarak yanlış yola sokulur. Bu nedenle Spectre tek bir donanım hatasından çok, optimizasyon ile güvenlik modeli arasındaki temel bir çatışmadır.

## Savunma neden zor?

Savunmalar arasında KPTI ile çekirdek sayfa tablolarını ayırmak, hassas noktalara spekülasyon bariyerleri eklemek, mikro kod güncellemeleri ve tarayıcılarda zamanlayıcı hassasiyetini azaltmak bulunur. Ancak her bariyer işlemciye “Burada tahmin etme, bekle” dediği için performans maliyeti doğurabilir.

Meltdown ve Spectre’nin büyük dersi şudur: Bir işlem mimari olarak gerçekleşmemiş sayılsa bile fiziksel sistemde iz bırakabilir. Güvenlik yalnızca programın ürettiği sonuçları değil; önbellekleri, tahmincileri, zamanlamayı ve geçici yürütmenin bütün gölgelerini hesaba katmalıdır.

![meltdown-ve-spectre-68](/img/meltdown-ve-spectre-68.svg)

