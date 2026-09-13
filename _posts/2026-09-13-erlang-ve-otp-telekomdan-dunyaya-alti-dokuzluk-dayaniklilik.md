---
layout: post
title: "Erlang ve OTP: Telekomdan Dünyaya Altı Dokuzluk Dayanıklılık"
math: true
categories: 
  - Bilgi
tags: 
  - erlang
  - otp
  - dağıtık sistemler
toc: true
---

Bir yazılım sisteminin yıllarca çalışması kulağa bilim kurgu gibi gelebilir. Erlang dünyasında ise sunucuyu yeniden başlatmadan kod güncellemek, çöken süreçleri otomatik olarak ayağa kaldırmak ve milyonlarca eşzamanlı bağlantıyı yönetmek tasarımın doğal parçalarıdır. Ericsson laboratuvarlarında telekom sistemleri için doğan Erlang, bugün mesajlaşmadan fintek altyapılarına kadar uzanan yolculuğunda hâlâ yüksek erişilebilirliğin en güçlü araçlarından biridir.
``

## Altı dokuz gerçekte ne demek?

Erişilebilirlik, sistemin çalışır durumda olduğu sürenin toplam süreye oranıdır:

$$
A = \frac{T_{çalışma}}{T_{toplam}} \times 100
$$

%99,9999 erişilebilirlik, yani “altı dokuz”, yılda yaklaşık 31,5 saniyelik kesinti bütçesi anlamına gelir. Kahveniz soğumadan bütün yıllık hata hakkını tüketebilirsiniz!

| Erişilebilirlik | Yıllık yaklaşık kesinti | Pratik anlamı |
|---|---:|---|
| %99 | 3,65 gün | Basit iç sistemler |
| %99,9 | 8 saat 46 dakika | Ortalama web hizmetleri |
| %99,99 | 52 dakika | Kritik ticari sistemler |
| %99,9999 | 31,5 saniye | Telekom sınıfı altyapı |

Erlang tek başına altı dokuz garantisi vermez. Ancak hata izolasyonu, dağıtık çalışma ve otomatik iyileşme için sunduğu yapı taşları bu hedefi ulaşılabilir kılar.

## Erlang’ın sırrı: küçük ve izole süreçler

Erlang süreçleri işletim sistemi süreçleri değildir. Çok hafiftirler, belleklerini paylaşmazlar ve birbirlerine mesaj göndererek haberleşirler. Bu yaklaşım, paylaşılan bellekteki kilit yarışlarını büyük ölçüde ortadan kaldırır.

```erlang
-module(counter).
-export([start/0, loop/1]).

start() ->
    spawn(fun() -> loop(0) end).

loop(Value) ->
    receive
        {increment, From} ->
            NewValue = Value + 1,
            From ! {value, NewValue},
            loop(NewValue);
        stop ->
            ok
    end.
```

Bu örnek, kendi durumunu taşıyan hafif bir sayaç süreci oluşturur. `receive` posta kutusundaki mesajları işler; `spawn` ise yeni süreci başlatır. Bir süreç bozulduğunda diğerlerinin belleği kirlenmez. Böylece hata, bütün uygulamayı devirmek yerine küçük bir bölmede tutulur.

## OTP, tek kullanımlık parola değildir

Buradaki OTP, **Open Telecom Platform** anlamına gelir. Erlang üzerinde güvenilir uygulamalar geliştirmek için davranış kalıpları, süreç yöneticileri ve standart kütüphaneler sunar.

| OTP bileşeni | Görevi |
|---|---|
| `gen_server` | Durum tutan sunucu süreçleri oluşturur |
| `supervisor` | Çöken çocuk süreçleri yeniden başlatır |
| `application` | Bileşenlerin başlatılmasını ve durdurulmasını yönetir |
| `release` | Sürüm paketleme ve yükseltme sağlar |

Bir supervisor tanımı oldukça sade olabilir:

{% raw %}
```erlang
init([]) ->
    Child = #{id => worker,
              start => {worker, start_link, []},
              restart => permanent,
              type => worker},
    {ok, {{one_for_one, 5, 10}, [Child]}}.
```
{% endraw %}

`one_for_one`, yalnızca çöken çocuğu yeniden başlatır. `5, 10` ayarı ise on saniyede beşten fazla yeniden başlatma olursa supervisor’ın pes etmesini sağlar. Böylece sonsuz hata döngüsü gizlenmez; problem üst seviyedeki denetleyiciye taşınır.

## “Let it crash” neden umursamazlık değildir?

“Bırak çöksün” yaklaşımı, hataları görmezden gelmek demek değildir. Savunmacı kodla her ihtimali yamamak yerine süreçlerin başarısız olabileceği kabul edilir. Kritik durum başka süreçlerde tutulur, hata kayda geçirilir ve supervisor bilinen temiz bir başlangıç durumunu kurar.

Bu modelin teorik gücü hata izolasyonundan gelir. Tek bir bileşenin başarısızlık olasılığı $p$ ise bağımsız yedeklerin birlikte başarısız olma olasılığı yaklaşık $p^n$ olur. Gerçek sistemlerde bağımsızlık kusursuz değildir; aynı veri merkezi, ağ veya hatalı sürüm ortak risk yaratabilir. Bu yüzden Erlang mimarisi izleme, coğrafi dağıtım ve doğru kapasite planlamasıyla tamamlanmalıdır.

Erlang bugün Elixir ekosistemine de temel olan BEAM sanal makinesi sayesinde sohbet, oyun, ödeme ve IoT sistemlerinde yaşamayı sürdürüyor. Sözdizimi herkese tanıdık gelmeyebilir; fakat “hata olacak, önemli olan sistemin iyileşmesi” fikri modern dağıtık sistemlerin tam merkezindedir. Telekomdan kalan asıl miras da budur: hiç hata yapmayan yazılım değil, hata yaptığında hizmet vermeye devam eden yazılım.
