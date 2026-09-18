---
layout: post
title: "ECS Mimarisi: Oyun Nesnelerini Kalıtım Değil Kompozisyonla Kurmak"
math: true
categories: 
  - Bilgi
tags: 
  - ecs
  - oyun geliştirme
  - kompozisyon
  - mimari
  - performans
  - csharp
toc: true
---

Bir oyunda oyuncu, düşman, uçan düşman, zehirli uçan düşman derken sınıf ağacınız aile albümüne dönebilir. Entity-Component-System (ECS), bu karmaşaya farklı bir soru sorarak yaklaşır: “Bu nesne nedir?” yerine “Hangi verilere sahip ve hangi davranışlara katılıyor?” Böylece oyun nesneleri derin kalıtım zincirleriyle değil, küçük parçaların bir araya getirilmesiyle oluşturulur.

``

## ECS’nin temel fikri

ECS mimarisi üç ana kavramdan oluşur:

- **Entity:** Bir oyun nesnesini temsil eden benzersiz kimliktir. Çoğu zaman yalnızca bir tam sayıdır.
- **Component:** Konum, hız, sağlık veya hasar gibi saf verileri tutar. Genellikle davranış içermez.
- **System:** Belirli component kümelerine sahip entity’leri bulur ve onların verilerini işler.

Örneğin bir entity üzerinde `Position` ve `Velocity` bulunuyorsa hareket sistemi onu hareket ettirebilir. Aynı entity’ye `Health` eklendiğinde nesne artık hasar alabilir. `Player` adında devasa bir sınıfa veya `FlyingPoisonousEnemy` gibi giderek uzayan alt sınıflara ihtiyaç kalmaz.

| Yaklaşım | Kalıtım | ECS kompozisyonu |
|---|---|---|
| Nesne tanımı | Sınıf türüyle | Component kümesiyle |
| Davranış | Nesnenin metotlarında | System katmanında |
| Yeniden kullanım | Üst sınıfa bağlı | Component ekleyip çıkararak |
| Değişiklik | Sınıf ağacını etkileyebilir | Genellikle yerel kalır |
| Veri düzeni | Nesneler arasında dağınık | Benzer veriler birlikte tutulabilir |

## Kompozisyon neden daha esnektir?

Kalıtımda ilişki çoğunlukla “bir türüdür” şeklindedir: ejderha bir düşmandır. Kompozisyonda ise “şunlara sahiptir” denir: ejderhanın konumu, sağlığı, uçuş yeteneği ve ateş saldırısı vardır. Ateş saldırısını başka bir yaratığa vermek için ortak bir üst sınıf tasarlamak yerine ilgili component’i eklemek yeterlidir.

Bir entity’nin yapısını matematiksel olarak component kümesiyle gösterebiliriz:

$$E_i = \{C_{position}, C_{velocity}, C_{health}\}$$

Bir hareket sistemi yalnızca gerekli alt kümeyi arar:

$$Required_{movement} = \{C_{position}, C_{velocity}\}$$

Dolayısıyla $Required_{movement} \subseteq E_i$ ise sistem o entity’yi işler. ECS sorgularının temel mantığı budur.

## Küçük bir C# örneği

Aşağıdaki sadeleştirilmiş örnekte component’ler yalnızca veri taşır. `MovementSystem` ise konum ve hız verilerini kullanarak güncelleme yapar:

```csharp
public struct Position
{
    public float X;
    public float Y;
}

public struct Velocity
{
    public float X;
    public float Y;
}

public static class MovementSystem
{
    public static void Update(
        Span<Position> positions,
        ReadOnlySpan<Velocity> velocities,
        float deltaTime)
    {
        for (int i = 0; i < positions.Length; i++)
        {
            positions[i].X += velocities[i].X * deltaTime;
            positions[i].Y += velocities[i].Y * deltaTime;
        }
    }
}
```

Buradaki denklem oldukça tanıdıktır: $p_{yeni} = p_{eski} + v \times \Delta t$. Önemli nokta, hareket davranışının herhangi bir oyuncu veya düşman sınıfına ait olmamasıdır. Gerekli verilere sahip tüm entity’ler aynı sistem tarafından işlenebilir.

## Performans tarafı: önbellek dostu veriler

ECS yalnızca temiz tasarım sağlamak için kullanılmaz. Component verileri bellekte ardışık tutulduğunda işlemci önbelleği daha verimli çalışabilir. Klasik nesne yönelimli düzende farklı adreslere dağılmış nesneler arasında dolaşmak gerekebilir. ECS’de ise sistem, örneğin binlerce `Position` değerini art arda okuyabilir.

Yaklaşık işlem maliyeti entity sayısıyla doğrusal büyür:

$$T(n) = O(n)$$

Ancak gerçek kazanç yalnızca karmaşıklık sınıfından değil; daha az önbellek kaçırma, toplu işleme ve paralelleştirme imkânından gelir.

## ECS her proje için doğru mu?

ECS; çok sayıda benzer nesne, yoğun simülasyon veya çalışma anında değişen yetenekler bulunan oyunlarda parlayabilir. Buna karşılık küçük bir menü oyunu ya da az sayıda karmaşık nesne için gereksiz altyapı oluşturabilir. Entity yaşam döngüsü, component sorguları ve sistem sıralaması ayrıca dikkatli tasarlanmalıdır.

En sağlıklı yaklaşım ECS’yi sihirli bir performans düğmesi olarak değil, veriyi davranıştan ayıran bir düşünme modeli olarak görmektir. Kalıtım “Sen nesin?” diye sorarken ECS “Nelerin var ve hangi işlemlere katılıyorsun?” der. Oyun dünyaları büyüdükçe ikinci soru çoğu zaman daha kullanışlıdır.
