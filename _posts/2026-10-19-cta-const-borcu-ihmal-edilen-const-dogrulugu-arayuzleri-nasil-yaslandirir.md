---
layout: post
title: "C++’ta Const Borcu: İhmal Edilen const Doğruluğu Arayüzleri Nasıl Yaşlandırır?"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - const-correctness
  - api-tasarımı
  - yazılım-mimarisi
  - teknik-borç
toc: true
image: /img/cta-const-borcu-47.png
---

C++’ta `const`, yalnızca derleyiciyi memnun eden küçük bir anahtar kelime değildir; bir arayüzün hangi işlemleri garanti ettiğini anlatan sözleşmedir. Bugün atlanan bir `const`, kodu hemen bozmayabilir. Ancak proje büyüdükçe yeniden kullanım, eşzamanlılık ve geriye dönük uyumluluk gibi alanlarda faiz işleyen bir tasarım borcuna dönüşür.
``
## Const doğruluğu gerçekte ne söyler?

Bir nesneye `const` erişim, gözlemlenebilir durumunun değiştirilmeyeceği sözünü verir. Üye fonksiyonun sonundaki `const` ise bu sözün fonksiyon arayüzündeki karşılığıdır:

```cpp
class User {
public:
    const std::string& name() const {
        return name_;
    }

private:
    std::string name_;
};
```

Burada ilk `const`, döndürülen referans üzerinden metnin değiştirilemeyeceğini; ikinci `const` ise `name()` çağrısının `User` nesnesini değiştirmediğini belirtir. İki kullanım farklı soruları yanıtlar: “Sonuç değiştirilebilir mi?” ve “İşlem nesneyi değiştiriyor mu?”

Bunu kabaca bir durum geçişiyle ifade edebiliriz. Salt okunur işlem için beklenen ilişki:

$$f(S) = (R, S)$$

Burada $S$ nesnenin başlangıç durumu, $R$ sonuçtur. Değiştirici bir işlemdeyse yeni durum $S'$ oluşabilir:

$$g(S) = (R, S'), \quad S' \neq S$$

`const`, ilk davranışı tür sistemi seviyesinde ilan eder ve derleyicinin bu sözleşmeyi denetlemesini sağlar.

## Küçük ihmal, büyük arayüz problemi

Aşağıdaki fonksiyon nesneyi değiştirmese bile `const` olarak işaretlenmemiştir:

```cpp
class Report {
public:
    std::string summary() { // Aslında değişiklik yapmıyor
        return title_ + ": " + body_;
    }

private:
    std::string title_;
    std::string body_;
};
```

Bu eksiklik yüzünden `const Report&` alan kodlar `summary()` metodunu çağıramaz. Sorunu geçici olarak aşmak isteyen geliştiriciler nesneleri gereksiz yere kopyalayabilir, parametrelerden `const` niteliğini kaldırabilir veya daha kötüsü `const_cast` kullanabilir. Böylece yerel bir ihmal, çağrı zinciri boyunca yayılır.

| Tasarım tercihi | Kısa vadeli sonuç | Uzun vadeli etki |
|---|---|---|
| Doğru `const` kullanımı | Biraz daha dikkat gerektirir | Açık sözleşme ve geniş kullanım alanı |
| `const` kullanımını ertelemek | Kod hızlı yazılır | API esnekliği azalır |
| `const_cast` ile aşmak | Derleme hatası susturulur | Tanımsız davranış ve bakım riski |
| Her şeyi değiştirilebilir bırakmak | Basit görünür | Eşzamanlılık analizi zorlaşır |

## Sonradan eklemek neden pahalıdır?

Bir metoda sonradan `const` eklemek kaynak kod düzeyinde küçük görünür:

```cpp
std::string summary() const;
```

Fakat gerçek projede bu değişiklik; çağrılan yardımcı metotların, kullanılan işaretçilerin ve önbelleklerin de incelenmesini gerektirir. Ayrıca üye fonksiyonun `const` niteliği türünün parçasıdır. Sanal fonksiyonlarda taban ve türetilmiş sınıfların imzaları eşleşmelidir:

```cpp
struct Document {
    virtual std::string title() const = 0;
};

struct Invoice : Document {
    std::string title() const override {
        return "Fatura";
    }
};
```

Taban sınıfa sonradan `const` eklemek, bütün türetilmiş sınıfları değiştirebilir. Paylaşılan kütüphanelerde bu durum kaynak ve ikili uyumluluk planlarını da etkiler.

## Mantıksal const ve önbellekleme

Bazen bir sorgu sonucu önbelleğe alınır. Kullanıcının gözünde nesne değişmezken içeride teknik bir güncelleme gerekir. Bunun için `mutable` bilinçli biçimde kullanılabilir:

```cpp
class Calculator {
public:
    int result() const {
        if (!cached_) {
            cache_ = expensiveCalculation();
            cached_ = true;
        }
        return cache_;
    }

private:
    int expensiveCalculation() const { return 42; }
    mutable bool cached_ = false;
    mutable int cache_ = 0;
};
```

Bu yaklaşım fiziksel değil, mantıksal değişmezliği temsil eder. Yine de `mutable`, eşzamanlı erişimi otomatik olarak güvenli yapmaz; gerekirse kilit veya atomik tür kullanılmalıdır.

## Sağlam arayüz için pratik ölçüt

Bir metot tasarlarken önce “Bu işlem nesnenin kullanıcı tarafından gözlemlenen anlamını değiştiriyor mu?” diye sorun. Yanıt hayırsa metodu `const` yapın. Parametrelerde mümkün olduğunda `const T&`, sahiplik aktarılmıyorsa salt okunur işaretçi veya görünüm türleri kullanın. `const` doğruluğunu baştan kurmak birkaç saniye; yıllar sonra bütün API ağında düzeltmek ise pahalı bir mimari operasyondur. Kısacası `const`, kısıtlama değil, gelecekteki kullanım biçimlerine açılan güvenli bir kapıdır.

![cta-const-borcu-47](/img/cta-const-borcu-47.svg)

