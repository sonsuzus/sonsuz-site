---
layout: post
title: "Kotlin Coroutines'in Perde Arkası: Suspend Fonksiyonlardan State Machine'e"
math: true
categories: 
  - Bilgi
tags: 
  - kotlin
  - coroutines
  - state-machine
  - asenkron-programlama
  - jvm
  - continuation
toc: true
image: /img/kotlin-coroutinesin-perde-94.png
---

Kotlin’de `suspend` anahtar sözcüğünü gördüğümüzde kodun sihirli biçimde arka plana taşındığını düşünebiliriz. Oysa coroutine’lerin asıl numarası yeni bir thread oluşturmak değil, çalışmayı uygun noktalarda durdurup daha sonra kaldığı yerden sürdürebilmektir. Kotlin derleyicisi bunu gerçekleştirmek için askıya alınabilen fonksiyonları birer **durum makinesine**, yani state machine’e dönüştürür.
``
## Askıya alınmak, thread’i bloke etmek değildir

Bloklayan bir çağrıda thread, işlem tamamlanana kadar bekler ve başka iş yapamaz. Askıya alınan coroutine ise mevcut durumunu kaydeder, thread’i serbest bırakır ve sonuç hazır olduğunda uygun bir thread üzerinde devam eder.

| Özellik | Bloklayan işlem | Askıya alınan coroutine |
|---|---|---|
| Thread durumu | Bekler ve meşgul kalır | Başka işlere ayrılabilir |
| Devam bilgisi | Çağrı yığınında tutulur | `Continuation` nesnesinde tutulur |
| Ölçeklenebilirlik | Çok sayıda thread gerektirebilir | Az sayıda thread ile çok iş yönetebilir |
| Örnek | `Thread.sleep(1000)` | `delay(1000)` |

Basitleştirilmiş olarak toplam çalışma süresini şöyle düşünebiliriz:

$$T_{bloklayan} = T_{işlem} + T_{thread\ bekleme}$$

Coroutine yaklaşımında thread’in boşa beklediği bölüm kaldırılır:

$$T_{coroutine} \approx T_{işlem}, \qquad T_{thread\ bekleme} \approx 0$$

Bu, dış işlemin daha hızlı tamamlandığı anlamına gelmez; yalnızca bekleme süresince işlemci ve thread kaynakları daha verimli kullanılır.

## Basit bir suspend fonksiyonu

Aşağıdaki fonksiyon iki farklı askıya alınma noktası içerir:

```kotlin
suspend fun kullaniciOzeti(id: Int): String {
    val kullanici = kullaniciGetir(id)
    val siparisler = siparisleriGetir(kullanici.id)
    return "${kullanici.ad}: ${siparisler.size} sipariş"
}
```

`kullaniciGetir` ve `siparisleriGetir` askıya alınabiliyorsa fonksiyonun üç mantıksal durumu oluşur:

1. Kullanıcı alınmadan önce,
2. Kullanıcı alındıktan, siparişler alınmadan önce,
3. İki işlem de tamamlandıktan sonra.

Derleyici, fonksiyona görünmez bir `Continuation` parametresi ekler. Continuation, işlemin sonucunun nereye gönderileceğini ve fonksiyonun hangi durumdan devam edeceğini temsil eder. Dönüş tipi kaynak kodda `String` görünse de JVM seviyesindeki sadeleştirilmiş biçim yaklaşık olarak şöyledir:

```kotlin
fun kullaniciOzeti(
    id: Int,
    continuation: Continuation<String>
): Any?
```

`Any?` kullanılmasının nedeni fonksiyonun ya gerçek sonucu ya da özel `COROUTINE_SUSPENDED` işaretini döndürebilmesidir.

## Derleyicinin ürettiği durum makinesi

Gerçek bytecode daha karmaşıktır; ancak dönüşümün mantığı şu sözde Kotlin koduyla görülebilir:

```kotlin
when (continuation.label) {
    0 -> {
        continuation.id = id
        continuation.label = 1
        val sonuc = kullaniciGetir(id, continuation)
        if (sonuc === COROUTINE_SUSPENDED) return sonuc
    }
    1 -> {
        val kullanici = continuation.result as Kullanici
        continuation.kullanici = kullanici
        continuation.label = 2
        val sonuc = siparisleriGetir(kullanici.id, continuation)
        if (sonuc === COROUTINE_SUSPENDED) return sonuc
    }
    2 -> {
        val siparisler = continuation.result as List<Siparis>
        return "${continuation.kullanici.ad}: ${siparisler.size} sipariş"
    }
}
```

Buradaki `label`, program sayacı gibi davranır. Coroutine yeniden çağrıldığında fonksiyon baştan çalışıyor gibi görünse de `when` doğru dala atlayarak son askıya alınma noktasından devam eder. Askıya alınma sonrasında gerekli olacak `kullanici` gibi yerel değişkenler de continuation nesnesinin alanlarına taşınır. Bu işleme bazen değişkenlerin **spill edilmesi** denir.

## Continuation Passing Style

Bu dönüşüm, **Continuation Passing Style** veya CPS yaklaşımına dayanır. Normal bir fonksiyon sonucu doğrudan çağırana döndürürken CPS biçimindeki fonksiyon, sonraki adımı temsil eden continuation’ı taşır:

$$f(x) \rightarrow y$$

yerine:

$$f(x, k) \rightarrow k(y)$$

Buradaki $k$, sonuç hazır olduğunda yürütülecek devam işlemidir. Dispatcher ise bu devamın hangi thread veya thread havuzunda çalışacağını belirleyebilir.

Sonuç olarak `suspend`, “arka planda çalıştır” komutu değildir. Derleyiciye, fonksiyonun bölünebilir olduğunu söyleyen bir işarettir. Kotlin’in zarif görünen sıralı kodu; continuation nesneleri, durum etiketleri ve özel askıya alınma işaretleri sayesinde thread bloke etmeden asenkron bir koreografiye dönüşür.

![kotlin-coroutinesin-perde-94](/img/kotlin-coroutinesin-perde-94.svg)

