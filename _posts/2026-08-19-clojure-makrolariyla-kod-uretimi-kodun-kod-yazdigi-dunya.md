---
layout: post
title: "Clojure Makrolarıyla Kod Üretimi: Kodun Kod Yazdığı Dünya"
math: true
categories: 
  - Bilgi
tags: 
  - clojure
  - makrolar
  - meta programlama
toc: true
image: /img/clojure-makrolariyla-kod-80.png
---

![clojure-makrolariyla-kod-80](/img/clojure-makrolariyla-kod-80.svg)


Clojure makroları, programın çalıştırdığı değerleri değil, programın kendisini dönüştürmenizi sağlar. Bu fikir ilk bakışta sihirli görünse de temelinde oldukça somut bir gerçek vardır: Clojure kodu, Lisp ailesinden geldiği için veri yapılarıyla aynı biçimde yazılır. Böylece bir fonksiyon çağrısı olan `(topla 2 3)` aynı zamanda liste olarak okunabilir; makro da bu listeyi alır, değiştirir ve derleyicinin işleyeceği yeni kodu üretir.
``

## Fonksiyon mu, makro mu?

Fonksiyonlar **çalışma zamanında** çağrılır; argümanları daha fonksiyona ulaşmadan değerlendirilmiştir. Makrolar ise **derleme/genişletme aşamasında** çalışır ve argümanlarını ham Clojure formları olarak görür. Bu ayrım, kontrol yapıları veya küçük alan-özgü diller (DSL) tasarlarken kritik önemdedir.

| Özellik | Fonksiyon | Makro |
|---|---|---|
| Ne zaman çalışır? | Çalışma zamanında | Kod derlenirken/genişletilirken |
| Argümanları görme biçimi | Değerlendirilmiş değerler | Değerlendirilmemiş formlar |
| Ana kullanım alanı | Veri işleme | Yeni sözdizimi ve kod şablonları |
| Örnek | `map`, `reduce` | `when`, `->`, `cond` |

Örneğin `when`, koşul doğruysa gövdeyi çalıştıran yerleşik bir makrodur. Bunu sıradan bir fonksiyonla tam olarak taklit edemezsiniz; çünkü gövdenin koşul yanlışken hiç değerlendirilmemesi gerekir. Teorik olarak makro, kaynak formu $S$ alır ve başka bir form olan $T(S)$ üretir. Ardından Clojure bu yeni formu normal kod gibi derler. Yani akış kabaca şöyledir: $\text{okuma} \rightarrow \text{macroexpand} \rightarrow \text{derleme} \rightarrow \text{çalıştırma}$.

## İlk makro: Kontrollü günlük kaydı

Aşağıdaki `log-value`, bir ifadeyi yalnızca bir kez değerlendirir; hem ifadeyi hem sonucunu ekrana yazar ve sonucu çağırana geri döndürür.

```clojure
(defmacro log-value [expr]
  `(let [result# ~expr]
     (println "Çalışan ifade:" '~expr)
     (println "Sonuç:" result#)
     result#))

(log-value (+ 10 32))
;; Çalışan ifade: (+ 10 32)
;; Sonuç: 42
;; => 42
```

Burada ters tırnak olan syntax quote, şablon oluşturur. `~expr` ile makronun aldığı form şablona yerleştirilir; buna **unquote** denir. `'~expr` ise ifadeyi veri olarak tutarak ekrana kaynak biçiminde yazdırır. `result#` ise otomatik benzersiz bir sembol üretir. Bu küçük `#`, makro yazarken çok büyük bir kazayı engeller: çağıranın değişken adını istemeden ezmeyi.

## Hijyen: Görünmez isim çarpışmalarından kaçınmak

Makrolar yeni yerel değişkenler tanıttığında isim çakışması doğabilir. Buna makro hijyeni problemi denir. Kötü yazılmış bir makro, kullanıcının `result` değişkenini yanlışlıkla gölgeleyebilir. Clojure makroları bütünüyle otomatik hijyenik değildir; ancak syntax quote içindeki `isim#` yaklaşımı güvenli, benzersiz adlar üretir.

```clojure
(defmacro unless [test & body]
  `(if (not ~test)
     (do ~@body)))

(unless (= 2 3)
  (println "Matematik bugün de çalışıyor!"))
```

`& body` kalan tüm formları toplar. `~@body` ise bu formları tek bir liste olarak koymak yerine `do` bloğuna açar; bu işleme **splice unquote** adı verilir. Sonuçta `unless`, Clojure'a küçük ama okunabilir bir yeni yapı eklemiş olur.

## Makronun ürettiği kodu görmek

Makroları anlamanın en iyi yolu, ürettikleri kodu incelemektir. `macroexpand-1` bir genişletme adımını gösterir:

```clojure
(macroexpand-1
 '(unless (= 2 3)
    (println "Merhaba")))
;; (if (clojure.core/not (= 2 3))
;;   (do (println "Merhaba")))
```

Makro yazarken önce fonksiyonla çözmenin mümkün olup olmadığını sorun. Veri dönüşümü, hesaplama ve tekrar kullanılabilir iş mantığı için fonksiyonlar daha basit, test edilebilir ve öngörülebilirdir. Makroyu; değerlendirme sırasını değiştirmek, kod tekrarını yapısal olarak azaltmak veya anlamlı bir DSL kurmak gerektiğinde seçin. İyi bir makro sürpriz yaratmaz: az kod üretir, genişletildiğinde okunur ve kullanıcıdan gizlediği karmaşıklık kadar gerçek değer sağlar.
