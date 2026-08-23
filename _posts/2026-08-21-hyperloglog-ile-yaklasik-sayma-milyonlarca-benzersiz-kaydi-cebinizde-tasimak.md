---
layout: post
title: "HyperLogLog ile Yaklaşık Sayma: Milyonlarca Benzersiz Kaydı Cebinizde Taşımak"
math: true
categories: 
  - Bilgi
tags: 
  - hyperloglog
  - algoritmalar
  - veri mühendisliği
---

Bir e-ticaret sitesinde kaç farklı kullanıcının ürünü görüntülediğini, bir log kümesinde kaç benzersiz IP bulunduğunu ya da bir kampanyanın gerçek erişimini saymak istiyorsunuz. Tüm kimlikleri `Set` içinde tutmak kesin sonuç verir; ancak yüz milyonlarca kayıt geldiğinde bellek bütçeniz hızla tükenir. HyperLogLog (HLL), bu noktada küçük ve sabit sayılabilecek bellek karşılığında çok isabetli bir **yaklaşık benzersiz eleman sayısı** üretir.
``
HLL'nin temel fikri şaşırtıcı derecede zariftir: İyi dağılan bir hash fonksiyonu, kayıtları rastgele bit dizileri gibi davranmaya zorlar. Rastgele bir bit dizisinin başında çok sayıda sıfır görülmesi nadirdir. Örneğin `000001...` ile başlayan bir hash, yaklaşık olarak $2^5$ deneme sonunda görülmesi beklenen bir olaya işaret eder. Bu nedenle gözlenen en uzun baştaki sıfır serisi, veri kümesinin büyüklüğü hakkında ipucu verir.

Tek bir böyle gözlem oldukça oynaktır; HLL bu gürültüyü azaltmak için hash'in ilk $p$ bitini **register** (kova) seçmekte kullanır. Kalan bitlerdeki ilk `1` konumu $\rho$ olarak kaydedilir. Her register yalnızca gördüğü en büyük $\rho$ değerini saklar. Register sayısı $m = 2^p$ olduğunda klasik tahminci kabaca şöyledir:

$$\hat{n}=\alpha_m m^2\left(\sum_{j=1}^{m}2^{-M[j]}\right)^{-1}$$

Buradaki $M[j]$, j'nci register'ın maksimum değeridir; $\alpha_m$ ise küçük sistematik hataları dengeleyen bir sabittir. HLL'nin beklenen bağıl standart hatası da yaklaşık $1.04/\sqrt{m}$ seviyesindedir. Yani $p=14$ için $m=16.384$ register kullanır ve hata kabaca $%0,81$ olur. Bu, analitik paneller için harika; banka bakiyesi hesaplamak için ise kesinlikle uygun değildir.

| Yaklaşım | Bellek maliyeti | Sonuç | Birleştirme |
|---|---:|---|---|
| `Set` / hash kümesi | Benzersiz kayıtla doğrusal büyür | Kesin | Küme birleşimi maliyetli |
| Bitmap | Evren küçükse verimli | Kesin | Bit düzeyinde kolay |
| HyperLogLog | Register sayısı kadar sabit | Yaklaşık | Register bazında `max` |

Dağıtık sistemlerde HLL'nin süper gücü birleşebilmesidir. İki sunucunun aynı register indeksindeki değerlerinden büyük olanı alınır. Böylece ham kullanıcı listelerini taşımadan günlük, saatlik veya bölgesel sayaçları birleştirebilirsiniz. Aynı kullanıcının bin kez gelmesi register değerini genellikle değiştirmez; bu da yapıyı doğal biçimde tekrar kayıtsız yapar.

Aşağıdaki eğitim amaçlı JavaScript örneği, üretimde Redis `PFADD`/`PFCOUNT` veya PostgreSQL eklentileri yerine mantığı görünür kılar. Gerçek projede kriptografik olmayan ama kaliteli 64 bitlik bir hash seçmek ve büyük sayılarda düzeltme kurallarını uygulamak gerekir.

```js
class MiniHLL {
  constructor(p = 10) {
    this.p = p;
    this.m = 1 << p;
    this.reg = new Uint8Array(this.m);
  }

  add(value) {
    const h = hash32(String(value)); // İyi dağılımlı 32 bit hash varsayımı
    const index = h >>> (32 - this.p);
    const rest = (h << this.p) | (1 << (this.p - 1));
    const rho = Math.clz32(rest) + 1;
    this.reg[index] = Math.max(this.reg[index], rho);
  }

  count() {
    let sum = 0;
    for (const r of this.reg) sum += 2 ** (-r);
    const alpha = 0.7213 / (1 + 1.079 / this.m);
    return Math.round(alpha * this.m * this.m / sum);
  }
}
```

Örnekteki `add`, hash'ten kovayı seçer ve nadirlik bilgisini register'a yazar; `count` ise harmonik ortalama fikrini formüle dönüştürür. Küçük kardinalitelerde boş register sayısını kullanan linear counting düzeltmesi, büyük değerlerde ise hash alanı doygunluk düzeltmesi gerekir. Kısacası HLL, “tam olarak kimler vardı?” sorusunu değil, “kaç farklı kişi vardı?” sorusunu düşük maliyetle yanıtlar; doğru soru sorulduğunda milyonluk veriyi birkaç kilobayta sığdırır.
