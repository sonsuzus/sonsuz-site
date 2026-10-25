---
layout: post
title: "Oyunlarda Kayıp Aversiyonu: Kaybetme Korkusu Oyuncuyu Nasıl Etkiler?"
math: true
categories: 
  - Bilgi
tags: 
  - oyun tasarımı
  - kayıp aversiyonu
  - oyuncu psikolojisi
  - davranışsal ekonomi
  - game design
toc: true
image: /img/oyunlarda-kayip-aversiyonu-16.png
---

![oyunlarda-kayip-aversiyonu-16](/img/oyunlarda-kayip-aversiyonu-16.svg)


Bir oyunda kazandığınız 100 altın sizi mutlu ederken aynı miktarı kaybetmek neden çok daha ağır hissettirir? Cevap, davranışsal ekonominin en güçlü kavramlarından biri olan **kayıp aversiyonunda** saklıdır. Oyun tasarımcıları bu psikolojik eğilimi görevlerden günlük ödüllere kadar pek çok sistemde kullanır. Ancak oyuncuyu motive etmek ile onu kaybetme korkusuyla baskı altında tutmak arasında dikkatle korunması gereken etik bir sınır vardır.
``

## Kayıp aversiyonu nedir?

Kayıp aversiyonu, insanların kayıplara eşit büyüklükteki kazançlardan daha güçlü tepki vermesidir. Örneğin 50 TL bulmanın yarattığı sevinç, 50 TL kaybetmenin oluşturduğu üzüntüyü genellikle dengelemez. Daniel Kahneman ve Amos Tversky tarafından geliştirilen **Beklenti Teorisi**, kararlarımızın mutlak sonuçlardan çok mevcut referans noktasına göre şekillendiğini söyler.

Bu düşünce basitleştirilmiş bir değer fonksiyonuyla gösterilebilir:

$$
v(x)=
\begin{cases}
x^\alpha, & x \geq 0 \\
-\lambda(-x)^\beta, & x < 0
\end{cases}
$$

Burada $x$ kazanç veya kaybı, $\alpha$ ve $\beta$ duyarlılığı, $\lambda$ ise kayıpların psikolojik ağırlığını temsil eder. Çoğu modelde $\lambda > 1$ kabul edilir. Örneğin $\lambda=2$ olduğunda 100 puanlık kayıp, yaklaşık 200 puanlık psikolojik etki yaratabilir.

| Durum | Oyuncunun algısı | Muhtemel davranış |
|---|---|---|
| Yeni bir ödül kazanmak | Olumlu fırsat | Oynamaya istek duyma |
| Mevcut seriyi kaybetmek | Sahip olunan değerin silinmesi | Bir maç daha oynama |
| Süreli ödülü kaçırmak | Geri gelmeyecek kayıp | Oyuna hızlıca dönme |
| Rütbenin düşmesi | Statü ve ilerleme kaybı | Kaybı telafi etmeye çalışma |

## Oyunlarda nasıl karşımıza çıkar?

**Galibiyet serileri**, kayıp aversiyonunun en görünür örneklerindendir. Oyuncu üç maç kazandığında sadece yeni bir ödüle yaklaşmaz; aynı zamanda oluşturduğu serinin sahibi gibi hissetmeye başlar. Sonraki maça girmesinin nedeni ödül kazanmak kadar seriyi kaybetmemektir.

**Günlük giriş serileri** de benzer çalışır. Yirmi gün boyunca oyuna giren biri, yirmi birinci günün ödülünden çok önceki yirmi günün boşa gitmesinden endişe edebilir. Süreli etkinlikler, sezon biletleri, düşebilen lig puanları ve kaybolabilen kaynaklar da aynı psikolojik düğmeye basar.

| Dengeli tasarım | Baskıcı tasarım |
|---|---|
| Kaçırılan gün için telafi hakkı verir | Tüm seriyi anında sıfırlar |
| Kaybın sonucunu önceden açıklar | Sonucu belirsiz veya gizli tutar |
| Oyuncuya mola seçeneği sunar | Sürekli bildirimlerle aciliyet yaratır |
| Eğlenceyi temel motivasyon yapar | Kaygıyı temel motivasyona dönüştürür |

## Basit bir mekanik örneği

Aşağıdaki JavaScript fonksiyonu, galibiyet serisinin tamamen silinmesi yerine bir miktar korunmasını sağlar. Böylece kayıp hâlâ anlamlıdır fakat oyuncunun emeği bütünüyle yok olmaz:

```javascript
function updateStreak(currentStreak, didWin, shieldCount) {
  if (didWin) {
    return {
      streak: currentStreak + 1,
      shields: shieldCount
    };
  }

  if (shieldCount > 0) {
    return {
      streak: currentStreak,
      shields: shieldCount - 1
    };
  }

  return {
    streak: Math.floor(currentStreak / 2),
    shields: 0
  };
}
```

Buradaki **koruma kalkanı**, kaybı tamamen kaldırmaz; yalnızca sertliğini azaltır. Kalkan yoksa seri yarıya iner. Bu yaklaşım, oyuncuya başarısızlığın bir sonucu olduğunu hissettirirken uzun süreli emeği de korur.

## Etik tasarım neden önemli?

Kayıp aversiyonu tek başına kötü bir mekanik değildir. Gerilim oluşturabilir, kararları anlamlı hâle getirebilir ve oyuncunun başarılarına değer katabilir. Sorun, sistemin eğlence yerine suçluluk, stres veya kaçırma korkusu üretmeye başlamasıdır.

İyi bir tasarımcı şu soruyu sormalıdır: **Oyuncu devam etmek istediği için mi oynuyor, yoksa bırakırsa cezalandırılacağını düşündüğü için mi?** Şeffaf kurallar, makul telafi seçenekleri, bildirim kontrolleri ve mola hakları bu ayrımı belirler. En başarılı oyun döngüsü, oyuncuyu korkuyla ekrana zincirleyen değil; kayıpları öğretici, adil ve geri dönülebilir deneyimlere dönüştüren döngüdür.
