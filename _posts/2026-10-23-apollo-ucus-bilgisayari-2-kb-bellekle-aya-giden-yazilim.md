---
layout: post
title: "Apollo Uçuş Bilgisayarı: 2 KB Bellekle Ay’a Giden Yazılım"
math: true
categories: 
  - Bilgi
tags: 
  - apollo
  - nasa
  - gömülü sistemler
  - yazılım mimarisi
  - agc
  - bilgisayar tarihi
toc: true
image: /img/apollo-ucus-bilgisayari-20.png
---

Bugün birkaç tarayıcı sekmesi yüzünden gigabaytlarca bellek tüketebilirken NASA, insanları Ay’a yaklaşık 2 KB yazılabilir belleğe sahip Apollo Guidance Computer (AGC) ile indirdi. Üstelik bu bilgisayar yalnızca rota hesaplamıyor; sensörleri okuyor, motorları yönetiyor ve astronotlarla iletişim kuruyordu. Kısacası AGC, donanım kısıtlarının yaratıcı yazılım mimarisine nasıl dönüştürülebileceğini gösteren tarihî bir gömülü sistem şaheseridir.


![apollo-ucus-bilgisayari-20](/img/apollo-ucus-bilgisayari-20.svg)

``

## Küçük ama görev kritik bir bilgisayar

MIT Instrumentation Laboratory tarafından geliştirilen AGC, Komuta Modülü ve Ay Modülü’nde kullanıldı. Yaklaşık 2,048 MHz saat frekansına sahipti; ancak bu değer modern işlemcilerle doğrudan karşılaştırılmamalıdır. Temel bellek birimi 15 veri biti ve bir eşlik bitinden oluşan 16 bitlik sözcüktü.

Bellek iki ana bölüme ayrılıyordu:

| Bellek türü | Yaklaşık kapasite | Kullanım amacı |
|---|---:|---|
| Erasable memory | 2.048 sözcük | Değişkenler, çalışma verileri ve yığın benzeri alanlar |
| Fixed rope memory | 36.864 sözcük | Kalıcı program kodu ve sabitler |

Modern ölçüyle yazılabilir kapasite yaklaşık olarak şöyle düşünülebilir:

$$M = 2048 \times 15 \text{ bit} \approx 3.75 \text{ KiB}$$

Fakat eşlik bitleri, adresleme düzeni ve kullanılabilir alanlar dikkate alındığında pratik çalışma alanı oldukça sınırlıydı. Sıkça söylenen “2 KB” ifadesi de bu kısıtlı erasable memory yapısını özetler.

## Core rope: Yazılımı gerçekten dokumak

AGC’nin kalıcı programı, core rope memory adı verilen özel bir bellekte saklanıyordu. Teller manyetik çekirdeklerin içinden geçirilirse bir, dışından geçirilirse sıfır temsil ediliyordu. Bu nedenle yazılım üretiminin son aşaması fiziksel dokuma sürecine benziyordu.

| Modern geliştirme | Apollo dönemi |
|---|---|
| Güncelleme birkaç saniyede yüklenebilir | Program değişikliği belleğin yeniden üretilmesini gerektirir |
| Hata düzeltmesi uzaktan dağıtılabilir | Hatalar fırlatmadan önce bulunmalıdır |
| Depolama görece ucuzdur | Her sözcük dikkatle planlanır |

Bu yöntem zahmetliydi ama belleği güç kesintilerine ve uzay koşullarına karşı dayanıklı kılıyordu. Yazılım ekibi, gereksiz her komutu gerçek bir maliyet olarak görüyordu.

## Executive: Erken dönem gerçek zamanlı işletim sistemi

AGC yazılımının kalbinde **Executive** bulunuyordu. Executive, görevleri önceliklerine göre çalıştıran kooperatif ve kesme destekli bir zamanlama mekanizmasıydı. Kritik bir görev geldiğinde daha düşük öncelikli işler ertelenebiliyordu. Böylece bilgisayar, aynı anda yapılacak çok iş varken “önce hangisi hayati?” sorusunu cevaplıyordu.

Basitleştirilmiş mantık şu sözde kodla gösterilebilir:

```text
while görev_var:
    görev = en_yüksek_öncelikli_görevi_seç()

    if yeterli_kaynak_var(görev):
        görevi_çalıştır(görev)
    else:
        düşük_öncelikli_işleri_bırak()
        alarm_göster()
```

Bu kod, gerçek AGC kaynak kodu değildir; Executive’in kaynak yetersizliğinde önemli işleri koruma yaklaşımını anlatır. Ayrıca **Interpreter** adlı sanal makine benzeri katman, navigasyon hesaplarında kullanılan karmaşık vektör ve matris işlemlerini daha yoğun biçimde ifade ediyordu. Yani ekip, sınırlı komut kümesinin üzerine göreve özel bir soyutlama katmanı kurmuştu.

## 1201 ve 1202 alarmları neden başarı hikâyesidir?

Apollo 11’in inişi sırasında buluşma radarından gelen beklenmedik işler işlemci yükünü artırdı. AGC, 1201 ve 1202 program alarmlarını üretti. Bu alarmlar bilgisayarın tamamen çöktüğünü değil, Executive’in bütün işleri zamanında tamamlayamadığını bildiriyordu.

Yeniden başlatma koruması sayesinde sistem, düşük öncelikli görevleri bıraktı; uçuş kontrolü ve yönlendirme gibi kritik görevleri sürdürdü. Yaklaşım kabaca şu ilkeye dayanıyordu:

$$kritik\ görevler > yardımcı\ görevler$$

Bu, günümüzde gerçek zamanlı işletim sistemlerinde kullanılan önceliklendirme, hata yalıtımı ve kontrollü bozulma fikirlerinin erken ve etkileyici bir örneğidir.

## DSKY ve kalıcı dersler

Astronotlar bilgisayarla **DSKY** adlı ekran-klavye birimi üzerinden, “verb” ve “noun” kodlarıyla iletişim kuruyordu. Örneğin fiil yapılacak işlemi, isim ise işlenecek veriyi belirtiyordu. Kullanımı alışılmadıktı ama az tuşla çok sayıda komut sunuyordu.

AGC bize iyi gömülü yazılımın yüksek donanım gücünden önce doğru öncelikler, öngörülebilir zamanlama ve güvenli hata davranışı gerektirdiğini öğretir. Ay’a inişi mümkün kılan şey sınırsız kaynaklar değil; her bitin, görevin ve hatanın titizlikle düşünülmesiydi.
