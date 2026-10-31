---
layout: post
title: "Ev Sessizleşince: Hareket Sensörleriyle Günlük Rutinlerdeki Sapmaları Yakalamak"
math: true
categories: 
  - Proje
tags: 
  - iot
  - python
  - anomali tespiti
  - hareket sensörleri
  - veri analizi
  - yaşlı bakımı
toc: true
image: /img/ev-sessizlesince-hareket-72.png
---

![ev-sessizlesince-hareket-72](/img/ev-sessizlesince-hareket-72.svg)


Sabah mutfakta başlayan hareketlilik, öğleden sonra salona taşınan sakinlik… Evlerin de kendine özgü bir ritmi vardır. Hareket sensörleri, bu ritimdeki beklenmedik değişiklikleri görünür kılabilir. Ama amaç eve dijital bir Sherlock yerleştirmek değil; yaşlı veya yalnız yaşayan bireylerin bağımsızlığını korurken, gerektiğinde iletişim kurulmasını destekleyen, mahremiyete saygılı bir yardımcı geliştirmektir.
``

## Sensör gerçekten neyi bilir?

Yaygın PIR sensörleri, görüş alanlarındaki kızılötesi değişimlerden hareket çıkarır. Birinin kim olduğunu, ne yaptığını veya sağlık durumunu doğrudan söylemezler. Dolayısıyla “hareket yok” ile “kişi tehlikede” aynı anlama gelmez: Uyku, dışarı çıkma, kitap okuma veya bağlantı arızası benzer kayıtlar oluşturabilir.

Temel veri akışı şöyledir: Sensör olayı, zaman damgası ve oda bilgisi yerel bir ağ geçidine ulaşır; ardından analiz için özetlenir. Saatlerin eşitlenmesi ve yinelenen kayıtların temizlenmesi önemlidir. Olay kaydı göndermeyen cihazın çalıştığını anlayabilmek için ayrıca düzenli durum mesajları gerekir. Aksi hâlde arızalı sensör, sessiz bir ev gibi görünür.

## Ham olaylardan anlamlı özelliklere

Sensörün yeniden tetikleme süresi, olay sayısını etkiler. Bu nedenle yalnızca tetikleme sayısını karşılaştırmak yanıltıcıdır. Daha dengeli bir özellik, otuz dakikalık pencerede hareket görülen farklı dakikaların sayısıdır. Bütün odaların kayıtları birleştirilir; aynı dakika iki odada hareket varsa toplamda bir kez sayılır.

| Özellik | Ne anlatır? | Tek başına neden yetmez? |
|---|---|---|
| Hareketli dakika | Genel etkinlik düzeyi | Dışarı çıkmak da azaltır |
| Hareketsizlik süresi | Uzun sessizlik dönemleri | Uyku sırasında normaldir |
| Odalar arası geçiş | Ev içindeki hareketlilik | Misafirler örüntüyü değiştirir |
| Cihaz durum mesajı | Veri akışının sağlığı | İnsan davranışını ölçmez |

İlk üç veya dört hafta, kişinin kendi referansını oluşturmak için kullanılabilir. Hafta içi ve hafta sonu ayrı değerlendirilmelidir. Karşılaştırma başka insanların ortalamasıyla değil, aynı kişinin benzer zaman dilimlerindeki geçmişiyle yapılır.

## Normalden uzaklığı ölçmek

Başlangıç için karmaşık bir sinir ağı şart değildir. Medyan, sıra dışı günlerden ortalamaya göre daha az etkilenir. Yayılımı ölçen medyan mutlak sapma ise $MAD = \operatorname{medyan}(\vert x_i-m\vert )$ şeklinde hesaplanır; burada $m$, geçmiş değerlerin medyanıdır.

Azalan etkinlik için kullanılabilecek sağlamlaştırılmış skor:

$$z_t = \frac{m-x_t}{\max(1,\;1.4826\cdot MAD)}$$

Burada $x_t$, güncel penceredeki hareketli dakika sayısıdır. Paydadaki 1, bir dakikalık alt sınırdır; geçmiş değerler aynı olduğunda sıfıra bölmeyi önler. Büyük pozitif skor, beklenenden düşük etkinlik gösterir. Örneğin medyan 18, MAD 3 ve güncel değer 2 olduğunda skor yaklaşık 3,6 olur. Ancak 3 gibi bir eşik yalnızca başlangıç tercihidir; klinik olarak doğrulanmış bir sınır değildir.

## Python ile aday sapmaları çıkaralım

Aşağıdaki kod, geçmiş özetlerden profil oluşturur ve güncel pencereleri karşılaştırır. `dilim`, gün içindeki otuz dakikalık zaman aralığını temsil eder. Güncel kayıtların geçmiş eğitim verisine katılmaması önemlidir.

```python
import pandas as pd

anahtar = ['gun_tipi', 'dilim']
grup = gecmis.groupby(anahtar)['aktif_dakika']

profil = grup.agg(merkez='median', ornek='count')
profil['mad'] = grup.apply(
    lambda s: (s - s.median()).abs().median()
)
profil['olcek'] = (1.4826 * profil['mad']).clip(lower=1)

sonuc = guncel.merge(
    profil.reset_index(),
    on=anahtar,
    how='left',
    validate='many_to_one'
)
sonuc['puan'] = (
    sonuc['merkez'] - sonuc['aktif_dakika']
) / sonuc['olcek']

sonuc['aday'] = (
    (sonuc['puan'] > 3)
    & (sonuc['ornek'] >= 6)
    & sonuc['sensorler_cevrimici']
    & sonuc['evde_olmasi_bekleniyor']
)
```

`gecmis` ve `guncel`, önceden hazırlanmış DataFrame tablolarıdır. Çıktı acil durum kararı değil, inceleme adayıdır. Evde bulunma beklentisi, yalnızca hareket yokluğundan çıkarılmamalı; kişinin belirttiği program gibi izinli bağlamlarla desteklenmelidir.

## Alarm değil, kontrollü iletişim

Tek pencere yerine ardışık pencerelerdeki sapmalar değerlendirilebilir. Ancak beklemek acil durumları geciktirebileceğinden, bu sistem tıbbi alarmın yerine geçmez. Bildirim politikası kişiyle birlikte belirlenmeli; önce nazik bir kontrol mesajı, gerekiyorsa yetkilendirilmiş yakına bildirim düşünülmelidir.

Başarıyı yalnızca doğrulukla ölçmeyin. Haftalık yanlış bildirim sayısı, tespit gecikmesi ve gözden kaçan olaylar da izlenmelidir. Tatiller veya kalıcı rutin değişiklikleri sonrasında profil kontrollü biçimde güncellenmelidir.

Son olarak, açık rıza, bildirimleri durdurabilme, sınırlı saklama süresi ve erişim kontrolü tasarımın temelidir. Mümkünse ham verileri evde tutup yalnızca gerekli özetleri paylaşın. İyi sistem, her sessizliği felaket sayan değil; belirsizliğini kabul edip insan iletişimini destekleyen sistemdir.
