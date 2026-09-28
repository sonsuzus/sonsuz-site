---
layout: post
title: "Tersine Mühendislikte Ghidra: Derlenmiş C Kodunun İzini Sürmek"
math: true
categories: 
  - Bilgi
tags: 
  - ghidra
  - tersine mühendislik
  - c
  - decompiler
  - binary analiz
  - siber güvenlik
toc: true
image: /img/tersine-muhendislikte-ghidra-80.png
---

![tersine-muhendislikte-ghidra-80](/img/tersine-muhendislikte-ghidra-80.svg)


Elimizde kaynak kodu olmayan bir çalıştırılabilir dosya bulunduğunda programın ne yaptığını anlamak, dijital bir olay yerini incelemeye benzer. NSA tarafından açık kaynak hâle getirilen Ghidra; makine komutlarını, fonksiyonları ve veri yapılarını analiz ederek bu gizemi çözmemize yardım eder. Ancak küçük bir uyarı: Derlenmiş C kodunu birebir geri getiremeyiz. Decompiler’ın sunduğu çıktı, kaybolan kaynak kodun mantıksal bir yeniden inşasıdır. Analizleri yalnızca sahibi olduğunuz veya inceleme izni aldığınız dosyalarda yapmalısınız.
``
## Derleme sırasında neler kaybolur?

C kaynak kodu derlenirken değişken adları, yorumlar, dosya organizasyonu ve çoğu tür bilgisi makine kodunda korunmaz. Optimizasyon da işlemleri birleştirebilir, sıralarını değiştirebilir veya gereksiz fonksiyonları tamamen silebilir. Dolayısıyla tersine mühendislik matematiksel olarak tam terslenebilir bir dönüşüm değildir.

Derleme sürecini kabaca şöyle gösterebiliriz:

$$S \xrightarrow{C} B$$

Burada $S$ kaynak kodu, $C$ derleyiciyi, $B$ ise binary dosyayı temsil eder. Farklı kaynaklar aynı davranışı üretebildiğinden genellikle

$$C^{-1}(B) \neq S$$

olur. Ghidra’nın ürettiği sözde kodu $S'$ ile gösterirsek hedefimiz $S' = S$ değil, $S' \approx S$ olacak kadar doğru bir davranış modeli elde etmektir.

| Kaynak koddaki unsur | Binary içindeki durum | Ghidra’nın yaklaşımı |
|---|---|---|
| Değişken adları | Genellikle kayıp | `local_10` gibi geçici adlar üretir |
| Fonksiyon adları | Strip edilmiş olabilir | Çağrı grafiği ve imzalardan tahmin eder |
| Tür bilgisi | Kısmen kayıp | Kullanım biçimine göre çıkarım yapar |
| Kontrol akışı | Makine dallanmalarına dönüşür | `if`, `while` ve `switch` yapılarını kurar |
| Yorumlar | Tamamen kayıp | Analistin eklemesini bekler |

## Ghidra projesini hazırlamak

Ghidra’da yeni bir proje oluşturup **Import File** ile ELF, PE veya desteklenen başka bir binary içe aktarılır. Dosya formatı ve işlemci mimarisi çoğu zaman otomatik belirlenir. Ardından **Auto Analyze** çalıştırılır. Disassembly, fonksiyon tanıma, referans bulma ve decompilation seçenekleri başlangıç için açık bırakılabilir.

**CodeBrowser** penceresinde iki görünüm özellikle önemlidir:

- **Listing:** Gerçek assembly komutlarını ve adresleri gösterir.
- **Decompiler:** Bu komutlardan C benzeri, okunabilir sözde kod üretir.
- **Symbol Tree:** Fonksiyonları, importları ve global sembolleri listeler.
- **Defined Strings:** Mesaj, dosya yolu ve hata metni gibi güçlü ipuçlarını sunar.

Örneğin özgün programda şu fonksiyon bulunmuş olsun:

```c
int indirimli_fiyat(int fiyat, int oran) {
    return fiyat - (fiyat * oran / 100);
}
```

Sembolleri kaldırılmış binary analiz edildiğinde Ghidra buna benzer bir çıktı verebilir:

```c
int FUN_00401120(int param_1, int param_2)
{
    return param_1 - (param_1 * param_2) / 100;
}
```

İşlem aynı kalırken anlamlı isimler kaybolmuştur. Analistin görevi fonksiyon çağrılarını ve parametre kullanımını inceleyerek `FUN_00401120` adını `indirimli_fiyat`, parametreleri de `fiyat` ve `oran` şeklinde yeniden adlandırmaktır. Bu düzenlemeler binary’yi değiştirmez; analiz veritabanını daha anlaşılır yapar.

## Veri yapılarını yeniden kurmak

Bir parametre sürekli `param_1 + 8` ve `param_1 + 16` adreslerinden okunuyorsa elimizde bir yapı işaretçisi olabilir. Alan adresi genel olarak

$$A_{alan} = A_{taban} + offset$$

şeklindedir. Offsetlerin boyutu, kullanılan komutlar ve erişim sırası incelenerek Ghidra’nın **Data Type Manager** aracıyla bir `struct` tanımlanabilir. Tür fonksiyona uygulandığında anlamsız pointer aritmetiği, okunabilir alan erişimlerine dönüşür.

## Analizi doğrulamak

Decompiler çıktısına körü körüne güvenilmemelidir. Şüpheli satırları Listing görünümündeki assembly ile karşılaştırın; fonksiyon çağrılarını, çapraz referansları ve string kullanımlarını takip edin. Gerekirse programı izole bir laboratuvar ortamında debugger ile çalıştırarak varsayımlarınızı sınayın.

Ghidra sihirli bir “kaynak kodu geri getir” düğmesi değildir. Daha çok assembly bilgisi, örüntü tanıma ve sabırlı isimlendirmeyi bir araya getiren güçlü bir çalışma masasıdır. İyi bir analiz sonunda özgün biçimi değil, programın kararlarını ve veri modelini açıklayan güvenilir bir harita elde ederiz.
