---
layout: post
title: "Hamilton Yolu Problemi: Her Düğümü Bir Kez Ziyaret Etmek Neden Bu Kadar Zor?"
math: true
categories: 
  - Bilgi
tags: 
  - graf teorisi
  - hamilton yolu
  - algoritmalar
  - np-tam
  - python
  - karmaşıklık
toc: true
---

Bir şehir turu planladığınızı düşünün: Her şehre tam bir kez uğrayacak, ancak başladığınız yere dönmek zorunda olmayacaksınız. Haritada bazı şehirler arasında doğrudan yol bulunmadığında işler hızla karışır. Graf teorisindeki **Hamilton yolu problemi**, tam olarak bu turun mümkün olup olmadığını sorar. Tanımı tek cümleye sığsa da çözümü bilgisayarları ciddi biçimde terletebilir.

``

Bir grafı $G=(V,E)$ olarak gösterelim. Burada $V$ düğüm kümesini, $E$ ise düğümler arasındaki kenarları temsil eder. Hamilton yolu, graftaki her düğümü **tam olarak bir kez** ziyaret eden bir düğüm dizisidir:

$$v_1, v_2, \ldots, v_n$$

Bu dizinin geçerli olması için her ardışık ikili arasında bir kenar bulunmalıdır:

$$(v_i,v_{i+1}) \in E \quad \text{ve} \quad 1 \leq i<n$$

Yolun son düğümü başlangıç düğümüne de bağlıysa ortaya bir **Hamilton çevrimi** çıkar. Buradaki kritik nokta, düğümlerin tekrar ziyaret edilememesidir. Yanlış bir seçim yaptığınızda ileride ulaşılması gereken bir düğümü erişilemez bırakabilirsiniz.

## Euler yolu ile karıştırmayalım

Hamilton ve Euler problemleri benzer görünür, fakat ziyaret ettikleri şey farklıdır:

| Özellik | Hamilton yolu | Euler yolu |
|---|---|---|
| Tam bir kez ziyaret edilen | Düğümler | Kenarlar |
| Kolay bir karakterizasyon var mı? | Genel durumda hayır | Evet |
| Karar probleminin durumu | NP-tam | Polinom zamanda çözülebilir |
| Temel odak | Ziyaret sırası | Düğüm dereceleri |

Euler yolu için tek dereceli düğümleri saymak çoğu zaman yeterlidir. Hamilton yolu içinse düğüm derecelerine bakarak her grafı kapsayan benzer bir reçete elde edemeyiz. Yerel olarak mantıklı görünen bir adım, küresel çözümü bozabilir.

## Neden bu kadar zor?

$n$ düğümlü bir grafta bütün ziyaret sıralarını denemek istersek en kötü durumda $n!$ farklı permütasyonla karşılaşırız. Örneğin:

$$20! \approx 2.43 \times 10^{18}$$

Saniyede milyonlarca seçeneği inceleyen bir bilgisayar bile bu uzayda pikniğe çıkmış sayılmaz. Üstelik Hamilton yolu problemi **NP-tamdır**. Yani verilen bir yolu hızlıca doğrulayabiliriz, fakat her graf için hızlı çalışan genel bir çözüm algoritması bilinmemektedir.

Aşağıdaki geri izleme algoritması, bir düğüm seçer ve çıkmaza girerse önceki seçime geri döner:

```python
def hamilton_yolu(graf):
    dugumler = list(graf)

    def ara(yol, ziyaret):
        if len(yol) == len(dugumler):
            return yol[:]

        son = yol[-1]
        for komsu in graf[son]:
            if komsu not in ziyaret:
                ziyaret.add(komsu)
                yol.append(komsu)

                sonuc = ara(yol, ziyaret)
                if sonuc:
                    return sonuc

                yol.pop()          # Yanlış seçimi geri al
                ziyaret.remove(komsu)
        return None

    for baslangic in dugumler:
        sonuc = ara([baslangic], {baslangic})
        if sonuc:
            return sonuc
    return None
```

Bu kod, komşuları deneyerek yolu büyütür. Tüm düğümlere ulaştığında çözümü döndürür; çıkmazda ise son adımı geri alır. Doğru çalışmasına rağmen en kötü durumdaki zamanı üstel büyüyebilir. Bit maskeleriyle dinamik programlama kullanıldığında süre yaklaşık $O(n^2 2^n)$ seviyesine indirilebilir, ancak bu da büyük graflar için pahalıdır.

## Pratikte ne yapılır?

Küçük graflarda geri izleme ve dinamik programlama yeterlidir. Daha büyük örneklerde dal-sınır, sezgisel arama, SAT çözücüleri veya tamsayılı programlama tercih edilebilir. Ayrıca grafın özel yapısı işleri kolaylaştırabilir. Örneğin yoğun graflarda Dirac teoremi gibi yeter koşullar bir Hamilton çevriminin varlığını garanti edebilir.

Hamilton yolu bize önemli bir algoritma dersini hatırlatır: Bir çözümü kontrol etmenin kolay olması, o çözümü bulmanın da kolay olduğu anlamına gelmez. Her düğümü yalnızca bir kez ziyaret etmek basit bir kuraldır; fakat olası sıralamaların patlayıcı büyümesi, bu küçük kuralı bilgisayar biliminin en ünlü bilmecelerinden birine dönüştürür.
