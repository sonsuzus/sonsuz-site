---
layout: post
title: "Zamanda Yolculuğun Kod Hali: Emülasyon ve Retro Konsollar"
math: true
categories: 
  - Bilgi
tags: 
  - emülasyon
  - retro oyun
  - konsol
  - donanım
  - simülasyon
  - yazılım
toc: true
image: /img/zamanda-yolculugun-kod-43.png
---

![zamanda-yolculugun-kod-43](/img/zamanda-yolculugun-kod-43.svg)


Bir zamanlar televizyona bağladığımız, kartuşuna üfleyince gizemli biçimde çalışan retro konsollar bugün bilgisayarlarda ve telefonlarda yeniden hayat buluyor. Bunun arkasındaki teknolojiye **emülasyon** denir. Emülatörler yalnızca eski oyunları çalıştıran programlar değildir; işlemciden ses çipine kadar başka bir sistemin davranışlarını yazılımla yeniden oluşturan küçük birer dijital zaman makinesidir.

``

## Emülasyon tam olarak nedir?

Emülasyon, bir kaynak sistemin davranışını farklı bir hedef sistem üzerinde taklit etme işlemidir. Örneğin modern bir x86-64 bilgisayar, 1980'lerde kullanılan 8 bitlik bir işlemcinin komutlarını doğrudan anlamaz. Emülatör, eski oyunun makine kodunu okur, her komutun ne yaptığını belirler ve aynı sonucu modern donanım üzerinde üretir.

Buradaki amaç yalnızca benzer bir görüntü oluşturmak değil, oyunun beklediği donanım ortamını mümkün olduğunca doğru sağlamaktır. İşlemci kayıtları, bellek haritası, grafik katmanları, giriş aygıtları, kesmeler ve saat döngüleri bu ortamın parçalarıdır.

| Yaklaşım | Taklit edilen şey | Avantajı | Dezavantajı |
|---|---|---|---|
| Emülasyon | Donanım davranışı | Yüksek uyumluluk | Daha fazla işlem gücü ister |
| Simülasyon | Sistemin genel modeli | Analiz için kullanışlıdır | Birebir davranmayabilir |
| Sanallaştırma | Aynı mimaride işletim sistemi | Çok hızlıdır | Farklı işlemciyi doğrudan taklit etmez |
| Yeniden yapım | Oyunun kendisi | Modern özellikler sunar | Orijinal sistem korunmaz |

## İşlemci nasıl taklit edilir?

Basit bir işlemci emülatörü genellikle **fetch-decode-execute** döngüsünü uygular: Komut bellekten alınır, anlamı çözülür ve ilgili işlem gerçekleştirilir. Program sayacı daha sonra sıradaki komuta ilerler.

Bir işlemcinin yaklaşık çalışma süresi şöyle düşünülebilir:

$$t = N / f$$

Burada $N$ yürütülen saat döngüsü, $f$ ise işlemcinin frekansıdır. Emülatör çok hızlı çalışırsa oyun hızlanır; yavaş çalışırsa görüntü ve ses takılır. Bu nedenle döngülerin zamanlaması önemlidir.

```python
memory = [0x01, 5, 0x02, 3, 0xFF]
pc = 0
accumulator = 0
running = True

while running:
    opcode = memory[pc]
    pc += 1

    if opcode == 0x01:       # Sonraki değeri yazmaca yükler
        accumulator = memory[pc]
        pc += 1
    elif opcode == 0x02:     # Sonraki değeri yazmaca ekler
        accumulator += memory[pc]
        pc += 1
    elif opcode == 0xFF:     # Sanal işlemciyi durdurur
        running = False

print(accumulator)
```

Bu örnek gerçek bir konsol işlemcisinden çok daha basittir. Yine de emülatörün temel mantığını gösterir: Baytlar komut olarak yorumlanır ve sanal donanımın durumu güncellenir.

## Grafik ve ses neden daha zordur?

Retro konsollar görüntüyü modern ekran kartları gibi üretmez. Karakter blokları, sprite'lar, paletler ve tarama çizgileri kullanabilirler. Bazı oyunlar donanımın belirli bir tarama çizgisindeki davranışına güvenerek ekran efektleri oluşturur. Bu yüzden yalnızca doğru pikselleri çizmek yetmez; onları doğru anda çizmek gerekir.

Ses tarafında da kare, üçgen veya gürültü dalgaları üreten özel kanallar bulunur. Örneğin ideal bir kare dalganın temel frekansı $f$ ise üst harmonikleri $3f$, $5f$ ve $7f$ gibi tek katlarda görülür. Emülatör bu kanalları modern ses örneklerine dönüştürürken gecikme ve senkronizasyon sorunlarını önlemelidir.

## Doğruluk mu, hız mı?

Emülatör geliştiricileri genellikle iki hedef arasında denge kurar. **Yorumlama**, her eski işlemci komutunu tek tek işler; anlaşılır ve doğru olabilir fakat yavaştır. **Dinamik yeniden derleme** ise komut bloklarını hedef işlemcinin koduna çevirerek hız kazandırır. Ancak önbellek, zamanlama ve kendi kodunu değiştiren programlar işi karmaşıklaştırabilir.

Cycle-accurate adı verilen emülatörler, donanımın saat döngülerini ayrıntılı biçimde taklit eder. Böylece özel grafik efektleri ve nadir oyunlar daha doğru çalışır; karşılığında daha güçlü bir cihaz gerekir.

Emülasyon, oyun oynamanın yanında dijital koruma açısından da değerlidir. Yaşlanan kartuşlar ve bozulan konsollar ortadan kaybolurken doğru belgelenmiş emülatörler donanım bilgisini gelecek nesillere taşır. Elbette emülatör yazılımı ile telif hakkına tabi oyun dosyaları aynı şey değildir; ROM kullanırken yerel yasalara ve lisanslara dikkat etmek gerekir. Kısacası her çalışan retro oyun, arka planda milyonlarca küçük donanım davranışının ustaca sahnelendiği teknolojik bir tiyatrodur.
