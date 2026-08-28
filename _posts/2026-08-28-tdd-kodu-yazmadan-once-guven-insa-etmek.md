---
layout: post
title: "TDD: Kodu Yazmadan Önce Güven İnşa Etmek"
math: true
categories: 
  - Bilgi
tags: 
  - TDD
  - Yazılım Testi
  - Yazılım Kalitesi
---

Test Güdümlü Geliştirme (Test-Driven Development, TDD), üretim kodunu yazmadan önce o kodun beklenen davranışını bir testle tarif etme disiplinidir. İlk bakışta “henüz olmayan kodu nasıl test ederim?” sorusunu doğurur; fakat asıl güç tam burada saklıdır: Geliştirici önce çözümün iç yapısını değil, kullanıcıya sunduğu sonucu düşünür. Böylece kod, tahminlere göre değil, doğrulanabilir gereksinimlere göre büyür.
``

TDD’nin klasik döngüsü **Kırmızı–Yeşil–İyileştir** olarak bilinir. Önce başarısız olan küçük bir test yazılır (**kırmızı**). Ardından testi geçirecek en basit üretim kodu eklenir (**yeşil**). Son olarak davranışı değiştirmeden kod sadeleştirilir, tekrarlar temizlenir ve isimler iyileştirilir (**refactor**). Döngü kısa tutulduğunda hata ayıklama alanı da küçülür: Sorun çıktıysa büyük olasılıkla son birkaç satırdadır.

Yazılım kalitesini kabaca şu üç bileşenin çarpımı gibi düşünebiliriz:

$$Kalite \approx Doğruluk \times BakımKolaylığı \times DeğişimGüveni$$

TDD her bileşeni doğrudan etkiler. Testler doğru davranışı kayıt altına alır; küçük tasarım adımları karmaşıklığı azaltır; otomatik test paketi ise değişiklikten sonra “bir şeyi kırdım mı?” sorusuna saniyeler içinde yanıt verir. Elbette bu matematiksel bir ölçüm değildir; kaliteli kodun yalnızca çalışmakla kalmayıp güvenle değiştirilebilmesi gerektiğini anlatan yararlı bir modeldir.

| Yaklaşım | Başlangıç noktası | Hata fark etme zamanı | Tasarım etkisi |
|---|---|---|---|
| Önce kod, sonra test | Uygulama ayrıntıları | Çoğunlukla test aşamasında | Bağımlılıklar kolayca büyür |
| TDD | Beklenen davranış | Her küçük adımda | Daha küçük, ayrık bileşenleri teşvik eder |
| Sadece manuel test | Kullanıcı senaryosu | Geç ve tekrarlanması zor | Regresyon riski yüksektir |

Örneğin bir indirim hesaplayıcısı geliştirirken önce “%20 indirim 100 TL için 80 TL üretmelidir” davranışını yazalım. Bu test, henüz `indirimliFiyat` fonksiyonu bulunmadığı için ilk çalıştırmada başarısız olur. Bu başarısızlık kusur değil, hedefin netleştiğinin kanıtıdır.

```javascript
import { indirimliFiyat } from './fiyat.js';

test('100 TL ürüne yüzde 20 indirim uygular', () => {
  expect(indirimliFiyat(100, 20)).toBe(80);
});
```

Testi yeşile çevirecek ilk uygulama oldukça küçük olabilir:

```javascript
export function indirimliFiyat(fiyat, oran) {
  return fiyat * (1 - oran / 100);
}
```

Burada önemli nokta, ilk anda tüm olasılıkları çözmeye çalışmamaktır. Sonraki testler negatif fiyat, yüzde 100’ü aşan oran veya küsurat yuvarlama kurallarını tanımladıkça kod evrilir. Örneğin para işlemlerinde kayan nokta hassasiyeti nedeniyle `0.1 + 0.2` beklenmedik sonuçlar verebilir; bu yüzden kuruş cinsinden tamsayı kullanmak ya da belirlenmiş bir yuvarlama politikası uygulamak gerekir.

TDD, “çok test yazmak” anlamına gelmez. Değerli test; davranışı anlatan, hızlı çalışan, birbirinden bağımsız ve uygulama ayrıntılarına gereksiz bağlanmayan testtir. Veritabanına, ağa veya zamana doğrudan bağlı testler yavaş ve kararsız olabilir. Bu bağımlılıkları arayüzler veya sahte nesnelerle ayırmak, testlerin deterministik olmasını sağlar.

| İyi TDD alışkanlığı | Kaçınılması gereken durum |
|---|---|
| Tek davranışı doğrulayan kısa testler | Bir testte onlarca senaryoyu birleştirmek |
| Anlamlı test isimleri | `test1`, `çalışıyor mu` gibi belirsiz adlar |
| Refactor sonrası testleri çalıştırmak | Testleri yalnızca teslimden önce çalıştırmak |
| Kenar durumları ayrı tanımlamak | Sadece mutlu yolu doğrulamak |

Sonuç olarak TDD, sihirli bir hata önleme makinesi değil; düşünme maliyetini erkene çeken bir geri bildirim sistemidir. Gereksinimleri somut örneklere dönüştürür, tasarımı sürekli sınar ve cesur refactor’lar için emniyet kemeri sağlar. Küçük bir fonksiyonla başlayın: önce başarısız testi görün, sonra onu yeşile çevirin. Birkaç döngü sonra kodunuzu değil, kararlarınızı test ettiğinizi fark edeceksiniz.
