---
layout: post
title: "JIT Derleme Mantığı: Kod Çalışırken Nasıl Hızlanır?"
math: true
categories: 
  - Bilgi
tags: 
  - jit
  - derleyici
  - performans
  - java
  - javascript
  - sanal-makine
toc: true
image: /img/jit-derleme-mantigi-68.png
---

Bir programın çalışmaya başladıktan birkaç saniye sonra hızlanması ilk bakışta sihir gibi görünebilir. Oysa perde arkasında, kodu izleyen ve sık kullanılan bölümleri daha verimli makine koduna dönüştüren bir mekanizma vardır: **JIT (Just-In-Time) derleme**. Java, JavaScript ve .NET gibi platformlarda kullanılan bu yaklaşım, yorumlayıcının esnekliğiyle önceden derlemenin hızını birleştirir.
``
## Derleme ile yorumlama arasındaki köprü

Bir işlemci Java, C# veya JavaScript gibi yüksek seviyeli dilleri doğrudan anlayamaz; yalnızca kendi komut setine uygun makine kodunu çalıştırır. Bu dönüşüm için üç temel yaklaşım bulunur:

| Yaklaşım | Dönüşüm zamanı | Avantajı | Dezavantajı |
|---|---|---|---|
| AOT derleme | Program çalışmadan önce | Hızlı başlangıç ve öngörülebilir performans | Çalışma zamanı davranışını bilemez |
| Yorumlama | Her komut çalıştırılırken | Esnek ve taşınabilir | Tekrarlanan çözümleme maliyetlidir |
| JIT derleme | Program çalışırken | Gerçek kullanım verisine göre optimizasyon | Isınma süresi ve ek bellek gerektirir |

JIT kullanan sistemler genellikle kaynak kodu önce **bytecode** veya benzeri bir ara temsile dönüştürür. Sanal makine başlangıçta bu ara kodu yorumlayabilir. Aynı fonksiyon tekrar tekrar çağrıldığında sistem, “Bu bölge sıcak!” diyerek onu yerel makine koduna derler.

## Sıcak kod nasıl belirlenir?

Çalışma zamanı; metot çağrılarını, döngü tekrarlarını ve kullanılan veri türlerini sayaçlarla takip eder. Bir kod parçasının çağrı sayısını $n$, yorumlama maliyetini $I$, derleme maliyetini $C$ ve derlenmiş çalışma maliyetini $M$ olarak düşünelim. JIT derlemenin kazançlı olması için yaklaşık olarak şu koşul aranır:

$$nI > C + nM$$

Başka bir ifadeyle, gelecekte sağlanacak hız kazancı derleme masrafını aşmalıdır. Yalnızca bir kez çalışan başlangıç kodunu derlemek çoğu zaman gereksizdir. Fakat milyonlarca kez dönen küçük bir hesaplama fonksiyonu oldukça değerli bir hedeftir.

```java
static long karelerToplami(int limit) {
    long toplam = 0;
    for (int i = 0; i < limit; i++) {
        toplam += (long) i * i;
    }
    return toplam;
}
```

Bu metot sık çağrılırsa JIT, yalnızca makine kodu üretmekle kalmaz; döngüyü açabilir, gereksiz kontrolleri kaldırabilir veya işlemcinin vektör komutlarından yararlanabilir. Böylece aynı sonuç daha az komutla hesaplanır.

## JIT’in gizli silahı: spekülatif optimizasyon

AOT derleyici, programın gelecekte hangi türlerle karşılaşacağını kesin olarak bilemez. JIT ise gerçek çalışma verisini görür. Örneğin JavaScript’te aşağıdaki fonksiyon başlangıçta her tür değeri kabul edebilir:

```javascript
function topla(a, b) {
  return a + b;
}

for (let i = 0; i < 1_000_000; i++) {
  topla(i, i + 1);
}
```

Motor, `a` ve `b` değerlerinin sürekli tam sayı olduğunu gözlemlerse genel amaçlı toplama yerine hızlı bir tamsayı komutu üretebilir. Buna **spekülatif optimizasyon** denir: sistem, gözlenen düzenin devam edeceğini varsayar.

Peki daha sonra `topla("merhaba", " dünya")` çağrılırsa ne olur? Varsayım bozulur ve motor **deoptimizasyon** yaparak daha genel koda geri döner. JIT hızlıdır ama falcı değildir; tahminlerini gerektiğinde iptal eder.

## Isınma neden önemlidir?

İlk çağrılar sırasında profil oluşturma ve derleme maliyeti bulunduğundan performans testlerinde “warm-up” aşaması kullanılır. Aksi hâlde ölçüm, uygulamanın kararlı hızından çok başlangıç masraflarını gösterir.

JIT’in çalışma döngüsü kısaca şöyledir:

1. Ara kodu yorumlayarak hızlıca başla.
2. Çalışma davranışını profille.
3. Sıcak bölgeleri makine koduna derle.
4. Gözlenen türlere göre agresif optimizasyon uygula.
5. Varsayımlar bozulursa güvenli sürüme geri dön.

Sonuç olarak kod aslında kendi kendine öğrenmez; çalışma zamanı sistemi onu gözlemler ve kaynaklarını en çok kullanılan bölgelere yatırır. Program “ısındıkça” hızlanmasının nedeni de tam olarak budur.

![jit-derleme-mantigi-68](/img/jit-derleme-mantigi-68.svg)

