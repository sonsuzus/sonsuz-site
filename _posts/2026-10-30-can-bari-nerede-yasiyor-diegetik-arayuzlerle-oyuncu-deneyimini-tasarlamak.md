---
layout: post
title: "Can Barı Nerede Yaşıyor? Diegetik Arayüzlerle Oyuncu Deneyimini Tasarlamak"
math: true
categories: 
  - Bilgi
tags: 
  - oyun-tasarımı
  - arayüz-tasarımı
  - diegetik-arayüz
  - oyuncu-deneyimi
  - unity
  - ux
toc: true
image: /img/can-bari-nerede-39.png
---

Bir uzay istasyonunda yürüyorsunuz. Oksijeniniz azalıyor; peki bunu ekranın köşesindeki bir göstergeden mi, yoksa karakterinizin bileğindeki cihazdan mı öğrenmelisiniz? İkisi de aynı bilgiyi verebilir, fakat aynı deneyimi yaratmaz. Can barının nerede yaşadığı; dikkatinizi, karar hızınızı ve oyun dünyasıyla kurduğunuz ilişkiyi değiştirir.


![can-bari-nerede-39](/img/can-bari-nerede-39.svg)

``

## Önce kavramları yerine oturtalım

**Diegetik arayüz**, oyunun kurmaca dünyasında gerçekten var olan bilgi sunumudur. Karakterin okuyabildiği bir bileklik ekranı veya zırhındaki durum göstergesi buna örnektir. **Diegetik olmayan arayüz** ise doğrudan oyuncuya seslenir: Ekranın köşesinde duran klasik can barını karakteriniz görmez.

Buradaki ayrım yalnızca iki boyutlu ve üç boyutlu olmak değildir. Düşmanın üzerinde süzülen bir can barı, sahnenin içinde çizilse bile kurmaca dünyada karşılığı yoksa otomatik olarak diegetik sayılmaz. Böyle göstergeler çoğunlukla **mekânsal arayüz** olarak değerlendirilir. Asıl soru şudur: Bu bilgi kaynağı, hikâyenin evreninde mevcut mu?

| Özellik | Diegetik arayüz | Diegetik olmayan arayüz |
|---|---|---|
| Bilginin taşıyıcısı | Dünyadaki nesne veya cihaz | Ekrana sabitlenmiş gösterge |
| Görünürlük | Bakışa, ışığa ve mesafeye bağlı olabilir | Genellikle daha tutarlıdır |
| Kurmaca ile ilişki | Dünyanın işleyişine katılır | Oyuncuya dışarıdan bilgi verir |
| Tipik örnek | Kıyafetteki sağlık göstergesi | Köşedeki can barı |

Bu sınıflar bir kalite sıralaması değildir. Diegetik tasarım her zaman daha sürükleyici, klasik HUD ise her zaman daha anlaşılır olmak zorunda değildir. Uygulama ve bağlam belirleyicidir.

## Oyuncunun dikkat bütçesi

Oyuncu çatışma sırasında düşmanı, çevreyi ve kaynaklarını aynı anda izler. Can bilgisini almak için bileğini kaldırması gerekiyorsa, bilgiye erişmek başlı başına bir eyleme dönüşür. Bu, korku oyununda gerilim yaratabilir; hızlı bir rekabetçi oyunda ise gereksiz sürtünme oluşturabilir.

Bu maliyeti düşünmek için basit bir model kullanabiliriz:

$$T_{tepki} = T_{bulma} + T_{okuma} + T_{karar}$$

Burada göstergeyi bulmak, anlamak ve karar vermek ayrı aşamalardır. Bu denklem evrensel bir ölçüm yasası değil, tasarım sorularını düzenleyen bir çerçevedir. Göstergeyi dünyaya yerleştirmek ilk iki süreyi artırıyorsa, kazandığınız atmosferin bu maliyeti karşılayıp karşılamadığını test etmelisiniz.

## Unity: Aynı sağlık, iki farklı sunum

Aşağıdaki örnek, tek sağlık değerini hem ekran üzerindeki bir `Image` bileşenine hem de kıyafetteki uyarı lambasını temsil eden bir `Light` bileşenine aktarır. HUD nesnesini ekran uzayındaki Canvas içine yerleştirin; `Image Type` ayarını `Filled` yapın. Lambayı ise karakterin ekipmanına bağlayın.

```csharp
using UnityEngine;
using UnityEngine.UI;

public class HealthFeedback : MonoBehaviour
{
    [SerializeField] private Image hudBar;
    [SerializeField] private Light suitLight;
    [SerializeField] private float maxHealth = 100f;
    private float health;

    private void Awake()
    {
        maxHealth = Mathf.Max(1f, maxHealth);
        health = maxHealth;
        Refresh();
    }

    public void TakeDamage(float amount)
    {
        health = Mathf.Clamp(
            health - Mathf.Max(0f, amount), 0f, maxHealth);
        Refresh();
    }

    private void Refresh()
    {
        float ratio = health / maxHealth;
        if (hudBar != null)
            hudBar.fillAmount = ratio;
        if (suitLight != null)
            suitLight.intensity = Mathf.Lerp(0.2f, 2f, ratio);
    }
}
```

Sağlık oranı $r = H/H_{max}$ ile normalize edilir. `TakeDamage`, negatif hasarı engeller ve sağlığı geçerli aralıkta tutar. `Refresh`, aynı veriyi iki görsel kanala dönüştürür. Büyük projelerde sağlık modeliyle sunum bileşenlerini ayırmak daha uygundur; burada bağlantıyı görünür tutmak için birlikte gösteriyoruz. Lambanın ayrıca görünür bir gövdesi ve anlaşılır bir kurmaca gerekçesi olmalıdır.

## Hangisini seçmeli?

Seçimi yalnızca estetik tercihle yapmayın. Oyunun temposu, bilginin önemi ve oyuncunun görsel koşulları birlikte değerlendirilmelidir. Diegetik bir lambanın parlaklığı, aydınlık sahnelerde kolayca kaybolabilir. Kritik bilgiyi yalnızca renkle anlatmak da erişilebilirlik sorunları yaratır.

| Tasarım hedefi | Denenebilecek yaklaşım |
|---|---|
| Gerilim ve kırılganlık | Etkileşim gerektiren diegetik gösterge |
| Hızlı ve kesin karar | Kolay okunabilen sabit HUD |
| Atmosfer ile erişilebilirlik | Diegetik gösterge ve isteğe bağlı HUD |

İki sürümü aynı görevde deneyin. Oyuncuların düşük sağlığı fark etme süresini, kaçırdığı uyarıları ve öznel sürükleyicilik değerlendirmelerini karşılaştırın. Kamera hareketi, ekran boyutu ve ışık koşullarını da değiştirin. Böylece yalnızca güzel görünen değil, farklı koşullarda işleyen bir tasarım seçersiniz.

Sonuçta iyi arayüz, kendini gizleyen arayüz değildir. Oyuncuya doğru bilgiyi doğru anda veren arayüzdür. Bazen bu bilgi bilekte yaşar; bazen ekranın köşesinde. Can barının adresinden çok, oyuncunun onu gerektiğinde bulabilmesi önemlidir.
