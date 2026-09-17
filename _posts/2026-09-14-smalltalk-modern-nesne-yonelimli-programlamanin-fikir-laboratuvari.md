---
layout: post
title: "Smalltalk: Modern Nesne Yönelimli Programlamanın Fikir Laboratuvarı"
math: true
categories: 
  - Bilgi
tags: 
  - smalltalk
  - nesne yönelimli programlama
  - oop
  - programlama tarihi
  - mesajlaşma
  - mvc
toc: true
image: /img/smalltalk-modern-nesne-15.png
---

Bugün sınıflardan, nesnelerden veya kullanıcı arayüzlerinden söz ederken kullandığımız birçok kavramın izi Smalltalk’a çıkar. Xerox PARC’ta Alan Kay, Dan Ingalls, Adele Goldberg ve ekip arkadaşları tarafından geliştirilen Smalltalk, nesne yönelimliliği yalnızca bir programlama tekniği olarak değil, bilgisayarla iletişim kurmanın bütüncül bir modeli olarak ele aldı.


![smalltalk-modern-nesne-15](/img/smalltalk-modern-nesne-15.svg)

``

## Her şey nesnedir

Smalltalk’ın en güçlü ilkesi şaşırtıcı derecede sadedir: **Sistemdeki her şey bir nesnedir.** Sayılar, metinler, sınıflar, kod blokları ve hatta çalışma bağlamları aynı modelin parçalarıdır. Başka dillerde özel sözdizimiyle gerçekleştirilen işlemler Smalltalk’ta nesneler arası mesajlaşmaya dönüşür.

Örneğin matematiksel olarak

$$3 + 4 = 7$$

ifadesindeki `+`, Smalltalk açısından sihirli bir operatör değildir. `3` nesnesine `+` mesajı, `4` argümanıyla gönderilir:

```smalltalk
3 + 4
```

Burada mesajı alan nesne `3`, mesajın seçicisi `+`, argüman ise `4` olur. Bu bakış açısı, programı emirler listesinden çok iş birliği yapan nesneler topluluğuna dönüştürür.

## Metot çağrısı değil, mesaj gönderimi

Alan Kay’in nesne yönelimlilik anlayışında asıl yıldız sınıflar değil **mesajlaşmadır**. Gönderici, alıcının mesajı nasıl işleyeceğini bilmez. Böylece nesnenin iç yapısı saklanır ve davranış uygulama ayrıntılarından ayrılır.

| Geleneksel yaklaşım | Smalltalk yaklaşımı |
|---|---|
| Fonksiyon çağrılır | Nesneye mesaj gönderilir |
| Veri ve işlem ayrılabilir | Veri ile davranış nesnede birleşir |
| Tür ayrıntısı çağıranı etkileyebilir | Alıcının uygun mesajı yanıtlaması yeterlidir |
| Erken bağlama yaygındır | Geç bağlama temel davranıştır |

Bir mesajın hangi metodu çalıştıracağı çalışma anındaki alıcıya göre belirlenir. Bunu kavramsal olarak şöyle gösterebiliriz:

$$metot = lookup(sınıf(alıcı), mesaj)$$

Bu mekanizma, günümüzde **dinamik gönderim** ve **polimorfizm** dediğimiz yaklaşımın berrak örneklerinden biridir.

## Sınıflar da nesnedir

Smalltalk’ın radikal katkılarından biri, sınıfları dilin dışında duran şablonlar olarak görmemesidir. Sınıflar da mesaj alabilen nesnelerdir ve metaclass adı verilen sınıfların örnekleridir. İlk karşılaşmada biraz “sınıfın da sınıfı mı olurmuş?” hissi uyandırsa da sistemin tutarlılığını sağlar.

Aşağıdaki örnek basit bir sayaç tanımlar:

```smalltalk
Object subclass: #Counter
    instanceVariableNames: 'value'
    classVariableNames: ''
    package: 'Examples'.

Counter >> initialize
    value := 0.

Counter >> increment
    value := value + 1.

Counter >> value
    ^ value
```

`initialize` başlangıç değerini kurar, `increment` sayacı artırır, `value` ise mevcut değeri döndürür. Nesnenin içindeki `value` değişkenine dışarıdan doğrudan dokunmak yerine davranış üzerinden erişilir. Bu, kapsüllemenin pratik karşılığıdır.

## Canlı sistem ve image fikri

Smalltalk programı yalnızca dosyalardan derlenen ölü bir metin değildir. **Image**, çalışan sistemin nesneleriyle birlikte kaydedilmiş hâlidir. Geliştirici çalışan nesneleri inceleyebilir, metotları değiştirebilir ve sonucu hemen gözlemleyebilir. Bugünkü REPL’ler, notebook ortamları, canlı kodlama araçları ve gelişmiş hata ayıklayıcılar bu yaklaşımın akrabalarıdır.

Smalltalk ortamında debugger yalnızca hatayı göstermez; askıya alınmış çalışmayı inceleyip metodu düzelterek devam etmeye imkân tanır. Programlama böylece “yaz, derle, yeniden başlat” döngüsünden çıkarak canlı bir sohbete yaklaşır.

## MVC ve geliştirme araçları

Model–View–Controller yaklaşımı da Smalltalk dünyasında şekillendi. Model veriyi ve kuralları, View sunumu, Controller kullanıcı etkileşimini yönetir. Bu ayrım daha sonra masaüstü, web ve mobil uygulama mimarilerini derinden etkiledi.

Smalltalk ayrıca sınıf tarayıcısı, nesne denetleyicisi, bütünleşik debugger ve refactoring kültürüyle modern IDE’lerin temel beklentilerini erkenden sergiledi. Simula sınıf ve kalıtım konusunda tarihsel öncüydü; Smalltalk ise bu fikirleri mesajlaşma, canlı ortam ve tutarlı nesne modeliyle bir programlama evrenine dönüştürdü. Kısacası Smalltalk yalnızca OOP kullanan eski bir dil değil, bugün hâlâ kullandığımız birçok fikrin çalışır durumdaki laboratuvarıdır.
