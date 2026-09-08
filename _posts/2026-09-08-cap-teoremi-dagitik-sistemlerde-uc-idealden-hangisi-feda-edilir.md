---
layout: post
title: "CAP Teoremi: Dağıtık Sistemlerde Üç İdealden Hangisi Feda Edilir?"
math: true
categories: 
  - Bilgi
tags: 
  - dağıtık sistemler
  - cap teoremi
  - sistem mimarisi
toc: true
---

Dağıtık sistem tasarlamak, üç önemli özelliği aynı valize sığdırmaya çalışmaya benzer: tutarlılık, erişilebilirlik ve ağ bölünmelerine tolerans. CAP Teoremi, ağ koptuğunda bu valizin kapanmayacağını ve mimarın zorunlu bir seçim yapması gerektiğini söyler. Bu nedenle mesele “mükemmel veritabanını” bulmak değil, sistemin hangi hata durumunda nasıl davranacağını bilinçli biçimde belirlemektir.
``
## CAP’in Üç Köşesi

CAP kısaltması aşağıdaki özelliklerden gelir:

- **Consistency (Tutarlılık):** Her okuma, en güncel yazma işlemini veya bir hata sonucunu görür. Buradaki tutarlılık çoğunlukla güçlü tutarlılık, yani *linearizability* anlamındadır.
- **Availability (Erişilebilirlik):** Hata almamış her düğüme gönderilen istek, sonsuza kadar beklemeden geçerli bir yanıt alır. Yanıtın en güncel veriyi içermesi şart değildir.
- **Partition Tolerance (Bölünme Toleransı):** Düğümler arasındaki mesajlar kaybolsa veya gecikse bile sistem çalışmayı sürdürür.

Bunları küme gösterimiyle düşünürsek arzulanan sistem şudur:

$$S = C \cap A \cap P$$

Ancak gerçek bir ağ bölünmesi sırasında CAP’in sonucu şöyledir:

$$P \Rightarrow (C \oplus A)$$

Buradaki $\oplus$, pratikte tutarlılık ile erişilebilirlik arasında seçim yapılması gerektiğini vurgular. Bu ifade, normal çalışma sırasında sistemin hem tutarlı hem erişilebilir olamayacağı anlamına gelmez. Kısıtlama özellikle **partition gerçekleştiğinde** ortaya çıkar.

## Çelişki Nasıl Doğar?

A ve B adlı iki düğümün bağlantısının koptuğunu düşünelim. Kullanıcı A üzerinde bakiyeyi 100 TL’den 50 TL’ye düşürüyor. Aynı anda başka bir kullanıcı B’den bakiyeyi okuyor. B, A’daki güncellemeyi öğrenemez.

- B isteği reddederse güncel olmayan veri gösterilmez; **tutarlılık korunur, erişilebilirlik feda edilir**.
- B eski değer olan 100 TL’yi döndürürse hizmet yanıt vermeyi sürdürür; **erişilebilirlik korunur, tutarlılık feda edilir**.

Ağ bağlantısı yokken B’nin hem kesin güncel değeri bilmesi hem de mutlaka yanıt vermesi mümkün değildir. Çelişkinin kalbi budur: Bilgi, düğümler arasında sihirli biçimde ışınlanamaz.

| Yaklaşım | Bölünme anındaki tercih | Avantaj | Bedel | Uygun örnek |
|---|---|---|---|---|
| CP | Tutarlılık | Yanlış veya eski veri engellenir | Bazı istekler reddedilir | Banka bakiyesi, kilit servisi |
| AP | Erişilebilirlik | Sistem yanıt vermeyi sürdürür | Geçici veri uyuşmazlığı oluşur | Sosyal akış, beğeni sayısı |
| CA | İkisini normal koşullarda sunar | Basit kullanım modeli | Gerçek bölünmeye dayanamaz | Tek düğümlü ilişkisel sistem |

## CP Kararı Kodda Nasıl Görünür?

Aşağıdaki basitleştirilmiş Python örneği, yazma işlemi için çoğunluk onayı arar:

```python
def write_with_quorum(nodes, key, value):
    required = len(nodes) // 2 + 1
    acknowledgements = 0

    for node in nodes:
        try:
            node.write(key, value)
            acknowledgements += 1
        except NetworkError:
            pass

    if acknowledgements < required:
        raise UnavailableError("Tutarlılık için yeterli çoğunluk yok")

    return True
```

Kod, yeterli düğüm güncellenemediğinde başarılı yanıt üretmez. Böylece eski bir liderin bağımsız yazma kabul etmesi önlenir; fakat istemci açısından sistem geçici olarak erişilemez olur. Konsensüs tabanlı sistemlerde benzer kararlar Raft veya Paxos gibi protokollerle daha güvenli biçimde uygulanır.

AP sistemleri ise yazmayı yerel düğümde kabul edip değişiklikleri bağlantı düzeldiğinde birleştirebilir. Bu süreçte *eventual consistency*, sürüm vektörleri, zaman damgaları veya CRDT yapıları kullanılabilir. Çakışma çözümü “son yazan kazanır” kadar basit olabileceği gibi iş kurallarına dayalı da olabilir.

## Tasarımcı Aslında Neyi Seçer?

“Veritabanımız CP mi, AP mi?” sorusu tek başına yetersizdir. Seçim işlem, veri türü ve hatta uç nokta bazında değişebilir. Ödeme işlemleri güçlü tutarlılık isterken ürün yorumları kısa süreli tutarsızlığı tolere edebilir.

PACELC yaklaşımı resmi tamamlar: Bölünme varsa **Availability–Consistency**, bölünme yoksa **Latency–Consistency** arasında feragat yapılır. Yani ağ sağlıklıyken bile uzak düğümlerden onay beklemek tutarlılığı artırırken gecikmeyi yükseltir.

CAP bir ürün etiketi değil, hata anında verilecek kararları görünür kılan bir düşünme aracıdır. İyi mimari üç özelliğe birden sahip olduğunu iddia etmez; hangi verinin ne kadar eski kalabileceğini, hangi isteğin reddedileceğini ve uzlaşmanın nasıl sağlanacağını açıkça tanımlar.
