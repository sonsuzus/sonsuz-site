---
layout: post
title: "Kısayol Ustası mı, Zihinsel Akrobat mı? Geliştirici Ergonomisinin Görünmeyen Bedeli"
math: true
categories: 
  - Bilgi
tags: 
  - geliştirici ergonomisi
  - bilişsel yük
  - klavye kısayolları
  - vim
  - kod editörleri
  - bilek sağlığı
toc: true
image: /img/kisayol-ustasi-mi-39.png
---

Bir geliştiricinin editörü bazen kokpite benzer: yüzlerce komut, tuhaf tuş dizileri ve yanlışlıkla basıldığında dosyayı başka boyuta gönderen kısayollar… Peki fareye uzanmadan kod yazmak gerçekten üretkenlik zirvesi mi, yoksa beynimizi ve bileklerimizi sessizce yoran bir optimizasyon oyunu mu? Cevap, kaç kısayol bildiğimizden çok onları nasıl öğrendiğimizde ve kullandığımızda saklıdır.


![kisayol-ustasi-mi-39](/img/kisayol-ustasi-mi-39.svg)

``

## Bilişsel yük nereden geliyor?

Çalışma belleğimiz sınırlıdır. Bir problemi çözerken değişkenleri, veri akışını ve olası hataları zihnimizde tutarız. Buna bir de “Bu işlemin kısayolu `Ctrl+Shift+P` miydi, yoksa `Ctrl+Alt+P` mi?” sorusu eklendiğinde araç kullanımı, problem çözmeyle aynı zihinsel bütçeden harcama yapar.

Basitleştirilmiş bir modelle toplam yükü şöyle düşünebiliriz:

$$L_{toplam} = L_{problem} + L_{araç} + L_{geçiş}$$

Burada $L_{problem}$ yazılım probleminin zorluğunu, $L_{araç}$ editör komutlarını hatırlama maliyetini, $L_{geçiş}$ ise klavye, fare, terminal ve dokümantasyon arasındaki bağlam değişimlerini temsil eder. İyi öğrenilmiş bir kısayol zamanla otomatikleşerek $L_{araç}$ değerini azaltır. Ancak aynı anda elli komut öğrenmeye çalışmak tam tersini yapar.

| Yaklaşım | Zihinsel başlangıç maliyeti | Uzun vadeli hız | Fiziksel risk noktası |
|---|---:|---:|---|
| Fare ağırlıklı kullanım | Düşük | Orta | Omuz ve tekrarlı uzanma |
| Klasik editör kısayolları | Orta | Yüksek | Modifier tuşlarını zorlama |
| Vim modal komutları | Yüksek | Çok yüksek olabilir | Tekrarlı parmak hareketleri |
| Dengeli hibrit kullanım | Orta | Yüksek | Kişiye göre dağıtılabilir |

## Vim neden hem rahatlatır hem yorabilir?

Vim’in modal yapısı, komutları küçük bir dil gibi birleştirir. Örneğin `d2w`, kabaca “iki kelimeyi sil” anlamına gelir. Bu yapı ezber listesinden ziyade bir gramer sunar:

$$Komut = Operatör + Sayı + Hareket$$

Bu nedenle yeterli pratikten sonra kullanıcı yüzlerce ayrı kısayol ezberlemeden yeni eylemler türetebilir. Kazanç yalnızca hız değildir; niyeti doğrudan komuta çevirmek akışı koruyabilir. Fakat öğrenme döneminde sürekli komut düşünmek, kodun kendisine ayrılan dikkati azaltır. Ayrıca “fare kullanmamak” bir başarı rozeti değildir. Grafik arayüz, görsel seçim veya nadiren yapılan işlemlerde fare daha düşük maliyetli olabilir.

## Bilek sağlığı: Az hareket her zaman iyi değildir

Fareye daha az uzanmak omuz hareketlerini azaltabilir; buna karşılık `Ctrl`, `Shift` ve `Alt` kombinasyonlarını sürekli zorlamak bilek ve küçük parmak yükünü artırabilir. Sorun çoğu zaman kullanılan cihazdan çok hareketin sıklığı, kuvveti, açısı ve molasız tekrarıdır.

Kısayollarınızı kişiselleştirirken kullanım sıklığını ölçebilirsiniz. Aşağıdaki örnek, basit bir komut sayacının mantığını gösterir:

```python
from collections import Counter

commands = ["rename", "search", "search", "format", "search", "rename"]
frequency = Counter(commands)

for command, count in frequency.most_common():
    print(f"{command}: {count}")
```

Bu yaklaşım gerçek editör telemetrisi veya kişisel notlarla genişletilebilir. En sık kullanılan birkaç eylemi rahat tuşlara taşımak, yüzlerce kısayolu baştan düzenlemekten daha verimlidir.

## Sürdürülebilir bir kısayol stratejisi

Önce günde defalarca yaptığınız 5–10 işlemi seçin. Her hafta yalnızca bir veya iki yeni kombinasyon ekleyin; kullanılmayanları bırakın. Tuş atamalarında bileği yana bükmeyi ve aynı parmağı aşırı germeyi gerektiren dizilerden kaçının. Gerekirse sticky keys, katmanlı klavyeler, makrolar veya alternatif modifier düzenleri deneyin.

En önemlisi, düzenli mikro molalar verin, oturuşunuzu değiştirin ve ağrıyı “alışma süreci” diye normalleştirmeyin. Kalıcı uyuşma ya da ağrı varsa bir sağlık uzmanına danışmak gerekir. Gerçek geliştirici ergonomisi, fareyi düşman ilan etmek değil; zihni akışta, bedeni ise uzun yıllar oyunda tutacak kadar esnek bir sistem kurmaktır.
