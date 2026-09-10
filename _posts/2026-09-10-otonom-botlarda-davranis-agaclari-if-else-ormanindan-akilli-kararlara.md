---
layout: post
title: "Otonom Botlarda Davranış Ağaçları: If-Else Ormanından Akıllı Kararlara"
math: true
categories: 
  - Bilgi
tags: 
  - oyun yapay zekası
  - behavior trees
  - otonom botlar
toc: true
---

Bir oyun botunu birkaç `if-else` ile hareket ettirmek kolaydır: Düşman varsa saldır, can azsa kaç, aksi hâlde devriye gez. Fakat botun şarj olması, saldırıdan kaçınması, yarım kalan görevine dönmesi ve değişen dünyaya anında tepki vermesi gerektiğinde bu yaklaşım hızla “dokunmaya korkulan kod” seviyesine ulaşır. Davranış Ağaçları, yani Behavior Trees, kararları küçük ve yeniden kullanılabilir düğümlere ayırarak bu karmaşayı yönetilebilir bir orkestraya dönüştürür.

``

## Davranış ağacının temel fikri

Davranış ağacı, kökten başlayarak belirli aralıklarla değerlendirilen hiyerarşik bir karar modelidir. Her düğüm çalıştırıldığında üç durumdan birini döndürür:

- **Success:** Görev başarıyla tamamlandı.
- **Failure:** Görev gerçekleştirilemedi.
- **Running:** Görev sürüyor; sonraki güncellemede devam edilmeli.

Bu durum kümesini matematiksel olarak $S = \{Success, Failure, Running\}$ biçiminde gösterebiliriz. Ağacın her oyun döngüsünde değerlendirilmesine ise genellikle **tick** denir. Saniyedeki değerlendirme sayısı $f$ ve oyun süresi $t$ ise toplam değerlendirme yaklaşık $N = f \times t$ olur. Her karede çalıştırmak şart değildir; örneğin çoğu NPC için saniyede 5-10 tick yeterlidir.

| Düğüm | Çalışma mantığı | Tipik kullanım |
|---|---|---|
| Sequence | Bir çocuk başarısız olana kadar sırayla ilerler | Hedefe git, nişan al, ateş et |
| Selector | Bir çocuk başarılı olana kadar alternatifleri dener | Kaç, saldır veya devriye gez |
| Condition | Dünya durumunu kontrol eder | Can düşük mü? |
| Action | Somut bir davranış gerçekleştirir | Kapıyı aç, mevziye ilerle |
| Decorator | Çocuğun sonucunu ya da tekrarını değiştirir | Üç kez dene, sonucu tersine çevir |

## Kesintiye uğratılabilir davranışlar

Bir bot sandığa doğru yürürken el bombası yakınına düşebilir. Klasik sıralı kod, yürüme işlemi bitene kadar tehlikeyi fark etmeyebilir. Reaktif bir Behavior Tree ise yüksek öncelikli dalları her tick sırasında yeniden kontrol eder. Böylece “acil tehlikeden kaç” dalı, “ganimet topla” dalını kesebilir.

Örnek öncelik sırası şöyle kurulabilir:

1. Ölümcül tehlikeden kaç.
2. Can düşükse iyileş.
3. Görünür düşmana saldır.
4. Verilen görevi tamamla.
5. Devriye gez.

Selector soldan sağa çalışıyorsa ilk başarılı veya çalışan dal kontrolü ele alır. Buradaki kritik ayrıntı, kesilen aksiyonun `Abort` veya `OnExit` aşamasında temizlenmesidir. Navigasyon hedefi iptal edilmeli, animasyon durumu sıfırlanmalı ve ayrılmış kaynaklar bırakılmalıdır.

## Basit bir uygulama iskeleti

Aşağıdaki C# örneği, düğümlerin ortak sözleşmesini ve bir Sequence düğümünü gösterir:

```csharp
public enum NodeState { Success, Failure, Running }

public abstract class Node
{
    public abstract NodeState Tick(Blackboard blackboard);
    public virtual void Abort() { }
}

public sealed class Sequence : Node
{
    private readonly List<Node> children;
    private int activeIndex;

    public Sequence(List<Node> children) => this.children = children;

    public override NodeState Tick(Blackboard blackboard)
    {
        while (activeIndex < children.Count)
        {
            NodeState state = children[activeIndex].Tick(blackboard);

            if (state == NodeState.Running)
                return NodeState.Running;

            if (state == NodeState.Failure)
            {
                activeIndex = 0;
                return NodeState.Failure;
            }

            activeIndex++;
        }

        activeIndex = 0;
        return NodeState.Success;
    }
}
```

`Blackboard`, hedef konumu, görülen düşman ve son hasar zamanı gibi düğümlerin paylaştığı verileri taşır. Böylece düğümler birbirine doğrudan bağımlı olmaz. Ancak blackboard’u her şeyin atıldığı sihirli bir çantaya çevirmemek gerekir; anahtarların türleri ve sahipliği açıkça tanımlanmalıdır.

## Selector tek başına yeterli mi?

Birden fazla uygun hedef bulunduğunda fayda puanı kullanılabilir. Örneğin bir hedefin önceliği

$$U = 0.5D + 0.3T + 0.2V$$

olarak hesaplanabilir. Burada $D$ hasar tehdidini, $T$ hedef yakınlığını, $V$ ise savunmasızlığı temsil eder. Behavior Tree davranışın akışını, Utility AI ise seçeneklerin puanlanmasını yönetir; ikisini birleştirmek oldukça güçlüdür.

Sonuç olarak davranış ağaçları botu gerçekten bilinçli yapmaz, fakat karar mantığını okunabilir, test edilebilir ve kesintiye açık hâle getirir. En iyi başlangıç; küçük aksiyonlar, gözlemlenebilir bir blackboard ve çalışan düğümü ekranda gösteren bir debug aracıdır. Çünkü akıllı bot geliştirmek kadar, botun neden çalıya koştuğunu anlayabilmek de önemlidir.
