---
layout: post
title: "Lig ve Puan Tablosu Sistemi Tasarlamak: Fikstürden Şampiyonluğa"
math: true
categories: 
  - Proje
tags: 
  - typescript
  - nodejs
  - veritabanı
  - algoritma
  - turnuva
  - puan-tablosu
toc: true
image: /img/lig-ve-puan-58.png
---

Bir lig yönetim sistemi dışarıdan yalnızca takımları sıralayan basit bir tablo gibi görünür. Oysa Open Tournament veya Tournament Software benzeri bir uygulama; fikstür oluşturma, sonuç kaydetme, eşitlik bozma, hükmen galibiyet ve farklı turnuva formatlarını yönetme gibi birçok kuralı aynı potada eritir. Gelin bu dijital hakemin nasıl tasarlanabileceğine bakalım.

![lig-ve-puan-58](/img/lig-ve-puan-58.svg)

``
## Temel veri modeli

Sistemin merkezinde **turnuva**, **katılımcı**, **karşılaşma** ve **puan durumu kaydı** bulunur. Katılımcı bir takım olabileceği gibi tekil bir sporcu da olabilir. Bu nedenle veri modelinde `team` yerine daha genel olan `participant` adını kullanmak sistemi farklı spor dallarına uyarlamayı kolaylaştırır.

| Varlık | Önemli alanlar | Sorumluluk |
|---|---|---|
| Tournament | ad, format, kurallar | Organizasyon ayarlarını saklar |
| Participant | ad, kategori, seri başı | Takım veya oyuncuyu temsil eder |
| Match | taraflar, skor, durum | Karşılaşma sonucunu tutar |
| Standing | puan, averaj, sıralama | Hesaplanan tabloyu temsil eder |

Puan tablosunu kalıcı olarak saklamak yerine maç sonuçlarından yeniden hesaplamak çoğu zaman daha güvenlidir. Böylece bir skor düzeltildiğinde eski ve yeni değerlerin birbirine karışması önlenir. Performans gerekiyorsa hesaplanan tablo önbelleğe alınabilir.

## Puan hesabının matematiği

Klasik futbol sisteminde galibiyet 3, beraberlik 1 ve mağlubiyet 0 puandır. Bir katılımcının toplam puanı şu şekilde ifade edilir:

$$P = 3G + 1B + 0M$$

Burada $G$ galibiyet, $B$ beraberlik, $M$ ise mağlubiyet sayısıdır. Genel averaj da

$$A = S_{atılan} - S_{yenilen}$$

formülüyle hesaplanır. Ancak masa tenisi, badminton veya e-spor ligleri set oranı, harita farkı ya da doğrudan ikili averaj kullanabilir. Bu yüzden puan kurallarını kodun içine sabitlemek yerine turnuva ayarlarında tanımlamak iyi bir fikirdir.

| Kriter | Avantajı | Dezavantajı |
|---|---|---|
| Genel averaj | Kolay hesaplanır | Güçsüz rakiplere karşı farkı ödüllendirir |
| İkili averaj | Doğrudan rekabeti önemser | Çoklu eşitlikte karmaşıklaşır |
| Kazanılan maç | Sonuç odaklıdır | Beraberlik ağırlığını azaltır |
| Fair-play puanı | Disiplini teşvik eder | Ana performansa dolaylı bağlıdır |

## Hesaplama motoru

Aşağıdaki TypeScript fonksiyonu, tamamlanmış maçlardan temel puan tablosu üretir. Fonksiyon saf tutulduğu için aynı girdi her zaman aynı çıktıyı verir; test etmek de oldukça kolaydır.

```typescript
type Match = {
  homeId: string;
  awayId: string;
  homeScore: number;
  awayScore: number;
  status: "finished" | "scheduled";
};

type Row = {
  id: string;
  played: number;
  won: number;
  draw: number;
  lost: number;
  scored: number;
  conceded: number;
  points: number;
};

function calculateTable(ids: string[], matches: Match[]): Row[] {
  const rows = new Map(ids.map(id => [id, {
    id, played: 0, won: 0, draw: 0, lost: 0,
    scored: 0, conceded: 0, points: 0
  }]));

  for (const match of matches.filter(m => m.status === "finished")) {
    const home = rows.get(match.homeId)!;
    const away = rows.get(match.awayId)!;

    home.played++; away.played++;
    home.scored += match.homeScore;
    home.conceded += match.awayScore;
    away.scored += match.awayScore;
    away.conceded += match.homeScore;

    if (match.homeScore === match.awayScore) {
      home.draw++; away.draw++;
      home.points++; away.points++;
    } else {
      const winner = match.homeScore > match.awayScore ? home : away;
      const loser = winner === home ? away : home;
      winner.won++; winner.points += 3;
      loser.lost++;
    }
  }

  return [...rows.values()].sort((a, b) =>
    b.points - a.points ||
    (b.scored - b.conceded) - (a.scored - a.conceded) ||
    b.scored - a.scored
  );
}
```

Sıralama zinciri burada puan, averaj ve atılan skor biçimindedir. İkili averaj gerekiyorsa eşit puanlı katılımcılar belirlenmeli, yalnızca kendi aralarındaki maçlardan geçici bir mini tablo oluşturulmalıdır.

## Fikstür ve operasyonel ayrıntılar

Tek devreli ligde $n$ katılımcı için toplam maç sayısı

$$M = \frac{n(n-1)}{2}$$

olur. Çift devreli ligde bu değer ikiyle çarpılır. Round-robin fikstür için kullanılan **çember yöntemi**, katılımcıları her tur döndürerek herkesin birbiriyle karşılaşmasını sağlar. Katılımcı sayısı tekse hayali bir `BYE` eklenir ve onunla eşleşen taraf haftayı maç yapmadan geçirir.

Gerçek dünyada maç erteleme, hükmen sonuç, katılımcı çekilmesi ve yönetici düzeltmeleri unutulmamalıdır. Her skor değişikliğini kullanıcı, zaman ve eski değer bilgisiyle bir denetim günlüğüne kaydetmek tartışmaları azaltır. Sonuç girişini yetkilendirme, eşzamanlı güncellemelerde transaction kullanma ve hesaplama motorunu bolca birim testiyle sınama da sistemin görünmeyen savunma hattıdır. Böylece puan tablosu yalnızca şık değil, son düdüğe kadar güvenilir olur.
