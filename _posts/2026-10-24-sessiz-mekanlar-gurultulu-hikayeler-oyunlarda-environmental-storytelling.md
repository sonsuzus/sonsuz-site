---
layout: post
title: "Sessiz Mekânlar, Gürültülü Hikâyeler: Oyunlarda Environmental Storytelling"
math: true
categories: 
  - Bilgi
tags: 
  - oyun tasarımı
  - environmental storytelling
  - seviye tasarımı
  - anlatı tasarımı
  - görsel hikâye anlatımı
toc: true
image: /img/sessiz-mekanlar-gurultulu-10.png
---

Bir odaya giriyorsunuz: Masada yarım kalmış bir yemek, duvarda çocuk çizimleri ve kapıya doğru uzanan kanlı ayak izleri var. Kimse konuşmuyor, görev günlüğü açılmıyor; fakat zihniniz çoktan olayları birleştirmeye başladı. İşte **environmental storytelling**, yani çevresel hikâye anlatımı, oyuncuya açıklama yapmak yerine mekânı konuşturma sanatıdır.

![sessiz-mekanlar-gurultulu-10](/img/sessiz-mekanlar-gurultulu-10.svg)

``
## Çevresel anlatı nasıl çalışır?

Bu yaklaşım, oyuncunun çevredeki işaretleri okuyarak geçmişte yaşanan olaylar hakkında çıkarım yapmasına dayanır. Tasarımcı hikâyeyi doğrudan aktarmak yerine nesneler, ışık, mimari, ses ve mekânsal düzen üzerinden kanıtlar bırakır. Oyuncu da küçük bir dedektif gibi bu parçaları birleştirir.

Tekniğin teorik temelinde **göstergebilim** bulunur. Her nesne yalnızca fiziksel bir varlık değil, aynı zamanda anlam taşıyan bir göstergedir. Örneğin devrilmiş bir sandalye tek başına önemsiz olabilir. Ancak kırılmış pencere, açık kasa ve yerdeki mermi kovanlarıyla birlikte görüldüğünde çatışma veya kaçış fikrini üretir.

Oyuncunun algıladığı anlatı etkisini basitçe şöyle düşünebiliriz:

$$E = D \times B \times K$$

Burada $E$ anlatısal etkiyi, $D$ detayların okunabilirliğini, $B$ bağlamsal bağlantıyı ve $K$ oyuncunun katılımını temsil eder. Unsurlardan biri sıfıra yaklaşırsa sahnenin etkisi de zayıflar. Çok ayrıntılı fakat bağlamsız bir oda, hikâye anlatmak yerine dağınık bir dekor deposuna dönüşebilir.

## Diyalog ile çevresel anlatının farkı

| Özellik | Diyalogla anlatım | Çevresel anlatım |
|---|---|---|
| Bilgi aktarımı | Doğrudan ve kontrollü | Dolaylı ve yoruma açık |
| Oyuncu rolü | Dinleyici | Araştırmacı |
| Tempo | Konuşmanın süresine bağlı | Keşif hızına bağlı |
| Tekrar oynanabilirlik | Genellikle düşük | Gizli detaylarla yüksek |
| Risk | Fazla açıklama | Belirsizlik veya fark edilmeme |

Bu iki yöntem birbirinin düşmanı değildir. Güçlü oyunlar çoğu zaman diyaloğu ana bilgileri vermek, çevreyi ise duyguyu ve alt metni taşımak için kullanır.

## Mekânı konuşturmanın araçları

**Nesne yerleşimi**, olayların sonucunu gösterir. İki kişilik masada tek tabak bulunması yalnızlığı; kapının önüne yığılmış mobilyalar korkuyu anlatabilir.

**Işık ve renk**, oyuncunun dikkatini yönlendirir. Sıcak ışıklı bir oda güvenli görünürken titreyen soğuk ışık huzursuzluk yaratır. Renk değişimi, farklı grupların hâkimiyet alanlarını da gösterebilir.

**Mimari ve yıpranma**, zamanın izini taşır. Sonradan örülmüş bir duvar, paslı güvenlik kapıları veya üzerine yeni semboller çizilmiş eski bir heykel; mekânın birden fazla döneme tanıklık ettiğini sezdirir.

**Ses tasarımı** da görünmeyen çevrenin parçasıdır. Uzakta çalışan bir makine, üst kattan gelen ayak sesleri ya da aniden kesilen kuş sesleri, oyuncuya kadraj dışında bir dünya bulunduğunu hatırlatır.

## Tasarımı sistemleştirmek

Çevresel ipuçları kod tarafında küçük bir veri modeliyle takip edilebilir:

```csharp
public class StoryClue
{
    public string Id;
    public string RequiredClue;
    public float DiscoveryRadius;
    public bool IsDiscovered;

    public bool CanBeUnderstood(HashSet<string> discoveries)
    {
        return string.IsNullOrEmpty(RequiredClue)
            || discoveries.Contains(RequiredClue);
    }
}
```

Bu sınıf, bir ipucunun keşif mesafesini ve anlaşılması için başka bir ipuca ihtiyaç duyup duymadığını tanımlar. Böylece kanlı anahtar bulunmadan kilitli dolabın anlam kazanmadığı, küçük bir anlatı zinciri kurulabilir. Ancak kod yalnızca altyapıdır; asıl başarı, ipuçlarının doğal görünmesindedir.

## Sessizliğe güvenmek

İyi çevresel anlatım oyuncuya “Burada ne oldu?” sorusunu sordurur, cevabı hemen bağırmaz. Her ayrıntının tek bir kesin açıklaması olmak zorunda değildir. Kontrollü belirsizlik, oyuncuların teori üretmesini ve deneyimi sahiplenmesini sağlar.

Kısacası mekân, yalnızca karakterlerin yürüdüğü bir sahne değildir; geçmişi, çatışmaları ve duyguları saklayan sessiz bir karakterdir. Doğru yerleştirilmiş bir oyuncak ayı bazen on dakikalık ara sahneden daha fazla şey anlatabilir.
