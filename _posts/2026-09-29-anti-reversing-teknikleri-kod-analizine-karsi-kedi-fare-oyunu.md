---
layout: post
title: "Anti-Reversing Teknikleri: Kod Analizine Karşı Kedi-Fare Oyunu"
math: true
categories: 
  - Bilgi
tags: 
  - tersine mühendislik
  - anti-debug
  - sanal makine
  - zararlı yazılım analizi
  - yazılım güvenliği
  - obfuscation
toc: true
image: /img/anti-reversing-teknikleri-85.png
---

Bir programın debugger veya sanal makine içinde çalıştığını anlamaya uğraşması, dijital dünyadaki “Beni gerçekten kim izliyor?” sorusudur. Bu yöntemler lisans korumasından oyun güvenliğine kadar meşru amaçlarla kullanılabilse de kötü amaçlı yazılımlar tarafından analizi geciktirmek için de tercih edilir. Bu yazıda teknikleri uygulanabilir kaçış tariflerine dönüştürmeden, çalışma mantıkları ve savunmacıların bunları nasıl yorumladığı üzerinde duracağız.
``

## Anti-reversing nedir?

Anti-reversing, bir yazılımın statik veya dinamik analizini zorlaştıran yöntemlerin genel adıdır. Amaç çoğu zaman analizi tamamen engellemek değil, maliyetini yükseltmektir. Çünkü işlemci tarafından çalıştırılabilen kod, yeterli zaman ve yetki verildiğinde gözlemlenebilir.

Bu ilişki basitçe şöyle modellenebilir:

$$
K_{analiz} = T \times U \times B
$$

Burada $T$ harcanan zamanı, $U$ gereken uzmanlığı, $B$ ise kullanılan araçların maliyetini temsil eder. Anti-reversing teknikleri bu değişkenlerden en az birini artırmaya çalışır.

| Teknik ailesi | Aranan belirti | Tipik tepki | Temel zayıflık |
|---|---|---|---|
| Anti-debug | Kesme noktası, araç veya zamanlama anomalisi | Kapanma ya da sahte davranış | Belirtiler taklit edilebilir |
| Anti-VM | Sanal donanım ve kaynak izleri | İşlevi geciktirme veya gizleme | Gerçek sistemlerde yanlış alarm üretir |
| Obfuscation | Okunabilir kontrol akışını bozma | Analisti yavaşlatma | Çalışma anında anlam açığa çıkar |
| Bütünlük kontrolü | Kod veya bellek değişikliği | Hata verme ya da farklı dala geçme | Kontrolün kendisi değiştirilebilir |

## Debugger nasıl sezilir?

Debugger, programı durdurur, adım adım ilerletir ve belleği inceler. Yazılım bu müdahaleyi doğrudan görmek yerine çoğunlukla yan etkilerini arar.

**Zamanlama kontrolleri**, iki işlem arasındaki sürenin olağandışı uzayıp uzamadığını ölçer. Normal süre $t_n$, gözlenen süre $t_o$ ise basit bir şüphe oranı şöyle düşünülebilir:

$$
R_t = \frac{t_o}{t_n}
$$

$R_t$ büyüdüğünde adım adım yürütme ihtimali artar; ancak yoğun sistem yükü de aynı sonucu doğurabilir. Diğer yaklaşımlar süreç adlarını, hata ayıklama bayraklarını, istisnaların nasıl işlendiğini veya kod bütünlüğünü gözlemler. Tek bir sinyal güvenilir olmadığından uygulamalar genellikle birkaç zayıf işareti birleştirir.

## Sanal makine tespiti

Analistler şüpheli programları ana sistemden ayırmak için VM ve sandbox kullanır. Buna karşı yazılım; işlemci özellikleri, sanal aygıt adları, ağ kartı üretici izleri, düşük RAM, az çekirdek, kısa sistem çalışma süresi veya kullanıcı etkinliği eksikliği gibi belirtileri değerlendirebilir.

Bu yaklaşım kusursuz değildir. Bulut sunucuları da sanallaştırılmıştır; düşük donanımlı gerçek cihazlar ise sandbox gibi görünebilir. Dolayısıyla katı bir “VM bulundu” kararı yerine risk puanı daha anlamlıdır:

```python
def ortam_riski(sinyaller):
    # Soyut sinyalleri ağırlıklandırır; gerçek sistem API'lerine erişmez.
    agirliklar = {
        'dusuk_bellek': 0.20,
        'az_cekirdek': 0.15,
        'sanal_aygit_izi': 0.40,
        'kullanici_etkinligi_yok': 0.25,
    }
    return sum(agirliklar.get(s, 0) for s in sinyaller)

puan = ortam_riski(['dusuk_bellek', 'sanal_aygit_izi'])
print(f'İnceleme puanı: {puan:.2f}')
```

Bu örnek yalnızca sınıflandırma mantığını gösterir. Üretim ortamında böyle bir puanın güvenlik kararı için tek başına kullanılması ciddi yanlış pozitiflere yol açabilir.

## Analistler nasıl karşılık verir?

Savunmacılar farklı donanım profilleri kullanır, zaman ölçümlerini karşılaştırır, ağ ve dosya davranışlarını kaydeder ve aynı örneği hem fiziksel hem sanal ortamlarda çalıştırır. Statik analiz davranışın olası yollarını gösterirken dinamik analiz gerçekten yürütülen yolu ortaya çıkarır. Bellek görüntüleri ise çalışma anında açılan kod ve verileri yakalayabilir.

En önemli ders şudur: Anti-reversing görünmezlik pelerini değil, hız tümseğidir. Meşru geliştiriciler gizli anahtarları istemci koduna gömmemeli; kritik doğrulamaları sunucu tarafına taşımalı, kod imzalama ve bütünlük denetimlerini katmanlı güvenlikle desteklemelidir. Araştırmacılar da bu teknikleri yalnızca izinli laboratuvarlarda incelemeli ve bulguları savunmayı güçlendirecek biçimde paylaşmalıdır.

![anti-reversing-teknikleri-85](/img/anti-reversing-teknikleri-85.svg)

