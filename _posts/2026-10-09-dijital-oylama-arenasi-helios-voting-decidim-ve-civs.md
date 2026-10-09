---
layout: post
title: "Dijital Oylama Arenası: Helios Voting, Decidim ve CIVS"
math: true
categories: 
  - Bilgi
tags: 
  - oylama
  - helios-voting
  - decidim
  - civs
  - e-demokrasi
  - açık-kaynak
toc: true
image: /img/dijital-oylama-arenasi-92.png
---

Bir dijital oylama sistemi seçmek, yalnızca “en çok oy alan kazansın” kodu yazmaktan ibaret değildir. Gizlilik, doğrulanabilirlik, kimlik denetimi ve seçim yöntemleri işin içine girdiğinde küçük bir anket hızla kriptografi laboratuvarına dönüşebilir. Bu yazıda Helios Voting, Decidim ve CIVS’nin farklı yaklaşımlarını karşılaştıracağız.

``

## Oylamanın teorik temeli

Basit çoğunluk oylamasında aday $i$ için kullanılan oy sayısını $v_i$ ile gösterirsek kazanan şöyle bulunur:

$$kazanan = argmax_i(v_i)$$

Ancak gerçek dünyadaki her karar “tek aday seç” biçiminde değildir. Seçmenler adayları sıralayabilir, birden fazla seçeneği destekleyebilir veya bütçe önerilerine oy verebilir. Ayrıca sistemin dört temel beklentiyi dengelemesi gerekir:

- **Gizlilik:** Bir oyun kime ait olduğu açıklanmamalıdır.
- **Bütünlük:** Oylar değiştirilememeli veya silinememelidir.
- **Doğrulanabilirlik:** Seçmen, oyunun sayıma katıldığını kontrol edebilmelidir.
- **Uygunluk:** Yalnızca yetkili kişiler ve izin verilen sayıda oy kullanabilmelidir.

Bu özellikler bazen çatışır. Kimlik doğrulamasını güçlendirmek gizlilik riskini artırabilir; tamamen anonim katılım ise mükerrer oyları engellemeyi zorlaştırabilir.

## Üç platform, üç farklı karakter

| Platform | Temel yaklaşım | Güçlü olduğu alan | Dikkat edilmesi gereken nokta |
|---|---|---|---|
| **Helios Voting** | Uçtan uca doğrulanabilir kriptografik seçim | Üniversite, dernek ve kurul seçimleri | Zorlayıcıya karşı dayanıklılık ve cihaz güvenliği ayrıca değerlendirilmelidir |
| **Decidim** | Katılımcı demokrasi platformu | Öneriler, toplantılar, süreçler ve katılımcı bütçeleme | Tek başına özel amaçlı kriptografik seçim motoru değildir |
| **CIVS** | Condorcet tabanlı sıralamalı oylama | Alternatifleri tercih sırasına koyma | Sonuç yöntemi kullanıcıya önceden açıklanmalıdır |

## Helios Voting: Matematik sandık başında

Helios, oyları açık anahtarlı şifreleme ile korur ve seçim sonucunun doğrulanabilmesi için kriptografik kanıtlar üretir. Homomorfik şifrelemenin sadeleştirilmiş fikri şudur:

$$E(v_1) \otimes E(v_2) = E(v_1 + v_2)$$

Yani sistem, tek tek oyların içeriğini açmadan şifreli oyları birleştirip toplamı elde edebilir. Seçmen genellikle oyuna karşılık gelen bir takip değeri alır ve bu değerin yayımlanan sandık kayıtlarında bulunup bulunmadığını denetler. Böylece “oyum kayboldu mu?” sorusu teknik olarak kontrol edilebilir.

Bununla birlikte uçtan uca doğrulanabilirlik, seçmenin cihazında zararlı yazılım bulunmadığını otomatik olarak garanti etmez. Resmî ve yüksek riskli seçimlerde bağımsız güvenlik incelemesi şarttır.

## Decidim: Oylamadan daha büyük bir sahne

Ruby on Rails tabanlı açık kaynak Decidim, yalnızca sandık kurmaz; karar alma sürecini baştan sona modellemeye çalışır. Katılımcılar öneri oluşturabilir, tartışabilir, toplantılara katılabilir ve bütçe projelerini destekleyebilir.

Bu nedenle Decidim’i “seçim uygulaması” yerine **katılım altyapısı** olarak düşünmek daha doğrudur. Bir belediyenin park önerilerini toplaması, projeleri tartışmaya açması ve ardından bütçe oylaması yapması için uygundur. Süreç şeffaflığı güçlüdür; fakat gizli oy gerektiren kritik seçimlerde kullanılacak özel bileşenler ayrıca incelenmelidir.

## CIVS: Tercih sıralarının gücü

CIVS, seçmenlerin adayları sıralamasına dayanır. Condorcet yaklaşımında bir aday, diğer her adayı ikili karşılaştırmada yeniyorsa kazanan kabul edilir. $P(a,b)$, $a$ adayını $b$ adayına tercih edenlerin sayısı olsun:

$$a \succ b \quad eğer \quad P(a,b) > P(b,a)$$

Bu yöntem, yalnızca birinci tercihleri saymak yerine seçmenlerin genel eğilimini yakalar. Ancak döngüler oluşabilir: A, B’yi; B, C’yi; C de A’yı yenebilir. CIVS bu durumları çözmek için belirli Condorcet tamamlayıcı yöntemlerinden yararlanır.

Aşağıdaki Python kodu, iki aday arasındaki basit ikili üstünlüğü hesaplar:

```python
def pairwise_winner(rankings, a, b):
    scores = {a: 0, b: 0}

    for ranking in rankings:
        if ranking.index(a) < ranking.index(b):
            scores[a] += 1
        else:
            scores[b] += 1

    if scores[a] == scores[b]:
        return 'berabere'
    return max(scores, key=scores.get)
```

Fonksiyon, her sıralamada hangi adayın daha yukarıda bulunduğunu kontrol eder. Gerçek bir Condorcet sistemi, bu işlemi bütün aday çiftleri için yaparak bir karşılaştırma matrisi oluşturur.

## Hangisini seçmeli?

Kriptografik doğrulanabilirlik önceliğinizse **Helios**, kapsamlı katılımcı süreçler tasarlıyorsanız **Decidim**, seçenekleri adil biçimde sıralamak istiyorsanız **CIVS** güçlü adaylardır. Son karar; tehdit modeline, seçmen kitlesine, kimlik doğrulama ihtiyacına ve kullanılan seçim yönteminin anlaşılabilirliğine dayanmalıdır. Unutmayın: İyi bir dijital sandık yalnızca doğru sonucu üretmez, sonucun neden güvenilir olduğunu da gösterebilir.

![dijital-oylama-arenasi-92](/img/dijital-oylama-arenasi-92.svg)

