---
layout: post
title: "MIT, GPL ve Apache: Kodunuzu Hangi Lisansla Özgür Bırakmalısınız?"
math: true
categories: 
  - Bilgi
tags: 
  - açık kaynak
  - yazılım lisansları
  - MIT
  - GPL
  - Apache
---

Açık kaynak dünyasında kod yazmak işin yalnızca yarısıdır; diğer yarısı ise insanların o kodla neler yapabileceğini belirlemektir. Bir lisans, projenizin kullanım, değiştirilme ve dağıtılma kurallarını tanımlayan hukuki bir sözleşmedir. MIT, GPL ve Apache 2.0 sıkça aynı sepete atılsa da ticari kullanım, kaynak kodun paylaşımı ve patent hakları konusunda oldukça farklı karakterlere sahiptir.
``
Bir lisans seçimini basitçe bir kısıt seviyesi olarak düşünebiliriz. Kabaca, geliştiriciye tanınan serbestlik $S$ arttıkça, türetilmiş projenin kaynak kodunu açık tutma zorunluluğu $Z$ azalır. Bu ilişki her zaman matematiksel olarak bire bir olmasa da öğretici bir modeldir: $S \uparrow \Rightarrow Z \downarrow$. MIT en serbest uçta, GPL ise karşılıklılık şartını en güçlü uygulayan taraftadır. Apache 2.0 ise serbest kullanım ile patent koruması arasında dengeli bir konum alır.

| Özellik | MIT | GPLv3 | Apache 2.0 |
|---|---|---|---|
| Ticari kullanım | Serbest | Serbest | Serbest |
| Kaynak kod açma zorunluluğu | Yok | Dağıtımda var | Yok |
| Lisans metni korunmalı mı? | Evet | Evet | Evet |
| Patent maddesi | Açık değil | Patent koruması içerir | Açık patent lisansı içerir |
| Kapalı kaynak projede kullanım | Evet | Genellikle hayır | Evet |

## MIT: “Al, Kullan, Ama İsmimi Silme” Yaklaşımı

MIT lisansı kısa, anlaşılır ve izin verici (*permissive*) bir lisansdır. Kodunuzu herkes kullanabilir, değiştirebilir, satabilir ve hatta kapalı kaynaklı bir ürünün içine gömebilir. Temel koşul, orijinal telif hakkı ve lisans bildiriminin dağıtımda korunmasıdır.

Örneğin bir JavaScript yardımcı kütüphanesi yazdınız ve MIT ile yayımladınız. Bir şirket bu kütüphaneyi ücretli SaaS ürününde kullanabilir; kendi uygulamasının kaynak kodunu paylaşmak zorunda değildir. Bu yüzden MIT, benimsenme hızını artırmak isteyen araç, kütüphane ve eğitim projelerinde popülerdir.

```text
Copyright (c) 2026 Ada Geliştirici

Permission is hereby granted, free of charge, to any person obtaining a copy...
```

Bu lisansın önemli sınırı şudur: Kodunuzun geliştirilmiş sürümlerinin tekrar topluluğa dönmesini zorlayamazsınız. Özgürlük yüksektir, ancak geri katkı garantisi düşüktür.

## GPL: Özgürlük Zincirini Koruyan Copyleft

GNU General Public License, özellikle GPLv3, *copyleft* yaklaşımını kullanır. Copyleft, türetilmiş eserin de aynı özgürlükleri korumasını ister. GPL kodunu içeren ve dağıtılan bir yazılımın kaynak kodu, GPL koşullarıyla erişilebilir olmalıdır.

Buradaki kritik kelime **dağıtım**dır. Bir şirket GPL lisanslı bir aracı kendi sunucusunda kullanıyorsa, her durumda kaynak kodunu yayımlamak zorunda değildir. Ancak bu aracı müşteriye masaüstü uygulaması, cihaz yazılımı veya indirilebilir paket olarak dağıtıyorsa, ilgili kaynak kodunu da sağlamalıdır.

| Senaryo | MIT sonucu | GPL sonucu | Apache 2.0 sonucu |
|---|---|---|---|
| Kodu değiştirip satmak | Mümkün | Mümkün, kaynak açık olmalı | Mümkün |
| Kodunuzu kapalı ürüne eklemek | Mümkün | Lisans uyumluluğuna bağlı, çoğunlukla uygun değil | Mümkün |
| Değişiklikleri yayımlamak | Zorunlu değil | Dağıtımda zorunlu | Zorunlu değil |

GPL, örneğin topluluk tarafından geliştirilen bir medya oynatıcı veya işletim sistemi bileşeni için güçlü bir tercihtir. Amaç, kodun bir şirket tarafından alınıp kapatılmasını engellemektir.

## Apache 2.0: Patent Kalkanlı Esneklik

Apache 2.0, MIT gibi izin vericidir; fakat patent konusunda daha ayrıntılı hükümler barındırır. Katkı sağlayanlar, katkılarıyla ilişkili patentler için kullanıcılara lisans verir. Buna karşılık, bir kullanıcı patent ihlali davası açarsa ilgili patent lisansını kaybedebilir. Bu mekanizma büyük şirketlerin ve çok katkıcılı projelerin risklerini azaltır.

Özellikle kurumsal altyapı projelerinde Apache 2.0 sık görülür. Lisans metnine ek olarak varsa `NOTICE` dosyasını koruma şartı bulunur. Örneğin projenize bağımlılık eklerken lisans dosyalarını otomatik incelemek için şu komut kullanılabilir:

```bash
npm install --save license-checker
npx license-checker --summary
```

Bu komut, Node.js projenizdeki bağımlılıkların lisans özetini çıkarır; ancak hukuki değerlendirme yerine geçmez.

Son karar projenizin hedefiyle ilgilidir: Maksimum yayılım için MIT, türetilmiş kodun da özgür kalması için GPL, kurumsal kullanım ve patent netliği için Apache 2.0 seçilebilir. Lisans seçimi bir dipnot değil, projenizin gelecekteki işbirliği modelidir.
