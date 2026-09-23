---
layout: post
title: "CAP Teoremi: Dağıtık Sistemlerde Neden Her Şeyi Aynı Anda Elde Edemiyoruz?"
math: true
categories: 
  - Bilgi
tags: 
  - cap teoremi
  - dağıtık sistemler
  - veritabanı
  - tutarlılık
  - yüksek erişilebilirlik
  - sistem tasarımı
toc: true
image: /img/cap-teoremi-dagitik-56.png
---

![cap-teoremi-dagitik-56](/img/cap-teoremi-dagitik-56.svg)


Bir uygulamayı tek sunucudan çıkarıp dünyanın farklı bölgelerindeki sunuculara dağıttığınızda işler hızlanabilir, sistem daha dayanıklı olabilir ve kullanıcılar uygulamaya daha kolay ulaşabilir. Ancak ağ bağlantıları koptuğunda önemli bir seçim kapıyı çalar: Sistem doğru cevabı mı beklemeli, yoksa elindeki bilgiyle hemen cevap mı vermeli? CAP teoremi, dağıtık sistemlerin bu tatsız fakat kaçınılmaz ikilemini açıklar.

``

## CAP harfleri ne anlatıyor?

CAP; **Consistency**, **Availability** ve **Partition Tolerance** özelliklerinin baş harflerinden oluşur:

- **Tutarlılık (Consistency):** Her okuma işlemi, sistemdeki en güncel yazma işleminin sonucunu görür veya hata alır. Buradaki tutarlılık, çoğunlukla güçlü ya da doğrusal tutarlılık anlamındadır.
- **Erişilebilirlik (Availability):** Hatasız çalışan bir düğüme gönderilen her istek, güncel olmasa bile hata dışı bir yanıt alır.
- **Bölünme toleransı (Partition Tolerance):** Düğümler arasındaki mesajlar kaybolsa veya gecikse bile sistem çalışmayı sürdürür.

Bu özellikleri kısa bir tabloda karşılaştıralım:

| Özellik | Temel soru | Sağlanmadığında ne olur? |
|---|---|---|
| C | Herkes aynı veriyi mi görüyor? | Eski veya çelişkili veri okunabilir. |
| A | Her istek yanıt alıyor mu? | Bazı istekler reddedilir ya da bekletilir. |
| P | Ağ kopunca sistem çalışıyor mu? | Dağıtık yapı iletişim sorununda durabilir. |

## Teoremin asıl söylediği şey

CAP genellikle “Üç özellikten yalnızca ikisini seçebilirsin” diye özetlenir. Bu ifade akılda kalıcıdır fakat biraz yanıltıcıdır. Normal koşullarda tutarlılık ve erişilebilirlik birlikte sağlanabilir. Kritik durum, bir **ağ bölünmesi** gerçekleştiğinde ortaya çıkar.

İki düğümün haberleşemediğini düşünelim. Bir kullanıcı A düğümündeki bakiyeyi güncellerken başka bir kullanıcı B düğümünden aynı bakiyeyi okumak istiyor. B, güncellemeyi doğrulayamaz. Önünde iki seçenek vardır:

1. İsteği reddederek veya bekleterek **tutarlılığı** korumak.
2. Eski olabilecek veriyi döndürerek **erişilebilirliği** korumak.

Bu ilişkiyi basitleştirilmiş biçimde şöyle gösterebiliriz:

$$P \Rightarrow \neg(C \land A)$$

Yani bölünme yaşandığı sürece güçlü tutarlılık ile tam erişilebilirlik aynı anda garanti edilemez. Gerçek dünyadaki ağlar kusursuz olmadığından, dağıtık sistemlerde P çoğu zaman vazgeçilebilir bir özellik değil, tasarımın kabul ettiği bir gerçektir.

## CP ve AP sistemleri

| Yaklaşım | Bölünme sırasında tercih | Uygun örnekler |
|---|---|---|
| CP | Tutarlılık korunur, bazı istekler reddedilir. | Banka bakiyesi, stok kilidi, lider seçimi |
| AP | Yanıt verilir, veri geçici olarak eski olabilir. | Sosyal akış, beğeni sayısı, alışveriş önerileri |

CP yaklaşımında sistem, yeterli düğümün onayını alamıyorsa yazmayı durdurabilir. AP yaklaşımında ise düğümler istekleri kabul eder; bağlantı düzeldiğinde kopyalar uzlaştırılır. Bu model **nihai tutarlılık** olarak bilinir: Yeterince yeni güncelleme gelmezse tüm kopyalar sonunda aynı değere yaklaşır.

Kopya sayısı $N$, yazma onayı $W$ ve okuma onayı $R$ olsun. Genellikle

$$R + W > N$$

koşulu, okuma ve yazma kümelerinin en az bir düğümde kesişmesini sağlayarak güncel veriyi görme ihtimalini güçlendirir. Ancak gecikme ve hata politikaları hâlâ önemlidir.

## Küçük bir uygulama örneği

Aşağıdaki Python benzeri kod, CP davranışını basitleştirerek gösterir:

```python
def update_balance(account, amount, replicas):
    acknowledgements = 0

    for replica in replicas:
        if replica.is_reachable():
            replica.write(account, amount)
            acknowledgements += 1

    majority = len(replicas) // 2 + 1
    if acknowledgements < majority:
        raise RuntimeError("Yeterli çoğunluk yok; yazma reddedildi")

    return "Güncelleme kabul edildi"
```

Kod, yazmayı başarılı saymadan önce çoğunluk onayı arar. Ağ bölünmesinde azınlık tarafı güncelleme yapamaz; böylece çelişkili bakiyeler engellenir. Bunun bedeli, bazı kullanıcıların geçici olarak hata almasıdır.

CAP teoremi belirli bir veritabanına yapıştırılan sabit bir etiket değil, hata anındaki davranışı düşünme aracıdır. İyi sistem tasarımı “CP mi, AP mi?” sorusundan önce hangi verinin ne kadar eski kalabileceğini, hangi işlemin bekleyebileceğini ve yanlış bir cevabın iş açısından maliyetini sorar. Çünkü dağıtık sistemlerde bedava öğle yemeği yoktur; yalnızca bilinçli seçilmiş menüler vardır.
