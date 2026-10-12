---
layout: post
title: "Luhn Algoritması ile Kart Numarası Doğrulama"
math: true
categories: 
  - Program
tags: 
  - luhn algoritması
  - javascript
  - kredi kartı
  - veri doğrulama
  - algoritma
  - programlama
toc: true
image: /img/luhn-algoritmasi-ile-54.png
---

Bir kart numarasını yanlış yazdığınızda sistemin hatayı ödeme kuruluşuna ulaşmadan fark etmesi sihir değildir. Çoğu kart numarası, basit ama etkili bir sağlama yöntemi olan **Luhn algoritması** ile kontrol edilebilir. Gelin algoritmanın matematiksel mantığını inceleyelim ve JavaScript ile yeniden kullanılabilir bir doğrulayıcı geliştirelim.

![luhn-algoritmasi-ile-54](/img/luhn-algoritmasi-ile-54.svg)

``
## Luhn algoritması ne işe yarar?

IBM araştırmacısı Hans Peter Luhn tarafından geliştirilen algoritma; kredi kartı numaraları, IMEI kodları ve bazı kimlik numaralarındaki yazım hatalarını yakalamak için kullanılır. Temel amacı bir numaranın gerçekten aktif, kullanılabilir veya bir kişiye ait olduğunu kanıtlamak değildir. Yalnızca rakam dizisinin belirlenen sağlama kuralına uyup uymadığını söyler.

Başka bir ifadeyle Luhn kontrolünden geçen rastgele bir sayı üretilebilir. Bu nedenle algoritma bir güvenlik veya yetkilendirme mekanizması olarak görülmemelidir.

| Kontrol | Luhn yapabilir mi? | Açıklama |
|---|---:|---|
| Eksik veya hatalı rakamı yakalama | Genellikle | Yaygın veri giriş hatalarını belirler |
| Kartın bankada kayıtlı olduğunu doğrulama | Hayır | Banka veya ödeme altyapısı gerekir |
| Kart sahibini doğrulama | Hayır | Kimlik doğrulama işlemi değildir |
| Sunucuya gitmeden ön kontrol yapma | Evet | Tarayıcıda kolayca çalıştırılabilir |

## Matematiksel mantık

Numaranın rakamları sağdan sola doğru işlenir. En sağdaki rakam kontrol basamağıdır. Sağdan başlayarak her ikinci rakam ikiyle çarpılır. Çarpım 9'dan büyükse sonuçtan 9 çıkarılır. Elde edilen bütün değerler toplanır.

Toplam $S$ ile gösterilirse numara şu koşul sağlandığında Luhn açısından geçerlidir:

$$S \bmod 10 = 0$$

Örneğin `79927398713` sayısını düşünelim. Sağdan sola ilerlerken uygun konumlardaki rakamlar iki katına çıkarılır. `8` rakamının iki katı `16` olduğunda $16-9=7$ kullanılır. Bu işlem aslında `16` sayısının basamaklarını toplamakla, yani $1+6=7$ hesaplamakla aynıdır.

| İki katına çıkarılan değer | Dönüştürülmüş değer |
|---:|---:|
| 4 | 4 |
| 8 | 8 |
| 12 | 3 |
| 16 | 7 |

Dokuz çıkarma kuralı kodu sadeleştirir; iki basamaklı sonuçları ayrıca metne dönüştürmemize gerek kalmaz.

## JavaScript ile uygulama

Aşağıdaki fonksiyon boşluk ve kısa çizgileri temizler, girdinin yalnızca rakamlardan oluştuğunu denetler ve ardından Luhn toplamını hesaplar:

```javascript
function luhnDogrula(kartNumarasi) {
  const temizNumara = String(kartNumarasi).replace(/[\s-]/g, '');

  if (!/^\d+$/.test(temizNumara) || temizNumara.length < 2) {
    return false;
  }

  let toplam = 0;
  let ikiyleCarp = false;

  for (let i = temizNumara.length - 1; i >= 0; i--) {
    let rakam = Number(temizNumara[i]);

    if (ikiyleCarp) {
      rakam *= 2;
      if (rakam > 9) rakam -= 9;
    }

    toplam += rakam;
    ikiyleCarp = !ikiyleCarp;
  }

  return toplam % 10 === 0;
}

console.log(luhnDogrula('7992 7398 713')); // true
console.log(luhnDogrula('7992 7398 714')); // false
```

`ikiyleCarp` değişkeni her turda tersine çevrilerek sıradaki rakama hangi işlemin uygulanacağı belirlenir. Döngünün sağdan başlaması önemlidir; çünkü çiftleme düzeni kontrol basamağına göre kurulmuştur. Boşlukların ve kısa çizgilerin temizlenmesi ise kullanıcıların `1234 5678` gibi okunabilir biçimler girmesine izin verir.

## Kullanırken nelere dikkat edilmeli?

Gerçek projelerde Luhn kontrolünü form doğrulamasının yalnızca ilk katmanı olarak kullanın. Kart numarasını günlük dosyalarına yazmayın, gereksiz yere saklamayın ve ödeme işlemlerini PCI DSS uyumlu sağlayıcılara bırakın. İstemci tarafındaki kontrol kullanıcı deneyimini iyileştirir; ancak aynı doğrulama sunucuda da yapılmalıdır, çünkü tarayıcıdaki JavaScript değiştirilebilir.

Sonuç olarak Luhn algoritması güçlü bir şifreleme tekniği değil, hızlı bir hata süzgecidir. Birkaç aritmetik işlemle yaygın yazım yanlışlarını yakalaması, küçük algoritmaların gerçek dünyada ne kadar faydalı olabileceğinin harika bir örneğidir.
