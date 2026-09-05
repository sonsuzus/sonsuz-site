---
layout: post
title: "Tersine Mühendislikte Statik ve Dinamik Analiz: Koddan Belleğe Yolculuk"
math: true
categories: 
  - Bilgi
tags: 
  - tersine mühendislik
  - statik analiz
  - dinamik analiz
toc: true
---

Elinizde kaynak kodu olmayan derlenmiş bir program bulunduğunu düşünün. Program çalışıyor, dosyalar okuyor ve hesaplamalar yapıyor; fakat içeride neler döndüğünü bilmiyorsunuz. Tersine mühendislik, bu kapalı kutunun davranışını assembly kodu, decompiler çıktısı ve çalışma zamanı gözlemleri üzerinden anlamaya çalışır. Elbette bu teknikler yalnızca size ait veya inceleme izniniz bulunan yazılımlarda kullanılmalıdır.
``

## İki Farklı Bakış Açısı

Bir programı incelemenin iki temel yolu vardır: Çalıştırmadan yapısına bakmak ve çalışırken davranışını izlemek. Bunlar sırasıyla **statik analiz** ve **dinamik analiz** olarak adlandırılır.

| Özellik | Statik analiz | Dinamik analiz |
|---|---|---|
| Program çalıştırılır mı? | Hayır | Evet |
| Temel araç | Disassembler, decompiler | Debugger, bellek izleyici |
| Güçlü yanı | Genel yapıyı gösterir | Gerçek değerleri ortaya çıkarır |
| Zayıf yanı | Decompiler çıktısı yanıltabilir | Yalnızca izlenen yürütme yolunu gösterir |
| Tipik araçlar | Ghidra, IDA, Binary Ninja | GDB, LLDB, WinDbg, x64dbg |

Bu yaklaşımlar rakip değil, takım arkadaşıdır. Statik analiz haritayı verir; dinamik analiz ise elinize pusulayı alıp arazide yürümenizi sağlar.

## Decompiler Aslında Ne Yapar?

Derleyici, kaynak koddaki değişkenleri ve ifadeleri işlemcinin anlayacağı makine komutlarına dönüştürür. Decompiler ise bu dönüşümü yaklaşık olarak tersine çevirmeye çalışır:

$$\text{Kaynak Kod} \xrightarrow{\text{derleyici}} \text{Makine Kodu} \xrightarrow{\text{decompiler}} \text{Sözde Kaynak Kod}$$

Son adım kusursuz değildir. Değişken isimleri, yorumlar ve bazı veri tipi bilgileri derleme sırasında kaybolabilir. Bu nedenle decompiler size özgün kaynak kodu değil, davranış bakımından ona benzeyen bir temsil sunar.

Örneğin kaynakta aşağıdaki fonksiyon bulunsun:

```c
int puan_hesapla(int seviye, int bonus) {
    return seviye * 10 + bonus;
}
```

Decompiler bunu şu biçimde gösterebilir:

```c
int FUN_00401120(int param_1, int param_2) {
    return param_1 * 10 + param_2;
}
```

İsimler kaybolmuştur ama matematiksel ilişki korunmuştur:

$$P = 10S + B$$

Analistin görevi, çağrıldığı yerleri ve kullanılan değerleri inceleyerek `param_1` değişkeninin seviye olduğunu çıkarmaktır. Fonksiyonları yeniden adlandırmak ve yorum eklemek, karmaşık bir ikili dosyayı giderek okunabilir bir belgeye dönüştürür.

## Bellekte Adım Adım İzleme

Dinamik analizde program kontrollü bir ortamda debugger ile başlatılır. İncelenecek komuta bir **breakpoint** yerleştirilir. İşlemci bu noktaya geldiğinde yürütme durur; register değerleri, çağrı yığını ve bellek bölgeleri incelenebilir.

Linux üzerinde eğitim amacıyla derlenmiş bir örnek program GDB ile şöyle gözlemlenebilir:

```bash
gcc -g -O0 ornek.c -o ornek
gdb ./ornek
```

GDB oturumunda temel akış şöyledir:

```text
break puan_hesapla
run
info registers
step
print seviye
x/16xb &seviye
continue
```

`break` yürütmeyi ilgili fonksiyonda durdurur. `step` bir sonraki kaynak satırına ilerler, `info registers` işlemci register’larını gösterir ve `x/16xb` belirtilen adresten başlayan 16 baytı onaltılık biçimde görüntüler. `continue` ise programı bir sonraki durma noktasına kadar sürdürür.

Bellekteki bir adresi raf numarası gibi düşünebilirsiniz. Pointer bu rafın konumunu, adresteki baytlar ise rafın içeriğini belirtir. Ancak modern sistemlerde ASLR nedeniyle adresler çalıştırmalar arasında değişebilir. Bu yüzden yalnızca sabit adreslere değil; modül tabanına, sembollere ve çağrı akışına odaklanmak daha güvenilirdir.

## Sağlam Bir İnceleme Akışı

Önce dosya türü, mimari, metinler ve içe aktarılan fonksiyonlar belirlenir. Ardından decompiler ile dikkat çeken fonksiyonlar incelenir ve anlamlı isimlerle etiketlenir. Son olarak program izole bir laboratuvar ortamında debugger ile çalıştırılarak varsayımlar doğrulanır.

En önemli kural şudur: Decompiler çıktısına körü körüne inanmayın, debugger’da gördüğünüz tek bir yürütme yolunu da bütün program sanmayın. Statik harita ile dinamik kanıt birleştiğinde kapalı kutu yavaş yavaş şeffaflaşır.
