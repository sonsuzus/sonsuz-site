---
layout: post
title: "Kodun Aynaya Bakışı: Macros ve Metaprogramming"
math: true
categories: 
  - Bilgi
tags: 
  - macros
  - metaprogramming
  - derleyici
  - ast
  - rust
  - kod üretimi
toc: true
image: /img/kodun-aynaya-bakisi-12.png
---

![kodun-aynaya-bakisi-12](/img/kodun-aynaya-bakisi-12.svg)


Bir programın başka bir program üretmesi ilk bakışta bilim kurgu gibi gelebilir. Oysa derleyicilerden web çatılarındaki otomatik yönlendirmelere kadar pek çok araç bu fikri kullanır. **Metaprogramming**, kodu veri gibi okuyup değiştirme veya yeni kod üretme tekniğidir; macro ise bu geniş ailenin en tanınmış üyelerinden biridir.

``

## Kod hakkında kod yazmak

Normal bir program veriyi işler: sayıları toplar, dosyaları okur veya kullanıcı isteklerine yanıt verir. Meta program ise girdilerinden en az biri olarak program yapısını ele alır. Basitleştirilmiş biçimde bunu şu fonksiyonla gösterebiliriz:

$$M(P, C) \rightarrow P'$$

Burada $P$ mevcut programı, $C$ yapılandırmayı, $M$ meta programı ve $P'$ üretilmiş yeni programı temsil eder. Sonuç doğrudan kaynak kod, bir **Abstract Syntax Tree (AST)** ya da çalıştırılabilir bir fonksiyon olabilir.

Örneğin yüz farklı veri modeli için aynı doğrulama kodunu elle yazmak yerine alan tanımlarını okuyan bir araç, gereken kontrolleri otomatik üretebilir. Böylece geliştirici tekrarları değil, kuralları tanımlar.

## Macro ile metaprogramming aynı şey mi?

Her macro bir metaprogramming aracıdır; fakat her metaprogramming tekniği macro değildir. Reflection, decorator, annotation processor, şablon sistemi ve kaynak kod üreteci de bu kapsama girer.

| Teknik | Çalışma zamanı | Temel avantaj | Başlıca risk |
|---|---|---|---|
| Metinsel macro | Derleme öncesi | Basit ve hızlı üretim | İsim çakışması |
| AST macro | Derleme sırasında | Sözdizimini güvenli işler | Karmaşık hata mesajları |
| Reflection | Çalışma sırasında | Dinamik davranış | Performans maliyeti |
| Kod üretici | Derleme öncesi | Büyük miktarda kod üretir | Üretilen kodun yönetimi |

C dilindeki `#define`, çoğunlukla metinsel değiştirme yapar. Rust gibi modern dillerdeki macro sistemleri ise token veya sözdizimi ağacı seviyesinde çalışarak daha güvenli dönüşümler sunar.

## Rust ile küçük bir macro

Aşağıdaki bildirime dayalı macro, verilen ifadeyi çalıştırır ve ne kadar sürdüğünü ölçer:

{% raw %}
```rust
macro_rules! zamanla {
    ($ifade:expr) => {{
        let baslangic = std::time::Instant::now();
        let sonuc = $ifade;
        println!("Süre: {:?}", baslangic.elapsed());
        sonuc
    }};
}

fn main() {
    let toplam = zamanla!((1..=1000).sum::<i32>());
    println!("Toplam: {}", toplam);
}
```
{% endraw %}

Buradaki `$ifade:expr`, macroya geçerli bir Rust ifadesi kabul edildiğini belirtir. Macro genişletildiğinde ölçüm kodu çağrının bulunduğu yere yerleştirilir. Çift süslü parantez ayrı bir kapsam oluşturarak geçici değişkenlerin dışarıdaki isimlerle çarpışmasını önler. Bu özellik **hygiene**, yani macro hijyeni fikriyle ilişkilidir.

## AST neden önemlidir?

Kaynak kod yalnızca karakterlerden oluşan bir metin değildir. Derleyici açısından `2 + 3 * 4`, operatör önceliğini taşıyan bir ağaçtır:

```text
    +
   / \
  2   *
     / \
    3   4
```

Bu temsil sayesinde dönüşüm aracı yalnızca kelime değiştirmek yerine programın anlamlı parçalarını hedefleyebilir. Örneğin bütün fonksiyon çağrılarına kayıt mekanizması ekleyebilir veya belirli bir annotation taşıyan sınıflar için serileştirme kodu oluşturabilir.

## Güç büyükse hata da yaratıcıdır

Metaprogramming tekrarları azaltır, alan odaklı mini diller kurulmasını sağlar ve derleme zamanında kontroller gerçekleştirebilir. Ancak aşırı kullanıldığında kodun görünen hâli ile çalışan hâli birbirinden uzaklaşır. Geliştirici bir satır yazar, derleyici perde arkasında elli satır üretir; hata mesajı da doğal olarak küçük bir polisiye romana dönüşebilir.

İyi bir meta program deterministik olmalı, ürettiği kod incelenebilmeli ve açık belgeler sunmalıdır. Şu sezgisel denge faydalıdır:

$$Kazanç = Tekrarın\ Azalması - Gizli\ Karmaşıklık$$

Üretim mekanizması, ortadan kaldırdığı tekrardan daha zor anlaşılır hâle geliyorsa yanlış soyutlama seçilmiş olabilir. Kısacası macros ve metaprogramming sihir değildir; derleyici aşamalarını bilinçli kullanan güçlü araçlardır. Doğru kullanıldıklarında programcıya daha fazla kod yazdırmaz, programa kendi kodunun bir bölümünü yazdırırlar.
