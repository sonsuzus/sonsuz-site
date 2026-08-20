---
layout: post
title: "Rust ile Bellek Güvenliği: Borrow Checker Sahne Arkasında Nasıl Çalışır?"
math: true
categories: 
  - Bilgi
tags: 
  - Rust
  - Bellek Güvenliği
  - Borrow Checker
image: /img/rust-ile-bellek-21.png
---

Rust'ın en iddialı vaadi, çöp toplayıcıya ihtiyaç duymadan bellek güvenliği sunmasıdır. Bu vaat; `null` işaretçileri, use-after-free, veri yarışları ve çift bellek serbest bırakma gibi klasik hataların büyük bölümünü program daha çalışmadan yakalamasına dayanır. Bu işin başrolünde, Rust derleyicisinin sahiplik kurallarını denetleyen titiz bir kapı görevlisi olan **borrow checker** vardır.
``
## Sahiplik: Her değerin bir sorumlusu var

Rust'ta heap üzerinde tutulan her değerin aynı anda yalnızca bir sahibi bulunur. Sahip değişkene ait yaşam alanı bittiğinde Rust, değeri otomatik olarak temizlemek için `drop` çağrısını ekler. Bu yaklaşımın temel fikri basittir: Bir kaynağı kimin temizleyeceği her zaman belliyse, iki kişinin aynı kaynağı temizlemeye çalışması engellenir.

```rust
fn main() {
    let mesaj = String::from("Merhaba");
    let yeni_sahip = mesaj;

    // println!("{mesaj}"); // Derleme hatası: değer taşındı
    println!("{yeni_sahip}");
}
```

Burada `String`, kopyalanmak yerine `yeni_sahip` değişkenine **taşınır** (*move*). Eski isim artık geçerli değildir. Derleyici bu kuralı uygular; dolayısıyla `mesaj` serbest bırakıldıktan sonra ona erişmeye yönelik bir çalışma zamanı sürprizi oluşmaz.

## Ödünç alma kuralları

Her değeri taşımak pratik değildir. Rust bu nedenle referanslarla ödünç alma (*borrowing*) sunar. Borrow checker, bir değer için şu iki durumdan yalnızca birine izin verir:

| Ödünç türü | Aynı anda izin verilen sayı | Yazma yapabilir mi? | Temel amaç |
|---|---:|---:|---|
| Değişmez referans `&T` | Bir veya daha fazla | Hayır | Güvenli, eşzamanlı okuma |
| Değiştirilebilir referans `&mut T` | Tam olarak bir | Evet | Tekil ve kontrollü güncelleme |

Bu kuralı kısa bir formülle düşünebiliriz. Bir kaynağın değişmez referans sayısı $R$, değiştirilebilir referans sayısı $W$ ise geçerli durum şudur:

$$W \leq 1 \quad \text{ve} \quad (W = 1 \Rightarrow R = 0)$$

Yani ya çok sayıda okuyucu vardır ya da yalnız bir yazıcı. Bu, özellikle çok iş parçacıklı kodlarda veri yarışlarını daha derleme aşamasında ortadan kaldıran kritik ilkedir.

```rust
fn main() {
    let mut sayilar = vec![1, 2, 3];
    let ilk = &sayilar[0];

    // sayilar.push(4); // Hata: `ilk` hâlâ kullanılıyor olabilir
    println!("İlk eleman: {ilk}");
}
```

`push`, vektörün belleğini yeniden tahsis edebilir; bu da `ilk` referansını geçersiz kılabilir. Rust "belki sorun olur" demekle yetinmez: Kodun bu biçimini derlemez. Böylece C veya C++ dünyasında sıkça görülen sarkan işaretçi (*dangling pointer*) problemi doğmadan biter.

## Yaşam süreleri: Referans ne kadar yaşayabilir?

Borrow checker referansın yalnızca türünü değil, ne kadar süreyle geçerli kaldığını da analiz eder. Yaşam süreleri (*lifetimes*), çoğu zaman derleyicinin otomatik çıkardığı ilişkilerdir. Gerekli olduğunda geliştirici bu ilişkiyi açıkça ifade eder:

```rust
fn uzun_olan<'a>(sol: &'a str, sag: &'a str) -> &'a str {
    if sol.len() >= sag.len() { sol } else { sag }
}
```

`'a`, dönüş değerinin `sol` ve `sag` referanslarından daha uzun yaşayamayacağını belirtir. Bu bir süre ölçümü değil, referanslar arasındaki geçerlilik sözleşmesidir. Fonksiyon, yerel bir `String` oluşturup ona ait referansı dışarı döndüremez; çünkü yerel değer fonksiyon bitince yok olur.

## Çalışma zamanı maliyeti neden oluşmaz?

Garbage collector kullanan diller, erişilemeyen nesneleri çalışma zamanında izleyip temizler. Rust ise sahiplik ve ödünç alma denetimini ağırlıkla derleme zamanında gerçekleştirir. Başarılı biçimde derlenen güvenli Rust kodunda referans denetimi için sürekli bir çalışma zamanı taraması gerekmez. Bu anlayış genellikle **zero-cost abstraction** ilkesiyle özetlenir: Güvenlik, gereksiz sürekli maliyet eklemeden sağlanır.

Elbette Rust sihirli değildir. `unsafe` blokları, ham işaretçiler ve FFI çağrıları bazı derleyici garantilerini geliştiricinin sorumluluğuna bırakabilir. Ayrıca `RefCell<T>` gibi türler, esnekliğe karşılık ödünç alma kurallarını çalışma zamanında denetler ve kural ihlalinde panic üretebilir. Ancak günlük, güvenli Rust kodunda borrow checker; bellek hatalarını kullanıcıya ulaşmadan, daha editörde kırmızı çizgiye dönüştürür.

![rust-ile-bellek-21](/img/rust-ile-bellek-21.svg)

