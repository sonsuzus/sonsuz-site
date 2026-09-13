---
layout: post
title: "Crystal ile Statik Tipli Ruby Deneyimi: Hız, Güvenlik ve Zarif Sözdizimi"
math: true
categories: 
  - Bilgi
tags: 
  - crystal
  - ruby
  - statik tipleme
  - tip çıkarımı
  - performans
  - programlama
toc: true
---

Ruby’nin okunabilir sözdizimini seviyor, ancak derleme zamanında tip güvenliği ve yerel kod performansı da istiyorsanız Crystal oldukça ilgi çekici bir seçenek. Crystal, Ruby’den güçlü biçimde esinlenen sözdizimini statik tip sistemi, tip çıkarımı ve LLVM tabanlı derleyiciyle birleştirir. Sonuç, geliştiriciye dinamik bir dil kullanıyormuş hissi veren fakat birçok hatayı program çalışmadan önce yakalayan modern bir programlama dilidir.
``
## Crystal neden Ruby gibi hissettiriyor?

Crystal kodu ilk bakışta Ruby koduyla kolayca karıştırılabilir. Parantezlerin çoğu durumda isteğe bağlı olması, blok yapısı, sınıflar ve koleksiyon işlemleri oldukça tanıdıktır:

```crystal
numbers = [1, 2, 3, 4, 5]

squares = numbers
  .select { |number| number.odd? }
  .map { |number| number ** 2 }

puts squares
```

Bu kod tek sayıları seçer, karelerini hesaplar ve sonucu yazdırır. `numbers` değişkeninin tipi açıkça belirtilmemesine rağmen derleyici onu `Array(Int32)` olarak çıkarır. Yani Crystal statik tiplidir, fakat her değişkenin yanına tip yazmanızı zorunlu kılmaz.

## Statik tipleme ve tip çıkarımı

Statik tip sisteminde ifadelerin tipi derleme sırasında bilinir. Basitleştirilmiş biçimde bir fonksiyonun tip dönüşümünü şöyle gösterebiliriz:

$$f: A \rightarrow B$$

Burada fonksiyon, `A` tipindeki bir değeri alıp `B` tipinde bir değer üretir. Crystal, mümkün olduğunda `A` ve `B` tiplerini kodun kullanımından çıkarır:

```crystal
def double(value)
  value * 2
end

puts double(21) # Int32 döndürür
puts double(2.5) # Float64 döndürür
```

Derleyici, metodun çağrıldığı tiplere göre uygun sürümler üretir. Bu yaklaşım rahat bir sözdizimi sunarken sayıyla metni yanlışlıkla toplamak gibi hataları erken yakalar.

| Özellik | Ruby | Crystal |
|---|---|---|
| Tip kontrolü | Çalışma zamanında | Derleme zamanında |
| Tip bildirimi | Gerekmez | Genellikle çıkarılır |
| Çalıştırma | Yorumlayıcı/VM | Yerel makine kodu |
| `nil` güvenliği | Hata çalışma anında görülebilir | Olasılık tipte belirtilir |
| Metaprogramlama | Dinamik | Makro ve derleme zamanı odaklı |

## `nil` sürprizlerine karşı güvenlik

Ruby’de bir değerin `nil` olduğunu unutarak metot çağırmak klasik bir çalışma zamanı hatasıdır. Crystal’da değer boş olabiliyorsa bu bilgi tipe eklenir. `String?`, aslında `String | Nil` birleşim tipinin kısa yazımıdır.

```crystal
def find_username(id : Int32) : String?
  id == 1 ? "ada" : nil
end

username = find_username(2)
puts username.try(&.upcase) || "Kullanıcı bulunamadı"
```

`try`, değer `nil` değilse `upcase` metodunu çağırır. Böylece olası boşluk durumu kodda görünür olur ve geliştiricinin onu bilinçli şekilde ele alması sağlanır.

## Performans nereden geliyor?

Crystal kaynak kodu LLVM aracılığıyla yerel makine koduna derlenir. Çok kaba bir performans modeli şu şekilde düşünülebilir:

$$T_{toplam} = T_{derleme} + n \times T_{çalıştırma}$$

Bir komut yalnızca bir kez çalışacaksa derleme maliyeti hissedilebilir. Fakat sunucu veya hesaplama uygulamasında `n` büyüdükçe hızlı yerel kod avantaj sağlar. Üretim derlemelerinde optimizasyon açılabilir:

```bash
crystal build app.cr --release
./app
```

`--release`, daha uzun derleme süresi karşılığında optimize edilmiş bir çalıştırılabilir dosya üretir. Geliştirme sırasında ise `crystal run app.cr` komutu hızlı denemeler için yeterlidir.

## Crystal her Ruby projesinin yerine geçer mi?

Hayır. Benzer sözdizimine rağmen Crystal, Ruby uyumlu değildir; Ruby gem’leri doğrudan kullanılamaz. Crystal paketleri **shard** olarak adlandırılır ve bağımlılıklar `shard.yml` dosyasında yönetilir. Ayrıca dinamik olarak sürekli şekil değiştiren nesneler statik tip sistemi nedeniyle yeniden tasarım gerektirebilir.

Crystal; komut satırı araçları, web servisleri ve performans odaklı uygulamalar için güçlü bir adaydır. Ruby’nin ifade gücünü sevip “bu hata keşke daha çalıştırmadan yakalansaydı” diyorsanız, Crystal size tanıdık ama daha sıkı kuralları olan eğlenceli bir oyun alanı sunar.
