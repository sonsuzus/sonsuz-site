---
layout: post
title: "Her Kopya Aynı Anda Haklı Olmak Zorunda mı? Nihai Tutarlılığın Teorisi"
math: true
categories: 
  - Bilgi
tags: 
  - dağıtık sistemler
  - eventual consistency
  - cap teoremi
toc: true
---

Bir veritabanında yazdığımız değeri hemen ardından okuyabilmek doğal bir beklentidir. Ancak veri farklı sunuculara, bölgelere ve hatta kıtalara yayıldığında “hemen” kelimesi pahalılaşır. Dağıtık sistemler bu nedenle bazen bütün kopyaları anında eşitlemek yerine kısa süreli görüş ayrılıklarına izin verir. Nihai tutarlılık, sistem sakinleştiğinde tüm kopyaların aynı değerde buluşacağını garanti eden bu pragmatik yaklaşımın adıdır.
``
## Anlık tutarlılık neden zorlaşır?

Tek sunuculu bir veritabanında işlemlerin sırası merkezi olarak belirlenebilir. Dağıtık bir yapıda ise aynı verinin $N$ farklı kopyası bulunabilir. Bir yazmanın başarılı sayılması için bütün kopyalardan yanıt beklersek yaklaşık gecikme şöyle düşünülebilir:

$$L_{write} = max(L_1, L_2, ..., L_N)$$

Yani hızımızı çoğu zaman en yavaş düğüm belirler. Üstelik ağ bağlantısı kopabilir, paketler gecikebilir veya bir veri merkezi geçici olarak erişilemez olabilir. Sistem tüm düğümleri beklerse tutarlılığı korur ama kullanılabilirliğini kaybedebilir. Beklemezse hizmet vermeyi sürdürür fakat bazı istemciler eski veri okuyabilir.

## CAP teoreminin asıl mesajı

CAP teoremi, bir ağ bölünmesi sırasında dağıtık sistemin hem güçlü tutarlılığı hem de tam kullanılabilirliği aynı anda garanti edemeyeceğini söyler:

- **Consistency (C):** Her okuma en güncel yazmayı görür.
- **Availability (A):** Her istek, hata yerine geçerli bir yanıt alır.
- **Partition tolerance (P):** Ağ parçalanmasına rağmen sistem çalışmayı sürdürür.

Gerçek sistemlerde ağ bölünmelerini tamamen yok sayamayız. Dolayısıyla $P$ pratikte zorunludur; kritik seçim çoğunlukla $C$ ile $A$ arasında yapılır. Nihai tutarlılık tercih edildiğinde sistem, bölünme sırasında eski veri döndürme ihtimali pahasına istekleri kabul etmeyi sürdürür.

| Yaklaşım | Okuma davranışı | Gecikme | Bölünme sırasında sonuç | Uygun örnek |
|---|---|---:|---|---|
| Güçlü tutarlılık | En güncel değer | Genellikle yüksek | Bazı istekler reddedilebilir | Banka bakiyesi |
| Nihai tutarlılık | Geçici olarak eski değer | Genellikle düşük | Hizmet devam eder | Beğeni sayısı |
| Oturum tutarlılığı | Kullanıcı kendi yazdığını görür | Orta | Sınırlı garanti sunar | Profil düzenleme |

CAP yalnızca arıza anını açıklar. **PACELC** yaklaşımı tabloyu genişletir: Bölünme varsa kullanılabilirlik ile tutarlılık; bölünme yoksa gecikme ile tutarlılık arasında seçim yapılır. Başka bir ifadeyle bedel yalnızca sistem bozulduğunda değil, normal çalışırken de ödenir.

## Quorum ile ayar düğmesini çevirmek

Kopyalı sistemlerde $N$ toplam kopya, $W$ yazma onayı ve $R$ okuma yanıtı olsun. Şu koşul sağlanırsa okuma ve yazma kümeleri en az bir düğümde kesişir:

$$R + W > N$$

Örneğin $N=3$, $W=2$ ve $R=2$ güçlü tutarlılığa yaklaşır. Buna karşılık $W=1$ ve $R=1$ daha hızlıdır, fakat eski veri okuma ihtimalini artırır. Böylece tutarlılık ikili bir anahtardan çok ayarlanabilir bir düğmeye dönüşür.

```python
# Üç kopyadan en az ikisi aynı değeri söylüyorsa çoğunluğu seçer.
def quorum_read(replicas):
    values = [node.read("stock") for node in replicas]
    return max(set(values), key=values.count)
```

Bu basitleştirilmiş kod çoğunluk okumasının fikrini gösterir. Gerçek sistemler yalnızca değeri değil; sürüm numarası, zaman damgası veya vektör saati gibi metadata bilgilerini de karşılaştırır.

## Kopyalar nasıl yeniden barışır?

Nihai tutarlılık “rastgele sonuçlar” anlamına gelmez. Arka plandaki çoğaltma, anti-entropy, read repair ve conflict resolution mekanizmaları kopyaları yakınlaştırır. Çakışmalar son yazan kazanır yaklaşımıyla, uygulamaya özel birleştirme kurallarıyla veya CRDT gibi matematiksel veri yapılarıyla çözülebilir.

Esas tasarım sorusu şudur: Kullanıcı birkaç saniye eski veri görürse ne olur? Sosyal medya sayacı biraz gecikirse dünya dönmeye devam eder; aynı tolerans çift harcama veya stok düşümü için tehlikelidir. Bu yüzden nihai tutarlılık güçlü tutarlılığın ucuz taklidi değil, gecikme, ölçeklenebilirlik ve kullanılabilirlik lehine verilmiş bilinçli bir mühendislik kararıdır.
