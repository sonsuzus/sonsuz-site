---
layout: post
title: "Rust'ta unsafe: Derleyiciyi Susturmak Değil, Sorumluluğu Devralmak"
math: true
categories: 
  - Bilgi
tags: 
  - rust
  - unsafe
  - bellek güvenliği
  - ffi
  - sistem programlama
  - ham işaretçiler
toc: true
image: /img/rustta-unsafe-derleyiciyi-34.png
---

Rust denince akla ilk olarak bellek güvenliği gelir. Ancak dilin ortasında, üzerinde kocaman bir uyarı etiketi varmış gibi duran `unsafe` anahtar sözcüğü bulunur. Bu ilk bakışta çelişkili görünebilir: Bellek hatalarını önleyen bir dil neden güvenlik kontrollerini aşmaya izin versin? Çünkü bazı doğru programların güvenli olduğunu derleyici kanıtlayamaz. `unsafe`, güvenliği çöpe atmak değil; belirli kuralları doğrulama sorumluluğunu programcıya devretmektir.
``
## `unsafe` gerçekte ne söyler?

Bir `unsafe` bloğu, “Bu kod tehlikelidir” demekten çok “Derleyici, burada ihtiyaç duyulan güvenlik kanıtını oluşturamıyor; gerekli değişmezleri ben koruyorum” anlamına gelir. Rust'ın sahiplik ve ödünç alma sistemi muhafazakârdır. Bir işlemin güvenli olduğundan emin değilse onu reddeder.

Bunu basitçe şöyle düşünebiliriz:

$$
\text{Program güvenliği} = \text{Derleyici garantileri} + \text{Programcı tarafından korunan değişmezler}
$$

Güvenli Rust'ta ikinci terim büyük ölçüde standart kütüphanenin içine saklanmıştır. `unsafe` kullandığımızda ise bu değişmezlerin bir kısmını doğrudan biz yönetiriz.

| Özellik | Güvenli Rust | `unsafe` Rust |
|---|---|---|
| Borrow checker çalışır mı? | Evet | Evet |
| Tür denetimi yapılır mı? | Evet | Evet |
| Her işlem serbest mi? | Hayır | Hayır |
| Ek güvenlik kanıtını kim sağlar? | Derleyici | Programcı |
| Tanımsız davranış riski | Çok düşük | Kurallar bozulursa yüksek |

Önemli ayrıntı şudur: `unsafe`, borrow checker'ı veya tür sistemini tamamen kapatmaz. Yalnızca Rust'ın normalde yasakladığı beş özel işlem sınıfına izin verir. Bunlar ham işaretçileri dereference etmek, `unsafe` fonksiyon çağırmak, değiştirilebilir statik verilere erişmek, `unsafe` trait uygulamak ve union alanlarını okumaktır.

## Ham işaretçiler neden gerekli olabilir?

Donanım kayıtları, işletim sistemi API'leri ve C kütüphaneleri Rust'ın referans kurallarından haberdar değildir. Örneğin belirli bir bellek adresindeki donanım kaydını okumamız gerekebilir:

```rust
fn read_register(address: usize) -> u32 {
    let register = address as *const u32;

    unsafe {
        // Adresin geçerli ve u32 için hizalı olduğunu biz garanti ediyoruz.
        core::ptr::read_volatile(register)
    }
}
```

Burada `read_volatile`, derleyicinin okumayı optimize ederek kaldırmasını engeller. Fakat adres geçersizse, yanlış hizalanmışsa veya okunması yasak bir bölgeyi gösteriyorsa sonuç tanımsız davranış olabilir. `unsafe` bloğu adresi sihirli biçimde güvenli yapmaz; yalnızca işlemi gerçekleştirmemize izin verir.

## C ile konuşurken sınır kapısı

C fonksiyonları Rust'ın sahiplik sözleşmesini taşımaz. Bu nedenle Foreign Function Interface, yani FFI çağrıları güvenlik sınırı kabul edilir:

```rust
unsafe extern "C" {
    fn strlen(text: *const std::ffi::c_char) -> usize;
}

fn text_length(text: &std::ffi::CStr) -> usize {
    unsafe {
        // CStr, işaretçinin null sonlandırmalı ve geçerli kalmasını sağlar.
        strlen(text.as_ptr())
    }
}
```

Burada iyi tasarımın püf noktası, tehlikeli çağrıyı küçük bir alana hapsetmek ve dışarıya güvenli bir arayüz sunmaktır. `text_length` çağırıcısı ham işaretçiyle uğraşmaz; gerekli koşullar `CStr` türü aracılığıyla ifade edilir.

## Ne zaman kullanmalıyız?

`unsafe`, performans kazanmak için başvurulan ilk araç olmamalıdır. Önce güvenli soyutlamalar, standart kütüphane ve güvenilir crate'ler araştırılmalıdır. Gerçekten gerektiğinde ise her blok küçük tutulmalı ve varsayımlar yorumlarla belgelenmelidir.

Bir `unsafe` işlemden önce şu soruları sorun:

1. İşaretçi geçerli, hizalı ve doğru türü gösteriyor mu?
2. Verinin yaşam süresi işlem boyunca devam ediyor mu?
3. Aynı belleğe çakışan değiştirilebilir erişimler oluşuyor mu?
4. C tarafı işaretçiyi saklıyor veya belleği serbest bırakıyor mu?
5. Bu kod güvenli bir fonksiyonun arkasına kapatılabilir mi?

Sonuç olarak `unsafe`, Rust'ın başarısızlığı değil, sistem programlamanın gerçekleriyle yaptığı dürüst anlaşmadır. Donanım ve yabancı kütüphaneler kusursuz Rust kurallarına göre davranmaz. İyi yazılmış `unsafe` kod, derleyiciyi susturup kaçmak yerine, kanıtlanamayan koşulları açıkça tanımlar ve tehlikeyi küçük, denetlenebilir bir bölgede tutar.

![rustta-unsafe-derleyiciyi-34](/img/rustta-unsafe-derleyiciyi-34.svg)

