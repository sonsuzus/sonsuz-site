---
layout: post
title: "Hindley-Milner Tip Çıkarımı: Tip Yazmadan Tip Güvenliği"
math: true
categories: 
  - Bilgi
tags: 
  - hindley-milner
  - tip-sistemleri
  - fonksiyonel-programlama
  - tip-çıkarımı
  - algoritma-w
toc: true
image: /img/hindley-milner-tip-79.png
---

Bir fonksiyon yazdığınızı, hiçbir parametreye tip eklemediğinizi ve derleyicinin yine de bütün tip hatalarını yakaladığını düşünün. Üstelik derleyici yalnızca kodun doğru olup olmadığını söylemekle kalmasın, mümkün olan en genel tipi de keşfetsin! Hindley-Milner, yani HM tip sistemi, fonksiyonel programlama dünyasının bu etkileyici numarasını matematiksel olarak gerçekleştirir.

``

## Temel fikir: İfadeler kısıt üretir

HM sisteminde her ifadeye başlangıçta bilinmeyen bir tip değişkeni atanabilir. Bu değişkenler genellikle $\alpha$, $\beta$ ve $\gamma$ ile gösterilir. Ardından programın yapısı incelenerek tip denklemleri oluşturulur.

Örneğin şu fonksiyonu ele alalım:

```haskell
f x = x
```

`x` için $\alpha$ tipini seçersek fonksiyon aynı tipte bir değer döndürür. Dolayısıyla:

$$f : \alpha \rightarrow \alpha$$

Buradaki $\alpha$, belirli bir tip değildir. `Int`, `String` veya başka herhangi bir tip olabilir. Bu nedenle `f`, polimorfik bir fonksiyondur.

Bir fonksiyon uygulamasında ise kural şöyledir: `f x` ifadesinin tipi $\beta$ ise `f` fonksiyonunun tipi mutlaka

$$\operatorname{type}(f) = \operatorname{type}(x) \rightarrow \beta$$

biçiminde olmalıdır. Tip çıkarımı, program boyunca bu tür denklemleri toplar ve çözer.

## Birleştirme: Tip bulmacasının motoru

Denklemleri çözme işlemine **unification**, yani birleştirme denir. Amaç, iki tipi eşit hâle getiren yer değiştirmeleri bulmaktır.

| Denklem | Sonuç | Açıklama |
|---|---|---|
| $\alpha = Int$ | $\alpha \mapsto Int$ | Değişken somutlaşır |
| $\alpha = \beta$ | $\alpha \mapsto \beta$ | İki bilinmeyen eşitlenir |
| $\alpha \to Int = Bool \to \beta$ | $\alpha = Bool$, $\beta = Int$ | Parçalar ayrı ayrı eşitlenir |
| $Int = String$ | Hata | Tipler uzlaştırılamaz |

Birleştirme sırasında önemli bir güvenlik kontrolü de **occurs check** işlemidir. Örneğin $\alpha = \alpha \to \beta$ eşitliğine izin verilirse sonsuz bir tip oluşur. HM bunu reddeder; matematiksel canavarların programa sızmasına müsaade etmez.

## Algorithm W nasıl çalışır?

HM tip çıkarımının klasik uygulaması **Algorithm W** olarak bilinir. Algoritma, sözdizimi ağacını dolaşırken hem bir tip hem de bulunan tip eşitliklerini temsil eden bir substitution üretir.

Aşağıdaki sadeleştirilmiş Python kodu, fonksiyon uygulamasının mantığını gösterir:

```python
def infer_application(env, function, argument):
    # Fonksiyonun ve argümanın tiplerini ayrı ayrı çıkar.
    s1, function_type = infer(env, function)
    s2, argument_type = infer(apply_env(s1, env), argument)

    # Uygulamanın henüz bilinmeyen sonuç tipi.
    result_type = fresh_type_variable()

    # Fonksiyon tipi, argüman -> sonuç biçimiyle eşleşmelidir.
    s3 = unify(
        apply_type(s2, function_type),
        FunctionType(argument_type, result_type)
    )

    substitution = compose(s3, compose(s2, s1))
    return substitution, apply_type(s3, result_type)
```

Burada `fresh_type_variable` yeni bir tip değişkeni oluşturur. `unify` gerekli eşleştirmeleri bulur, `compose` ise farklı aşamalarda bulunan sonuçları birleştirir. Böylece çıkarım yerel tahminlerden tutarlı bir genel sonuca ilerler.

## Let-polimorfizmi neden önemlidir?

HM sisteminin güçlü taraflarından biri `let` ile tanımlanan değerleri **genelleştirmesidir**:

```haskell
let identity = \x -> x
in (identity 42, identity "merhaba")
```

`identity` yalnızca tek bir bilinmeyen tipe sabitlenmez. Tipi $\forall \alpha.\alpha \to \alpha$ olarak genelleştirilir ve her kullanımda yeni değişkenlerle örneklenir. Böylece aynı fonksiyon hem sayı hem metin üzerinde güvenle kullanılabilir.

| Yaklaşım | Tip anotasyonu | Hataları yakalama | Polimorfizm |
|---|---:|---:|---:|
| Dinamik tipleme | Gerekmez | Çalışma zamanında | Doğal fakat dinamik |
| Açık statik tipleme | Genellikle gerekir | Derleme zamanında | Sisteme bağlı |
| Hindley-Milner | Çoğunlukla gerekmez | Derleme zamanında | Otomatik ve genel |

HM kusursuz değildir; alt tipleme, gelişmiş nesne modelleri ve bazı yan etkiler sistemi karmaşıklaştırır. Yine de ML, OCaml ve Haskell gibi dillerin temelinde yer alarak önemli bir denge kurar: geliştirici az tip yazar, derleyici çok düşünür ve hatalı programlar üretime çıkmadan kapıda yakalanır.

![hindley-milner-tip-79](/img/hindley-milner-tip-79.svg)

