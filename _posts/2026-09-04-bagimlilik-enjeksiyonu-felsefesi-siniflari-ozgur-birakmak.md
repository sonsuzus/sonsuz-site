---
layout: post
title: "Bağımlılık Enjeksiyonu Felsefesi: Sınıfları Özgür Bırakmak"
math: true
categories: 
  - Bilgi
tags: 
  - dependency-injection
  - nesne-yonelimli-programlama
  - solid
toc: true
---

Bir sınıfın ihtiyaç duyduğu araçları kendi içinde üretmesi ilk bakışta pratik görünebilir. Ancak proje büyüdüğünde bu yaklaşım, sınıfları birbirine görünmez halatlarla bağlar. Bağımlılık Enjeksiyonu (Dependency Injection veya DI), bu halatları keserek nesnelerin ihtiyaçlarını dışarıdan almasını sağlar. Sonuç; daha modüler, değiştirilebilir ve test edilebilir bir yazılım mimarisidir.

``

## Bağımlılık nedir?

Bir nesnenin görevini yerine getirebilmek için kullandığı başka bir nesneye **bağımlılık** denir. Örneğin `SiparisServisi`, sipariş sonrasında e-posta göndermek için `EpostaGonderici` kullanıyorsa gönderici, servisin bağımlılığıdır.

Sorun bağımlılığın varlığı değil, sınıf tarafından doğrudan oluşturulmasıdır:

```csharp
public class SiparisServisi
{
    private readonly EpostaGonderici _gonderici;

    public SiparisServisi()
    {
        _gonderici = new EpostaGonderici();
    }

    public void Tamamla()
    {
        _gonderici.Gonder("Sipariş tamamlandı.");
    }
}
```

Burada `SiparisServisi`, somut `EpostaGonderici` sınıfına sıkıca bağlıdır. SMS göndermek, farklı bir sağlayıcı kullanmak veya test sırasında gerçek e-posta gönderimini engellemek istediğimizde servis kodunu değiştirmemiz gerekir.

Bu ilişkiyi basitçe şöyle düşünebiliriz:

$$S \rightarrow E$$

Burada $S$ sipariş servisini, $E$ ise somut e-posta göndericisini temsil eder. DI uygulandığında ilişki bir soyutlama üzerinden kurulur:

$$S \rightarrow I \leftarrow E$$

$I$, iki tarafın üzerinde anlaştığı arayüzdür. Böylece servis, gönderimin nasıl yapıldığını değil yalnızca yapılabildiğini bilir.

## Kontrolü tersine çevirmek

Bağımlılık Enjeksiyonu, **Inversion of Control** yaklaşımının uygulama biçimlerinden biridir. Geleneksel modelde sınıf bağımlılığını seçer ve üretir. DI modelinde bu sorumluluk uygulamanın başlangıç noktası veya bir DI konteyneri tarafından üstlenilir.

| Yaklaşım | Bağımlılığı kim oluşturur? | Test edilebilirlik | Esneklik |
|---|---|---:|---:|
| Doğrudan oluşturma | Sınıfın kendisi | Düşük | Düşük |
| Dependency Injection | Dış kod veya konteyner | Yüksek | Yüksek |
| Service Locator | Global servis sağlayıcı | Orta | Orta |

Service Locator bazen DI ile karıştırılır. Ancak bu yöntemde sınıf, ihtiyacını global bir kayıt mekanizmasından arar. Bağımlılıklar kurucu imzasında görünmediği için kodun gereksinimleri gizlenebilir.

## Constructor Injection uygulaması

En yaygın ve güvenli yöntem, bağımlılıkları kurucu üzerinden vermektir:

```csharp
public interface IBildirimGonderici
{
    void Gonder(string mesaj);
}

public class SiparisServisi
{
    private readonly IBildirimGonderici _gonderici;

    public SiparisServisi(IBildirimGonderici gonderici)
    {
        _gonderici = gonderici;
    }

    public void Tamamla()
    {
        _gonderici.Gonder("Sipariş tamamlandı.");
    }
}
```

Bu kodda servis, e-posta veya SMS ayrıntısını bilmez. Tek beklentisi, verilen nesnenin `IBildirimGonderici` sözleşmesine uymasıdır. Gerçek uygulamada bağımlılık bir DI konteynerine kaydedilebilir:

```csharp
services.AddScoped<IBildirimGonderici, EpostaGonderici>();
services.AddScoped<SiparisServisi>();
```

Konteyner, `SiparisServisi` oluşturulurken uygun göndericiyi otomatik olarak kurucuya verir.

## Testlerde sağladığı avantaj

DI sayesinde gerçek servis yerine sahte bir nesne kullanılabilir:

```csharp
public class SahteGonderici : IBildirimGonderici
{
    public bool Gonderildi { get; private set; }

    public void Gonder(string mesaj)
    {
        Gonderildi = true;
    }
}
```

Böylece test; internet bağlantısı, SMTP sunucusu veya ücretli bir API olmadan yalnızca iş davranışını doğrular. Test maliyetini kabaca bağımlılık sayısıyla ilişkilendirirsek sıkı bağlı bir sistemde değişiklik etkisi $O(n)$ seviyesine yayılabilirken, iyi soyutlanmış bir tasarımda hedeflenen bileşene daha yakın tutulabilir.

Elbette her sınıf için arayüz üretmek DI değildir; bu, gereksiz soyutlama festivaline dönüşebilir. Değişme ihtimali olan, dış kaynak kullanan veya testlerde ikame edilmesi gereken bağımlılıklar önceliklidir. DI’nin asıl felsefesi konteyner kullanmak değil, nesnelere “İhtiyacını kendin üretme; sana verilsin” diyerek sorumlulukları doğru yere taşımaktır.
