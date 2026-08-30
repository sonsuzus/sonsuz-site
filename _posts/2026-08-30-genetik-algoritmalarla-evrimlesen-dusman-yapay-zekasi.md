---
layout: post
title: "Genetik Algoritmalarla Evrimleşen Düşman Yapay Zekâsı"
math: true
categories: 
  - Proje
tags: 
  - genetik algoritma
  - oyun yapay zekâsı
  - game development
  - evrimsel hesaplama
  - Unity
---

Oyunlardaki düşmanların çoğu, tasarımcının önceden yazdığı davranış ağaçları ve durum makineleriyle hareket eder. Bu yaklaşım güvenilir olsa da oyuncu aynı taktiği tekrar ettiğinde kolayca tahmin edilebilir hâle gelir. Genetik algoritmalar (GA) ise düşman stratejilerini bir popülasyon olarak ele alır: başarılı taktikler hayatta kalır, birbirleriyle çaprazlanır ve küçük mutasyonlarla yeni çözümler üretir. Sonuç, oyuncunun “hep köşede bekleyip keskin nişancı kullanma” alışkanlığına zamanla karşı önlem geliştirebilen daha dinamik bir rakiptir.
``

Genetik algoritmanın temel fikri biyolojik evrimden gelir. Her düşman politikası bir **kromozom**, politikayı oluşturan sayısal kararlar ise **gen** kabul edilir. Örneğin kromozom; saldırı mesafesi, siper arama isteği, takım arkadaşına yaklaşma oranı ve geri çekilme eşiği içerebilir. Bir nesildeki tüm aday çözümler popülasyonu oluşturur. Her aday kısa bir simülasyonda oyuncuya karşı denenir; ardından başarısına göre bir uygunluk (fitness) puanı alır.

Bir düşmanın uygunluğunu sadece “oyuncuyu öldürdü mü?” sorusuyla ölçmek kötü bir fikirdir. Böyle bir ölçüm, yapay zekâyı ucuz ama eğlencesiz taktiklere itebilir. Bunun yerine hasar, hayatta kalma, alan kontrolü ve davranış çeşitliliğini dengeli biçimde puanlayabiliriz:

$$F = 0.35D + 0.25S + 0.20A + 0.20V$$

Burada $D$ verilen hasarını, $S$ hayatta kalma süresini, $A$ stratejik alan kontrolünü, $V$ ise son nesillerden farklı davranma miktarını temsil eder. Katsayılar oyunun türüne göre ayarlanmalıdır. Bir korku oyununda hayatta kalma yerine gerilim yaratma; bir takım nişancı oyununda ise koordinasyon daha yüksek ağırlık alabilir.

| Kavram | Oyun içindeki karşılığı | Neden önemlidir? |
|---|---|---|
| Kromozom | Saldırı, kaçış ve konumlanma parametreleri | Davranışın ayarlanabilir temsilidir |
| Seçilim | Başarılı düşmanların ebeveyn seçilmesi | İyi taktikleri korur |
| Çaprazlama | İki stratejinin genlerini birleştirmek | Yeni kombinasyonlar üretir |
| Mutasyon | Bir parametreyi küçük oranda değiştirmek | Yerel optimum tuzağını azaltır |
| Elitizm | En iyi birkaç adayı doğrudan taşımak | Başarılı çözümün kaybolmasını önler |

Aşağıdaki C# benzeri örnek, davranış parametreleri taşıyan basit bir genomun nasıl mutasyona uğrayabileceğini gösterir. Bu kod, doğrudan tam bir düşman sistemi değildir; evrim katmanının temel veri modelidir.

```csharp
[System.Serializable]
public class EnemyGenome
{
    public float preferredRange;   // Hedefe yaklaşmak istediği mesafe
    public float coverPriority;    // Siper arama eğilimi: 0-1
    public float retreatHealth;    // Bu can oranında geri çekilir
    public float fitness;

    public EnemyGenome CloneAndMutate(float mutationRate)
    {
        var child = (EnemyGenome)MemberwiseClone();
        if (Random.value < mutationRate)
            child.preferredRange += Random.Range(-2f, 2f);
        if (Random.value < mutationRate)
            child.coverPriority = Mathf.Clamp01(child.coverPriority + Random.Range(-.15f, .15f));
        if (Random.value < mutationRate)
            child.retreatHealth = Mathf.Clamp01(child.retreatHealth + Random.Range(-.10f, .10f));
        child.fitness = 0;
        return child;
    }
}
```

Uygulamada her karede evrim yapmak yerine, bunu maç sonunda veya belirli karşılaşma paketleri sonrasında çalıştırmak daha mantıklıdır. Oyuncu telemetrisi; kullanılan silah, ölüm konumu, ortalama angajman mesafesi ve kaçış rotası gibi bilgileri sağlar. Sistem bu verileri doğrudan “oyuncuyu hileyle okumak” için değil, eğilimleri sınıflandırmak için kullanmalıdır.

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Çevrimdışı evrim | Kararlı testler, düşük çalışma maliyeti | Oyuncuya geç tepki verir |
| Maç arası evrim | Kişiselleştirilmiş karşılık üretir | Denge testleri gerekir |
| Gerçek zamanlı evrim | Çok uyarlanabilir görünür | CPU maliyeti ve öngörülemezlik yüksektir |

Son olarak, evrimleşen düşman “kazanmak” yerine **ilginç karşı oyun üretmeyi** hedeflemelidir. Mutasyon oranını çok yükseltmek kaotik düşmanlar yaratır; çok düşürmek ise popülasyonu tekdüzeleştirir. Küçük popülasyonlar için $0.05 \leq m \leq 0.15$ aralığındaki mutasyon oranı iyi bir başlangıç noktasıdır. İnsan tasarımıyla sınırlandırılmış, telemetriyle beslenen ve eğlence metrikleriyle denetlenen bir GA sistemi; düşmanları sadece daha zor değil, daha unutulmaz da yapabilir.
