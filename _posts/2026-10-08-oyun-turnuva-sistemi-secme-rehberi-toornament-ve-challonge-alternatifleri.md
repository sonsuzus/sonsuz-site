---
layout: post
title: "Oyun Turnuva Sistemi Seçme Rehberi: Toornament ve Challonge Alternatifleri"
math: true
categories: 
  - Program
tags: 
  - turnuva
  - espor
  - challonge
  - toornament
  - oyun geliştirme
  - web uygulaması
toc: true
image: /img/oyun-turnuva-sistemi-47.png
---

Bir oyun turnuvası düzenlemek, oyuncuları bir listeye yazıp “hadi kapışın” demekten biraz daha karmaşıktır. Kayıt yönetimi, eşleşmeler, skor doğrulama, yayın entegrasyonu ve adil sıralama gibi parçalar devreye girdiğinde doğru platformu seçmek kritik hâle gelir. Toornament ve Challonge popüler seçeneklerdir; ancak farklı ölçeklere, bütçelere ve özelleştirme ihtiyaçlarına hitap eden güçlü alternatifler de bulunur.

``

## Önce turnuva formatını anlayalım

Platform seçmeden önce kullanılacak eşleşme modelini belirlemek gerekir. **Tek eleme**, yenilen oyuncunun turnuvadan çıktığı en hızlı formattır. Katılımcı sayısı $n$ ve sayı ikinin kuvvetiyse toplam maç sayısı şöyledir:

$$M = n - 1$$

Örneğin 32 oyunculu tek eleme turnuvasında 31 maç oynanır. **Çift eleme**, oyuncuya ikinci bir şans verir; ancak maç sayısını ve organizasyon süresini artırır. **Round-robin** formatında ise herkes birbiriyle oynar:

$$M = \frac{n(n-1)}{2}$$

Sekiz takımlı bir ligde 28 maç gerekir. Dolayısıyla “en güzel görünen bracket” yerine zaman, sunucu kapasitesi ve oyuncu sayısı birlikte değerlendirilmelidir.

| Format | Avantaj | Dezavantaj | Uygun kullanım |
|---|---|---|---|
| Tek eleme | Hızlı ve anlaşılır | Tek yenilgide elenme | Günlük etkinlikler |
| Çift eleme | Daha adil ikinci şans | Yönetimi daha karmaşık | Rekabetçi kupalar |
| Round-robin | Dengeli karşılaşmalar | Çok sayıda maç | Ligler ve küçük gruplar |
| İsviçre sistemi | Benzer güçleri eşleştirir | Sıralama mantığı karmaşık | Büyük katılımlı etkinlikler |

![oyun-turnuva-sistemi-47](/img/oyun-turnuva-sistemi-47.svg)


## Hazır platform alternatifleri

**Challonge**, hızlı bracket oluşturma ve kolay paylaşım konusunda güçlüdür. Küçük topluluklar, okul kulüpleri ve kısa süreli etkinlikler için düşük öğrenme eşiği sunar.

**Battlefy**, oyuncu iletişimi, kayıt akışları ve rekabetçi etkinlik operasyonlarına odaklanır. Birden fazla yöneticiyle çalışan organizasyonlar açısından değerlendirilebilir.

**start.gg**, özellikle dövüş oyunları ve topluluk etkinliklerinde tanınır. Katılımcı kaydı, etkinlik sayfaları ve farklı oyun kümelerini aynı organizasyon altında toplama konusunda kullanışlıdır.

**Bracket HQ**, sade görsel bracket hazırlamak isteyenler için pratik bir seçenektir. Karmaşık otomasyon yerine hızlı sunum gerektiğinde avantaj sağlar.

| Platform | Güçlü yön | En uygun senaryo | Dikkat edilmesi gereken |
|---|---|---|---|
| Toornament | Gelişmiş organizasyon araçları | Profesyonel etkinlik | Özellik ve paket sınırları |
| Challonge | Kolay kurulum | Küçük-orta turnuvalar | İleri özelleştirme ihtiyacı |
| Battlefy | Operasyon ve iletişim | Topluluk ligleri | İş akışını öğrenme süresi |
| start.gg | Etkinlik ekosistemi | Dövüş oyunları, LAN | Oyuna göre uygunluk |
| Bracket HQ | Basit görselleştirme | Hızlı bracket paylaşımı | Sınırlı otomasyon |

Özellikler ve fiyatlandırmalar zamanla değişebileceği için karar vermeden önce platformların güncel planları mutlaka incelenmelidir.

## Kendi sistemini geliştirmek

Hazır çözümler yetersizse temel veri modeli `Tournament`, `Participant`, `Match` ve `Result` varlıklarından oluşabilir. Aşağıdaki JavaScript fonksiyonu, oyuncuları karıştırarak ilk tur eşleşmelerini üretir:

```javascript
function createFirstRound(players) {
  const shuffled = [...players].sort(() => Math.random() - 0.5);
  const matches = [];

  for (let i = 0; i < shuffled.length; i += 2) {
    matches.push({
      playerA: shuffled[i],
      playerB: shuffled[i + 1] ?? null,
      winner: shuffled[i + 1] ? null : shuffled[i]
    });
  }

  return matches;
}
```

Kod, tek sayıda oyuncu olduğunda son katılımcıya otomatik geçiş anlamına gelen bir **bye** verir. Gerçek projede `Math.random()` yerine test edilebilir bir rastgelelik yöntemi kullanılmalı; ayrıca seri başı oyuncuların ilk turda karşılaşmasını engelleyen seeding kuralları eklenmelidir.

## Seçim kontrol listesi

Karar verirken katılımcı kapasitesi, mobil kullanım, API veya webhook desteği, skor itiraz süreci, Discord entegrasyonu, yayın ekranları ve kişisel verilerin saklanma biçimi incelenmelidir. Küçük bir hafta sonu kupası için Challonge benzeri sade bir araç yeterliyken, sponsorlu bir espor ligi gelişmiş yetkilendirme ve otomasyon isteyebilir. En iyi sistem, en fazla düğmeye sahip olan değil; organizatörün yükünü azaltıp oyuncuya “Sıradaki rakibim kim?” sorusunun cevabını anında verendir.
