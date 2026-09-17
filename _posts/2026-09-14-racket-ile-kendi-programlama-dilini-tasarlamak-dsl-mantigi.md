---
layout: post
title: "Racket ile Kendi Programlama Dilini Tasarlamak: DSL Mantığı"
math: true
categories: 
  - Proje
tags: 
  - racket
  - dsl
  - programlama-dilleri
  - makrolar
  - scheme
  - lang
toc: true
image: /img/racket-ile-kendi-62.png
---

Bir robotu hareket ettirmek için yüzlerce satırlık genel amaçlı kod yazmak yerine `move 5` ve `turn left` gibi ifadeler kullanabilseydik nasıl olurdu? Etki alanına özgü dil, yani DSL (Domain-Specific Language), belirli bir problem alanını doğal ve güvenli biçimde ifade etmek için tasarlanır. Racket ise güçlü makro sistemi, sözdizimi nesneleri ve `#lang` mekanizması sayesinde küçük bir dili sıfırdan üretmek için adeta programlama dilleri laboratuvarıdır.

![racket-ile-kendi-62](/img/racket-ile-kendi-62.svg)

``
## DSL tam olarak nedir?

Genel amaçlı diller birçok problemi çözmeye çalışırken DSL yalnızca belirli bir alana odaklanır. SQL veri sorgular, düzenli ifadeler metin desenlerini tanımlar, HTML ise belge yapısını ifade eder. Bir DSL'nin değerini kabaca şöyle düşünebiliriz:

$$
D = \frac{A \times O}{K}
$$

Burada $A$ anlatım gücünü, $O$ problem alanına uygunluğu, $K$ ise öğrenme karmaşıklığını temsil eder. Başarılı bir DSL, gereksiz genel amaçlı özellikleri azaltırken alanın kavramlarını doğrudan sunar.

| Özellik | Genel amaçlı dil | DSL |
|---|---|---|
| Kapsam | Çok geniş | Belirli bir alan |
| Sözdizimi | Teknik ve genel | Alan terimlerine yakın |
| Esneklik | Yüksek | Kontrollü |
| Öğrenme maliyeti | Genellikle yüksek | Hedef kullanıcı için düşük |
| Örnek | Racket, Python | SQL, robot komut dili |

## Racket neden uygun?

Racket'ta program kodu da liste tabanlı bir veri yapısıdır. Bu özellik, yani homoikoniklik, kodu kodla dönüştürmeyi kolaylaştırır. Makrolar yalnızca metin değiştirmez; derleme sırasında sözdizimi nesneleri üzerinde çalışır ve hijyenik oldukları için değişken isimlerinin yanlışlıkla çakışmasını önler.

İlk olarak robot komutlarımızı sağlayan `robot-dsl.rkt` dosyasını oluşturalım:

```racket
#lang racket

(provide
 (except-out (all-from-out racket) #%module-begin)
 (rename-out [dsl-module-begin #%module-begin])
 move turn repeat)

(struct robot (position direction) #:transparent)
(define current-robot
  (make-parameter (robot 0 'north)))

(define (perform-move distance)
  (define r (current-robot))
  (current-robot
   (robot (+ (robot-position r) distance)
          (robot-direction r))))

(define (perform-turn direction)
  (define r (current-robot))
  (current-robot
   (robot (robot-position r) direction)))

(define-syntax-rule (move distance)
  (perform-move distance))

(define-syntax-rule (turn direction)
  (perform-turn 'direction))

(define-syntax-rule (repeat count command ...)
  (for ([i (in-range count)])
    command ...))

(define-syntax-rule (dsl-module-begin form ...)
  (#%plain-module-begin
   (parameterize ([current-robot (robot 0 'north)])
     form ...
     (displayln (current-robot)))))
```

Bu dosyada `move`, `turn` ve `repeat` dilimizin kelimeleridir. `define-syntax-rule`, kullanıcının yazdığı ifadeleri standart Racket koduna dönüştürür. Örneğin `(move 4)` ifadesi derleme sırasında `(perform-move 4)` biçimini alır. Özel `#%module-begin` tanımı ise programın başlangıç durumunu kurar ve komutlar tamamlandığında robotun son durumunu gösterir.

## Tasarladığımız dili kullanmak

Şimdi `rota.rkt` adlı ikinci bir dosya hazırlayabiliriz:

```racket
#lang s-exp "robot-dsl.rkt"

(move 3)
(turn east)
(repeat 2
  (move 4))
```

Program çalıştırıldığında robotun konumu $3 + 2 \times 4 = 11$ olur ve yönü `east` olarak görünür:

```text
#(struct:robot 11 east)
```

`#lang s-exp`, parantezli Racket sözdizimini korurken dilin anlamını bizim modülümüzden alır. Tamamen farklı, örneğin parantezsiz bir sözdizimi isteseydik özel bir reader yazarak metni sözdizimi nesnelerine çevirmemiz gerekirdi.

## İyi bir DSL için tasarım ilkeleri

Komutlar problem alanının diliyle konuşmalı, hatalar erken yakalanmalı ve kullanıcı gereksiz ayrıntılardan korunmalıdır. Örneğin negatif hareketi yasaklamak için `perform-move` içinde sözleşme kontrolü eklenebilir. Yönler de yalnızca `north`, `south`, `east` ve `west` ile sınırlandırılabilir.

Racket'ta DSL geliştirmek, yalnızca yeni komutlar tanımlamak değildir; ayrıştırma, dönüşüm, çalışma zamanı ve hata mesajları gibi bir dilin temel katmanlarını öğrenmektir. Küçük robot dilimiz oyuncak gibi görünse de aynı yaklaşım test senaryoları, yapılandırma sistemleri, oyun görevleri ve veri işleme boru hatları tasarlamak için kullanılabilir.
