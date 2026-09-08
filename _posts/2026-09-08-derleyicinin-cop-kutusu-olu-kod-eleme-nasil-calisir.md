---
layout: post
title: "Derleyicinin Çöp Kutusu: Ölü Kod Eleme Nasıl Çalışır?"
math: true
categories: 
  - Bilgi
tags: 
  - derleyici
  - optimizasyon
  - ölü kod eleme
toc: true
---

Kodunuzda kimsenin ziyaret etmediği bir `if` dalı veya hesaplanıp unutulan bir değişken bulunabilir. Bunlar kaynak dosyada gayet canlı görünse de programın gözlemlenebilir sonucuna katkı sağlamaz. Derleyicilerin **ölü kod eleme** (Dead Code Elimination, DCE) optimizasyonu, bu gereksiz parçaları belirleyip makine kodundan çıkarır. Sonuç genellikle daha küçük, daha hızlı ve işlemci önbelleğiyle daha iyi anlaşan bir programdır.
``

## Ölü kod tam olarak nedir?

Ölü kod denildiğinde iki temel durumdan söz edilir:

1. **Ulaşılamayan kod:** Kontrol akışının hiçbir koşulda erişemediği komutlardır.
2. **Sonucu kullanılmayan kod:** Çalıştırılabilir olsa bile ürettiği değer programın daha sonraki davranışını etkilemez.

| Kod türü | Tipik örnek | Neden silinebilir? |
|---|---|---|
| Ulaşılamayan kod | `return` sonrasındaki komut | Kontrol akışı oraya gelemez |
| Ölü atama | Üzerine hemen yeni değer yazılan değişken | İlk değer hiç okunmaz |
| Kullanılmayan hesaplama | Sonucu saklanmayan aritmetik işlem | Gözlemlenebilir çıktı üretmez |
| Sabit koşullu dal | `if (false)` bloğu | Koşul hiçbir zaman doğru değildir |

Örneğin aşağıdaki C kodunda bazı satırlar gereksizdir:

```c
int hesapla(int x) {
    int sonuc = x * 10; // Bu değer aşağıda eziliyor.
    sonuc = x + 2;
    return sonuc;

    x++;                // return sonrasında: ulaşılamaz.
}
```

Derleyici ilk atamayı ve `return` sonrasındaki artırmayı kaldırabilir. İşlevin anlamı değişmez; geriye esasen `return x + 2;` kalır.

## Kontrol akış grafiğiyle düşünmek

Derleyici, fonksiyonu çoğunlukla **temel bloklara** ayırır. Kesintisiz çalışan komut dizileri düğüm, olası geçişler ise kenar olarak gösterilir. Böylece bir **kontrol akış grafiği** (Control Flow Graph, CFG) elde edilir.

Giriş düğümünden erişilemeyen bir düğüm varsa o blok güvenle silinebilir. Matematiksel olarak giriş düğümü $s$, bütün düğümler kümesi $V$ ve erişilebilenler $R(s)$ olsun. Ulaşılamayan bloklar şu kümededir:

$$D_{unreachable} = V \setminus R(s)$$

Ancak erişilebilir olmak, faydalı olmak demek değildir. Bu noktada **canlılık analizi** devreye girer. Bir değişkenin mevcut değeri gelecekte okunacaksa değişken o noktada canlıdır. Temel bir geriye doğru veri akışı denklemi şöyledir:

$$LiveIn(B) = Use(B) \cup (LiveOut(B) \setminus Def(B))$$

Burada `Use`, blokta okunan; `Def`, değer atanan değişkenleri temsil eder. `LiveOut` ise sonraki blokların ihtiyaç duyduğu değerlerden oluşur. Derleyici bu kümeleri sonuç değişmeyene, yani sabit noktaya ulaşana kadar tekrar tekrar hesaplar.

## Yan etkiler neden işleri karıştırır?

Bir ifadenin sonucu kullanılmasa bile ifade silinemeyebilir. Çünkü fonksiyon çağrıları, dosya yazma, ekrana çıktı verme, atomik işlemler ve `volatile` erişimleri **yan etki** oluşturabilir.

```c
int deger = pahali_hesaplama(); // Saf fonksiyonsa kaldırılabilir.
printf("İşlem başladı\n");       // Sonucu kullanılmasa da silinemez.
```

| İşlem | Sonuç kullanılmıyorsa silinebilir mi? |
|---|---|
| `a + b` | Genellikle evet |
| Saf fonksiyon çağrısı | Genellikle evet |
| `printf` çağrısı | Hayır |
| Belleğe görünür yazma | Genellikle hayır |
| `volatile` okuma/yazma | Hayır |

Bu nedenle DCE yalnızca “değişken kullanılmıyor” diye karar vermez; işlemin programın dışarıdan gözlemlenebilir davranışını değiştirip değiştirmediğini de inceler.

## SSA biçimi ve işaretle-süpür yaklaşımı

Modern derleyiciler ara temsili sıklıkla **Static Single Assignment** (SSA) biçimine dönüştürür. SSA’da her değişken yalnızca bir kez atanır. Bu özellik, hangi değerin nerede kullanıldığını açık hâle getirir.

Derleyici önce `return`, bellek yazma ve yan etkili çağrı gibi zorunlu komutları canlı olarak işaretler. Ardından bu komutların bağımlı olduğu değerleri geriye doğru takip eder. İşaretlenmeyen komutlar süpürülür. Tıpkı çöp toplayıcının erişilemeyen nesneleri temizlemesi gibi!

DCE çoğu zaman sabit yayılımı, fonksiyon içe alma ve dal sadeleştirme gibi optimizasyonlardan sonra yeniden çalıştırılır. Çünkü her dönüşüm yeni ölü kodlar doğurabilir. Derleyici böylece programın niyetini korurken gereksiz hesapları sessizce çöpe gönderir; yazdığımız kod ile işlemcinin gerçekten çalıştırdığı kod arasındaki şaşırtıcı fark da burada ortaya çıkar.
