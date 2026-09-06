---
layout: post
title: "Mutation Testing ile Testlerinizin Gerçekten Güçlü Olup Olmadığını Ölçün"
math: true
categories: 
  - Bilgi
tags: 
  - mutation testing
  - yazılım testi
  - test kalitesi
image: /img/mutation-testing-ile-43.png
---

Bir test paketinin yeşil olması, uygulamanın iyi test edildiği anlamına gelmez. Testler yalnızca kodu çalıştırıyor, fakat yanlış sonucu fark etmiyor olabilir. Mutation testing (mutasyon testi), bu konfor alanını bozan bir tekniktir: Kodunuza kasıtlı, küçük hatalar ekler ve testlerinizin bu hataları yakalayıp yakalayamadığını ölçer. Kısacası soru “Kod çalışıyor mu?” değil, “Testlerim hatalı kodu reddedebiliyor mu?” olur.


![mutation-testing-ile-43](/img/mutation-testing-ile-43.svg)

``

Mutasyon testinin temel aktörü **mutant**tır. Mutant, üretim kodunun bilerek değiştirilmiş bir sürümüdür. Örneğin `>` operatörü `>=` yapılabilir, bir koşulun sonucu tersine çevrilebilir veya bir metot çağrısı kaldırılabilir. Ardından mevcut test paketi mutant üzerinde çalıştırılır. En az bir test başarısız olursa mutant **öldürülmüş** sayılır; tüm testler geçerse mutant **hayatta kalmıştır**. Hayatta kalan mutant, test senaryolarınızda bir kör nokta olduğuna işaret eder.

Mutasyon skoru genellikle şu formülle hesaplanır:

$$Mutation\ Score = \frac{Killed\ Mutants}{Total\ Mutants - Equivalent\ Mutants} \times 100$$

Buradaki kritik istisna **eşdeğer mutant**tır. Kod değişmiş görünse bile davranış değişmiyorsa, testin onu öldürmesi mümkün değildir. Örneğin `x + 0` ifadesini `x` yapmak çoğu durumda eşdeğer bir dönüşümdür. Bu mutantlar skordan çıkarılmalıdır; aksi takdirde test paketinizi haksız yere başarısız görürsünüz.

| Kavram | Anlamı | Test kalitesi için mesajı |
|---|---|---|
| Öldürülen mutant | Bir test hata eklenmiş kodu yakaladı | İlgili davranış iyi korunuyor |
| Hayatta kalan mutant | Tüm testler yeşil kaldı | Eksik assertion veya senaryo olabilir |
| Eşdeğer mutant | Davranış gerçekte değişmedi | Manuel değerlendirme gerekebilir |
| Mutasyon skoru | Öldürülen mutantların oranı | Kapsamdan daha anlamlı bir kalite sinyali |

Örneğin aşağıdaki indirim hesabında sınır koşulu oldukça önemlidir:

```javascript
export function calculateDiscount(total, isVip) {
  if (isVip && total > 1000) {
    return total * 0.20;
  }
  return total * 0.05;
}
```

Bir mutasyon aracı `total > 1000` koşulünü `total >= 1000` hâline getirebilir. Yalnızca `1500` ve `500` değerlerini test ediyorsanız mutant hayatta kalır; çünkü iki durumda da davranış aynıdır. Sınır değerini hedefleyen test ise problemi yakalar:

```javascript
import { calculateDiscount } from './discount.js';

test('VIP müşteri 1000 TL sepetle standart indirim alır', () => {
  expect(calculateDiscount(1000, true)).toBe(50);
});

test('VIP müşteri 1001 TL sepetle yüzde 20 indirim alır', () => {
  expect(calculateDiscount(1001, true)).toBeCloseTo(200.2);
});
```

Bu testler sadece satır çalıştırmaz; iş kuralının eşiğini doğrular. Mutation testing’in asıl değeri de budur: geliştiriciyi daha iyi assertion yazmaya, sınır değerleri düşünmeye ve gereksiz mock kullanımını sorgulamaya iter.

| Yaklaşım | Ölçtüğü şey | Tek başına riski |
|---|---|---|
| Code coverage | Testlerin hangi satırlardan geçtiği | Assertion zayıflığını gizleyebilir |
| Unit test sayısı | Test miktarı | Çok sayıda yüzeysel test üretilebilir |
| Mutation testing | Testlerin hatayı yakalama gücü | Çalıştırması daha maliyetlidir |

JavaScript projelerinde Stryker, Java dünyasında PIT, Python tarafında ise mutmut popüler araçlardır. Bunları her küçük değişiklikte tüm proje için çalıştırmak pahalı olabilir. Pratik bir strateji; önce değişen modüllerde, ardından CI pipeline’ında gece çalışacak daha geniş bir mutasyon testi planlamaktır. Başlangıçta yüzde 100 skor hedeflemek yerine, hayatta kalan mutantları tek tek inceleyin: gerçek bir eksik mi, eşdeğer davranış mı, yoksa önemsiz bir ayrıntı mı?

Sonuç olarak mutasyon testi bir puan yarışından çok geri bildirim mekanizmasıdır. Coverage size “nerelere gittim?” der; mutation testing ise “orada gerçekten bir şeyi doğruladım mı?” diye sorar. Bu soruya düzenli cevap vermek, test paketinizi güvenlik ağı olmaktan çıkarıp gerçek bir kalite filtresine dönüştürür.
