---
layout: post
title: "Lisp ve Scheme’de Kod Veridir: Homoiconicity Neden Hâlâ Önemli?"
math: true
categories: 
  - Bilgi
tags: 
  - lisp
  - scheme
  - homoiconicity
toc: true
image: /img/lisp-ve-schemede-23.png
---

Bir Lisp programına ilk kez bakanların ortak tepkisi genellikle şudur: “Bu kadar parantez gerçekten gerekli mi?” Bir süre sonra parantezlerin süs değil, dilin temel fikrinin görünür hâli olduğu anlaşılır. Lisp ailesinde programlar, dilin sıradan veri yapılarıyla temsil edilir. Kısacası kod ile veri aynı kıyafeti giyer; buna **homoiconicity** denir.

``

## Homoiconicity tam olarak nedir?

Homoiconic bir dilde kaynak kodun yapısı, programın doğrudan işleyebildiği veri yapılarıyla eşleşir. Scheme’de listeler nasıl yazılıyorsa fonksiyon çağrıları da aynı biçimde yazılır:

```scheme
(+ 2 3)
```

Bu ifade yalnızca “toplama işlemi” değildir. Aynı zamanda üç elemanlı bir liste olarak düşünülebilir:

```scheme
(list '+ 2 3)
```

Başındaki tek tırnak, ifadenin çalıştırılmasını engelleyerek onu veri hâlinde tutar:

```scheme
(define ifade '(+ 2 3))
(car ifade)   ; +
(cadr ifade)  ; 2
```

Buradaki zihinsel model şu eşitlikle özetlenebilir:

$$\text{Program gösterimi} \approx \text{Dil içindeki veri gösterimi}$$

Bu, kod ile verinin tamamen aynı kavram olduğu anlamına gelmez. Kod, değerlendirme bağlamına girdiğinde davranış kazanır; alıntılandığında ise üzerinde dolaşılabilen ve dönüştürülebilen bir veri yapısıdır.

| Özellik | Geleneksel sözdizimi | Lisp/Scheme yaklaşımı |
|---|---|---|
| Fonksiyon çağrısı | `topla(2, 3)` | `(+ 2 3)` |
| Kodun temsili | Ayrı bir AST gerekir | Liste yapısına çok yakındır |
| Dönüştürme | Parser ve araç zinciri ister | Liste işlemleriyle yapılabilir |
| Dil genişletme | Genellikle sınırlıdır | Makrolarla doğaldır |

## Parantezler aslında görünür AST’dir

Derleyiciler kaynak kodu çoğunlukla bir **soyut sözdizimi ağacına** (AST) çevirir. Örneğin `2 + 3 * 4` ifadesinin ağacında çarpma, toplamadan daha aşağıda yer alır. Lisp’te bu hiyerarşi doğrudan yazılır:

```scheme
(+ 2 (* 3 4))
```

Matematiksel olarak sonuç:

$$2 + (3 \times 4) = 14$$

Dolayısıyla öncelik kurallarını ezberlemek yerine ağacı yazarsınız. Parantezler kalabalık yapmak için değil, programın yapısını tartışmasız biçimde belirtmek için oradadır.

## Kod üreten kod: makrolar

Homoiconicity’nin en güçlü sonucu makrolardır. Makro, çalışma zamanında çağrılan sıradan bir fonksiyon değildir; kodu çalıştırılmadan önce başka bir koda dönüştürür.

```scheme
(define-syntax when
  (syntax-rules ()
    ((_ condition body ...)
     (if condition
         (begin body ...)))))

(when (> 7 3)
  (display "Koşul doğru!")
  (newline))
```

Buradaki `when`, yeni bir kontrol yapısı gibi görünür fakat sonuçta `if` ve `begin` kullanan Scheme koduna genişletilir. `syntax-rules` ayrıca hijyenik makro desteği sunar; makronun ürettiği isimlerin kullanıcı değişkenleriyle yanlışlıkla çakışmasını önler.

| Fonksiyon | Makro |
|---|---|
| Değerleri alır | Kod biçimlerini alır |
| Çalışma zamanında işler | Genişletme aşamasında işler |
| Sonuç üretir | Yeni kod üretir |
| Değerlendirme sırasını kolayca değiştiremez | Yeni kontrol yapıları kurabilir |

## Neden bugün hâlâ önemli?

Modern yazılım geliştirme; AST dönüşümleri, kod üreticileri, derleyici eklentileri ve alan odaklı dillerle doludur. JSX, şablon sistemleri, ORM sorguları ve build araçları özünde “programı veri olarak ele alma” fikrine yaklaşır. Lisp bunu sonradan eklenen bir araç yerine dilin merkezine yerleştirir.

Bu yaklaşım; tekrarlanan kalıpları soyutlamayı, projeye özel küçük diller geliştirmeyi ve derleme zamanında doğrulama yapmayı kolaylaştırır. Ancak `eval` ile rastgele veri çalıştırmak güvenlik riski taşır. Homoiconicity’nin değeri her şeyi dinamik olarak çalıştırmak değil, program yapısını güvenli ve sistematik biçimde dönüştürebilmektir.

Sonuç olarak Lisp’in parantezleri geçmişten kalma tuhaflıklar değildir. Onlar, kodun incelenebilir, üretilebilir ve dönüştürülebilir veri olduğunu gösteren açık bir arayüzdür. Bugünün metaprogramlama araçları değişse de bu fikir hâlâ şaşırtıcı derecede moderndir.

![lisp-ve-schemede-23](/img/lisp-ve-schemede-23.svg)

