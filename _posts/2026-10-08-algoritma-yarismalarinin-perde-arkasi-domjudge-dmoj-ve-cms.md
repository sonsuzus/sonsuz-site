---
layout: post
title: "Algoritma Yarışmalarının Perde Arkası: DOMjudge, DMOJ ve CMS"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - online-judge
  - domjudge
  - dmoj
  - cms
  - programlama-yarışmaları
toc: true
image: /img/algoritma-yarismalarinin-perde-38.png
---

Bir algoritma yarışmasında çözümünüzü gönderip birkaç saniye sonra “Accepted” sonucunu gördüğünüzde arka planda küçük bir yazılım orkestrası çalışır. Kaynak kod derlenir, izole bir ortamda test edilir, süre ve bellek tüketimi ölçülür, çıktı karşılaştırılır ve puan hesaplanır. DOMjudge, DMOJ ve CMS, bu orkestrayı yöneten en popüler açık kaynak yarışma sistemleri arasındadır.
``

## Online judge nasıl çalışır?

Bir değerlendirme sisteminin temel girdileri kaynak kod, programlama dili ve problem kimliğidir. Sistem önce kodu derler, ardından her test için programı çalıştırır. En basit toplam değerlendirme süresi şöyle düşünülebilir:

$$T_{toplam} = T_{derleme} + \sum_{i=1}^{n} T_{test_i}$$

Programın herhangi bir testte süre sınırını aşması **TLE**, fazla bellek kullanması **MLE**, hatalı çıktı üretmesi ise **WA** sonucuna yol açar. Doğru sonuç yalnızca çıktının doğru olması değildir; programın belirlenen kaynak sınırları içinde çalışması da gerekir.

Gönderilen kod güvenilir kabul edilmez. Sonsuz döngüye girebilir, süreç oluşturmaya çalışabilir veya dosya sistemine erişmek isteyebilir. Bu nedenle judge sunucuları Linux kullanıcıları, cgroups, chroot, container veya benzeri izolasyon mekanizmalarından yararlanır. Kısacası değerlendirme sunucusu, yarışmacının koduna “Seni çalıştırırım ama evin anahtarını vermem” der.

## Üç platformun karşılaştırması

| Özellik | DOMjudge | DMOJ | CMS |
|---|---|---|---|
| Ana kullanım | ICPC tarzı yarışmalar | Eğitim ve çevrim içi arşiv | IOI tarzı olimpiyatlar |
| Puanlama | Genellikle problem bazlı | Esnek, kısmi puan destekli | Alt görev odaklı |
| Teknoloji | PHP, Symfony, MariaDB | Python, Django, C++ judge | Python tabanlı servisler |
| Kurulum | Orta | Orta-zor | Zor |
| Kullanıcı arayüzü | Yarışma odaklı | Topluluk ve arşiv odaklı | Yönetim odaklı |
| Güçlü yanı | Kararlı takım yarışmaları | Dil ve problem çeşitliliği | Gelişmiş olimpiyat değerlendirmesi |

## DOMjudge: ICPC ruhunun temsilcisi

DOMjudge, takım yarışmaları ve klasik ICPC kuralları için oldukça uygundur. Yanlış gönderimler ceza süresine eklenir; problem çözüldüğünde süre hesabı kesinleşir. Basitleştirilmiş ceza modeli şöyledir:

$$P = T_{kabul} + 20 \times W$$

Burada $T_{kabul}$ kabul dakikası, $W$ ise kabulden önceki yanlış gönderim sayısıdır. DOMjudge; yarışma yönetimi, canlı sıralama, hakem işlemleri ve ayrı judgehost makineleriyle ölçeklendirme konusunda güçlüdür. Üniversite kulübünde gerçekçi bir ICPC provası düzenlemek istiyorsanız genellikle ilk adaydır.

## DMOJ: Esnek ve geliştirici dostu

DMOJ, sürekli açık problem arşivleri ve eğitim platformları için öne çıkar. Çok sayıda dili destekler; özel checker, interaktif problem ve kısmi puanlama gibi özellikler sunar. Django tabanlı web uygulaması ile değerlendirme düğümleri birbirinden ayrılabilir.

Bir problemin basit yapılandırması kavramsal olarak şöyle görünebilir:

```yaml
archive: data.zip
time: 2
memory: 256
test_cases:
  - points: 20
    input: sample.in
    output: sample.out
  - points: 80
    batched:
      - input: secret.in
        output: secret.out
```

Bu yapı süreyi, bellek sınırını ve testlerin puan ağırlığını tanımlar. Gerçek sözdizimi sürüme ve problem paketine göre değişebilse de temel fikir aynıdır: değerlendirme davranışı kod yerine yapılandırmayla açıklanır.

## CMS: Olimpiyat seviyesinde kontrol

Contest Management System, özellikle IOI biçimindeki yarışmalara yöneliktir. Alt görevler, geri bildirim düzeyleri, token sistemi ve ayrıntılı puanlama senaryolarında çok başarılıdır. Örneğin çözüm ilk alt görevden 20, ikinci alt görevden 30 puan alabilir; en zor grup başarısız olsa bile toplam puan korunur.

CMS güçlüdür ancak kurulumu ve işletimi diğer seçeneklere göre daha fazla sistem yönetimi bilgisi ister. Servislerin dağıtılması, worker makinelerinin hazırlanması ve yarışma verilerinin doğru modellenmesi dikkat gerektirir.

## Hangisini seçmeli?

Tek günlük ICPC benzeri bir etkinlik için **DOMjudge**, okul veya topluluk tabanlı sürekli bir soru platformu için **DMOJ**, ulusal olimpiyat düzeyinde alt görevli yarışmalar için **CMS** daha doğal seçimdir. Platformdan bağımsız olarak yedekleme, HTTPS, kaynak izolasyonu ve yarışma öncesi yük testi ihmal edilmemelidir. Çünkü en zor algoritma sorusu bile çözülebilir; yarışma ortasında çöken judge sunucusu ise herkese aynı anda sistem tasarımı dersi verir.

![algoritma-yarismalarinin-perde-38](/img/algoritma-yarismalarinin-perde-38.svg)

