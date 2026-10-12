---
layout: post
title: "Shamir'in Sır Paylaşma Şeması: Bir Sırrı Matematikle Parçalara Ayırmak"
math: true
categories: 
  - Bilgi
tags: 
  - kriptografi
  - shamir
  - sır paylaşımı
  - bilgi güvenliği
  - python
  - matematik
toc: true
image: /img/shamirin-sir-paylasma-18.png
---

Bir kasanın parolasını tek bir kişiye emanet etmek risklidir: Kişi parolayı unutabilir, kötüye kullanabilir veya ortadan kaybolabilir. Parolayı herkese vermekse güvenliği tamamen bozar. Shamir'in Sır Paylaşma Şeması, bu ikilemi zarif bir matematik fikriyle çözer: Sır, tek başına anlamsız görünen paylara bölünür ve yalnızca yeterli sayıda pay bir araya geldiğinde yeniden oluşturulabilir.
``
## Eşik mantığı nedir?

Adi Shamir tarafından 1979'da geliştirilen yöntem, bir **eşik şemasıdır**. Sistem genellikle $(t,n)$ biçiminde gösterilir:

- $n$: Üretilen toplam pay sayısıdır.
- $t$: Sırrı kurtarmak için gereken en az pay sayısıdır.

Örneğin $(3,5)$ şemasında beş kişiye birer pay dağıtılır. Herhangi üç kişi birlikte sırrı bulabilir; ancak bir veya iki kişinin elindeki bilgiler yeterli olmaz. Böylece hem güvenlik hem de hata toleransı sağlanır.

| Yaklaşım | Sırrı kurtarma koşulu | Temel risk |
|---|---:|---|
| Tek kişiye emanet | 1 kişi | Tek hata noktası |
| Herkese tam kopya verme | 1 kişi | Sızıntı ihtimali yüksek |
| Shamir $(3,5)$ | Herhangi 3 kişi | Payların güvenli dağıtılması gerekir |

## İşin arkasındaki matematik

Yöntemin kalbinde polinomlar bulunur. Temel gerçek şudur: Derecesi $t-1$ olan bir polinomu kesin olarak belirlemek için $t$ farklı noktaya ihtiyaç vardır. İki nokta bir doğruyu, üç nokta bir parabolü belirler.

Sır $S$, polinomun sabit terimi yapılır:

$$f(x)=S+a_1x+a_2x^2+...+a_{t-1}x^{t-1} \pmod p$$

Buradaki $a_i$ değerleri rastgele seçilir. $p$ ise sırdan ve hesaplamalarda kullanılan değerlerden büyük bir asal sayıdır. Her katılımcıya $(x,f(x))$ biçiminde farklı bir nokta verilir. Sırrın kendisi polinom üzerinde $(0,f(0))$ noktasıdır; çünkü $f(0)=S$ olur.

Hesaplamalar normal tam sayılar yerine sonlu bir alanda, yani modulo $p$ altında yapılır. Bu seçim taşmaları sınırlar ve eksik paylardan sırrın yaklaşık olarak tahmin edilmesini engeller. Yeterli noktaya sahip kişiler **Lagrange interpolasyonu** uygulayarak $f(0)$ değerini hesaplar.

## Python ile küçük bir örnek

Aşağıdaki kod, eğitim amacıyla $(3,5)$ düzeninde pay üretir. Gerçek sistemlerde `random` yerine kriptografik olarak güvenli `secrets` modülü kullanılmıştır.

```python
from secrets import randbelow

PRIME = 2089

def split_secret(secret, threshold=3, share_count=5):
    if not 0 <= secret < PRIME:
        raise ValueError("Sır, asal sayıdan küçük olmalı")

    coefficients = [secret]
    coefficients += [randbelow(PRIME) for _ in range(threshold - 1)]

    def evaluate(x):
        return sum(coef * pow(x, power, PRIME)
                   for power, coef in enumerate(coefficients)) % PRIME

    return [(x, evaluate(x)) for x in range(1, share_count + 1)]

shares = split_secret(1234)
print(shares)
```

`coefficients` listesinin ilk elemanı sırdır; diğer elemanlar polinomu gizleyen rastgele katsayılardır. `evaluate` fonksiyonu her katılımcı için farklı bir nokta hesaplar. Üretilen tek bir paya bakıldığında `1234` değerini doğrudan çıkarmak mümkün değildir.

## Neden güvenlidir?

$t-1$ veya daha az pay elde eden saldırgan, eksik noktaları tamamlayabilecek çok sayıda farklı polinomla karşılaşır. Bu polinomların sabit terimleri farklı sırlar olabilir. Dolayısıyla saldırgan, doğru sır hakkında matematiksel bir avantaj kazanmaz. Bu özellik, katsayıların gerçekten rastgele seçildiği ve sonlu alan işlemlerinin doğru uygulandığı durumda geçerlidir.

| Özellik | Sağladığı fayda |
|---|---|
| Eşik yapısı | Tek kişinin sırrı açmasını önler |
| Rastgele katsayılar | Eksik paylardan bilgi sızmasını engeller |
| Fazladan paylar | Bazı paylar kaybolsa bile kurtarma sağlar |
| Merkezi olmayan saklama | Tek hata noktasını azaltır |

Shamir şeması; kripto para cüzdanlarının kurtarılmasında, sertifika anahtarlarında, şirket kasalarında ve kritik altyapılarda kullanılabilir. Ancak payların kimlik doğrulaması yapılmadan paylaşılması, asal sayıların yanlış seçilmesi veya payların açık kanallardan gönderilmesi sistemi zayıflatabilir. Matematik sırrı böler; operasyonel güvenlik ise parçaların yanlış ellere düşmemesini sağlar.

![shamirin-sir-paylasma-18](/img/shamirin-sir-paylasma-18.svg)

