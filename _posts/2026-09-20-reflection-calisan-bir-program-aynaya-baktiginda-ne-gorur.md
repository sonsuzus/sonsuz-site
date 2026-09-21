---
layout: post
title: "Reflection: Çalışan Bir Program Aynaya Baktığında Ne Görür?"
math: true
categories: 
  - Bilgi
tags: 
  - reflection
  - programlama
  - java
  - python
  - metaprogramlama
  - runtime
toc: true
image: /img/reflection-calisan-bir-37.png
---

Bir programın çalışırken kendi sınıflarını, metotlarını ve alanlarını inceleyebilmesi kulağa bilim kurgu gibi gelebilir. Oysa **reflection**, modern programlama dillerinde test araçlarından web çatılarının otomatik yapılandırmasına kadar pek çok sistemin görünmez kahramanıdır. Program aynaya bakıp “Ben hangi türüm, hangi yeteneklere sahibim?” diye sorar; reflection API’si de ona cevap verir.
``
## Reflection tam olarak nedir?

Normalde kaynak kod yazılırken hangi sınıfın hangi metodunun çağrılacağı bellidir. Reflection kullanıldığında ise bu bilgi çalışma zamanında, yani **runtime** sırasında keşfedilebilir. Program; bir nesnenin türünü öğrenebilir, metot listesini çıkarabilir, annotation bilgilerini okuyabilir ve izin verildiğinde üyeleri dinamik olarak çağırabilir.

Bunu kabaca şu fonksiyonla ifade edebiliriz:

$$R(o) = \{T, F, M, A\}$$

Burada $o$ incelenen nesne, $T$ tür bilgisi, $F$ alanlar, $M$ metotlar ve $A$ annotation ya da benzeri metadata bilgileridir. Reflection nesnenin iş verisini değil, çoğunlukla onu tanımlayan **metadata** katmanını araştırır.

İki temel kavramı ayırmak faydalıdır:

- **Introspection:** Programın yapısını okuması ve anlamasıdır.
- **Intercession:** Programın davranışa müdahale etmesi; örneğin bir metodu dinamik çağırmasıdır.

| Yaklaşım | Bilgi ne zaman belirlenir? | Avantaj | Dezavantaj |
|---|---|---|---|
| Doğrudan çağrı | Derleme sırasında | Hızlı ve güvenli | Daha az esnek |
| Reflection | Çalışma sırasında | Dinamik ve genişletilebilir | Daha yavaş, hata riski yüksek |
| Kod üretimi | Derleme veya kurulum sırasında | Performanslı otomasyon | Araç zinciri karmaşık olabilir |

![reflection-calisan-bir-37](/img/reflection-calisan-bir-37.svg)


## Java ile çalışma zamanında keşif

Java’nın `Class` API’si, reflection için ana giriş kapısıdır. Aşağıdaki örnek, bir sınıftaki herkese açık metotları keşfeder ve parametresiz olanlardan seçtiğini çalıştırır:

```java
import java.lang.reflect.Method;

class Robot {
    public void selamVer() {
        System.out.println("Merhaba, insan!");
    }
}

public class ReflectionDemo {
    public static void main(String[] args) throws Exception {
        Robot robot = new Robot();
        Class<?> tur = robot.getClass();

        System.out.println("Tür: " + tur.getName());

        for (Method metot : tur.getDeclaredMethods()) {
            System.out.println("Bulundu: " + metot.getName());

            if (metot.getName().equals("selamVer")
                    && metot.getParameterCount() == 0) {
                metot.invoke(robot);
            }
        }
    }
}
```

`getClass()` gerçek çalışma zamanı türünü verir. `getDeclaredMethods()` sınıfın tanımladığı metotları listeler, `invoke()` ise seçilen metodu ilgili nesne üzerinde çağırır. Böylece metodun adı kaynak kodda doğrudan çağrı biçiminde kullanılmadan davranış tetiklenir.

## Python’da aynı ayna

Dinamik yapısı nedeniyle Python’da iç gözlem daha doğal görünür. `inspect` modülü, üyeleri düzenli biçimde araştırmayı sağlar:

```python
import inspect

class Robot:
    def selam_ver(self):
        return "Merhaba, insan!"

robot = Robot()

for ad, uye in inspect.getmembers(robot, predicate=inspect.ismethod):
    if ad == "selam_ver":
        print(ad, uye())
```

Burada `getmembers`, nesnenin üyelerini getirir; `ismethod` ise sonuçları metotlarla sınırlar. Java’daki daha resmî reflection mekanizmasına karşılık Python, dilin dinamik doğasını kullanır.

## Nerelerde kullanılır?

Reflection özellikle bağımlılık enjeksiyonu, ORM, serileştirme, test keşfi, eklenti sistemleri ve annotation tabanlı yönlendirme için kullanılır. Örneğin bir test aracı, adı `test_` ile başlayan metotları keşfedip otomatik çalıştırabilir. Bir web çatısı da belirli annotation taşıyan sınıfları denetleyerek URL rotaları oluşturabilir.

Fakat esnekliğin bedeli vardır. Reflection işlemlerinin yaklaşık maliyetini şöyle düşünebiliriz:

$$C_{toplam} = C_{arama} + C_{erişim} + C_{cağrı}$$

Doğrudan çağrıda arama maliyeti genellikle yoktur. Ayrıca yanlış metot adı, uyumsuz parametre veya erişim kısıtı ancak çalışma sırasında hata verebilir. Bu nedenle sonuçları önbelleğe almak, kullanıcı girdisini doğrudan metot adına dönüştürmemek ve mümkün olduğunda standart arayüzleri tercih etmek önemlidir.

Reflection güçlü bir tornavidadır; çekiç gibi her yerde kullanılmamalıdır. Altyapı, araç veya genişletilebilir mimari geliştirirken harikalar yaratır. Sıradan iş mantığında aşırı kullanıldığında ise kodu gizemli bir kaçış odasına çevirebilir.
