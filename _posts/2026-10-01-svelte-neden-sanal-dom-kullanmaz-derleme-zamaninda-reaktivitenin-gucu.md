---
layout: post
title: "Svelte Neden Sanal DOM Kullanmaz? Derleme Zamanında Reaktivitenin Gücü"
math: true
categories: 
  - Bilgi
tags: 
  - svelte
  - javascript
  - reaktivite
  - sanal-dom
  - frontend
  - derleyici
toc: true
image: /img/svelte-neden-sanal-62.png
---

Modern arayüzlerde temel problem basittir: Uygulamanın durumu değiştiğinde ekrandaki doğru bölüm de güncellenmelidir. Birçok framework bu problemi tarayıcıda çalışan bir Sanal DOM katmanıyla çözerken Svelte farklı bir soru sorar: Yapılacak güncellemeleri derleme sırasında biliyorsak neden çalışma zamanında tekrar hesaplayalım?
``
## Sanal DOM yaklaşımı nasıl çalışır?

Sanal DOM, gerçek DOM’un JavaScript nesneleriyle oluşturulmuş hafif bir temsilidir. Durum değiştiğinde yeni bir sanal ağaç üretilir ve önceki ağaçla karşılaştırılır. **Diffing** adı verilen bu işlem hangi gerçek DOM düğümlerinin değiştirilmesi gerektiğini belirler.

Kabaca maliyeti şöyle düşünebiliriz:

$$T_{güncelleme} = T_{render} + T_{diff} + T_{DOM}$$

Burada gerçek DOM işlemi kaçınılmazdır; ancak yeniden render ve karşılaştırma framework tarafından çalışma zamanında eklenen maliyetlerdir. Sanal DOM kötü değildir. Bildirimsel arayüz geliştirmeyi kolaylaştıran, son derece başarılı bir soyutlamadır. Fakat her değişiklikte ağacın ilgili bölümlerini yeniden değerlendirmek gerekir.

| Özellik | Sanal DOM yaklaşımı | Svelte yaklaşımı |
|---|---|---|
| Güncelleme kararı | Tarayıcıda verilir | Derleme sırasında planlanır |
| Karşılaştırma | Eski ve yeni ağaç kıyaslanır | Bilinen DOM düğümü doğrudan değiştirilir |
| Runtime yükü | Framework çalışma zamanı daha belirgindir | Genellikle daha küçüktür |
| Çıktı | Sanal düğüm işlemleri | Hedeflenmiş JavaScript komutları |
| Geliştirici deneyimi | Bildirimsel | Bildirimsel |

## Svelte’in derleyici numarası

Svelte bileşenleri tarayıcıya yazıldıkları biçimde gönderilmez. Derleyici, şablonu ve reaktif bağımlılıkları analiz ederek bunları DOM oluşturan ve güncelleyen JavaScript’e dönüştürür.

```svelte
<script>
  let count = 0;
</script>

<button on:click={() => count += 1}>
  Tıklama: {count}
</button>
```

Bu bileşende derleyici, `count` değerinin yalnızca butondaki metni etkilediğini görebilir. Değer değiştiğinde bütün bileşenin sanal temsilini oluşturup karşılaştırmak yerine ilgili metin düğümünü güncelleyen kod üretir. Basitleştirilmiş zihinsel model şöyledir:

```javascript
const button = document.createElement('button');
let count = 0;

function updateText() {
  button.textContent = `Tıklama: ${count}`;
}

button.addEventListener('click', () => {
  count += 1;
  updateText(); // Yalnızca hedef düğüm güncellenir.
});
```

Gerçek derleyici çıktısı sürüme ve optimizasyonlara göre daha karmaşıktır; bu örnek mimarinin özünü gösterir. Svelte 5 ile öne çıkan `$state`, `$derived` ve `$effect` gibi rune’lar da bağımlılıkların açık ve hassas biçimde izlenmesini sağlar.

## İnce taneli reaktivite

Bir değer yalnızca belirli ifadeleri etkiliyorsa güncelleme kümesi şöyle tanımlanabilir:

$$U(x) = \{d_i \mid d_i\text{ DOM düğümü }x\text{ değerine bağlıdır}\}$$

Svelte’in hedefi, `x` değiştiğinde tüm bileşeni değil yalnızca $U(x)$ kümesindeki düğümleri güncellemektir. Buna **ince taneli reaktivite** denir. Sonuçta tarayıcı, genel amaçlı bir karşılaştırma algoritması çalıştırmak yerine önceden hazırlanmış talimatları uygular.

## Her zaman daha hızlı mı?

“Sanal DOM yoksa kesinlikle daha hızlıdır” demek fazla iddialıdır. Performans; bileşen yapısına, liste büyüklüğüne, güncelleme sıklığına, bellek kullanımına ve geliştiricinin koduna bağlıdır. Büyük listelerde anahtar kullanımı, gereksiz efektlerden kaçınma ve doğru veri modelleme Svelte’te de önemlidir.

Derleme yaklaşımının asıl kazancı yalnızca hız değildir. Daha az runtime kodu, daha küçük paketler ve doğrudan DOM işlemleri sunabilir. Buna karşılık derleyiciye bağımlılık artar; üretilen kodu anlamak bazen daha zordur ve son derece dinamik senaryolar ek çalışma zamanı mekanizmaları gerektirebilir.

Svelte’in yeniliği bildirimsel geliştirme rahatlığını bırakmadan işin önemli bölümünü tarayıcıdan derleme aşamasına taşımasıdır. Kısacası orkestrayı tarayıcıda sürekli prova yaptırmak yerine notaları önceden yazar; tarayıcıya da doğru anda doğru notayı çalmak kalır.

![svelte-neden-sanal-62](/img/svelte-neden-sanal-62.svg)

