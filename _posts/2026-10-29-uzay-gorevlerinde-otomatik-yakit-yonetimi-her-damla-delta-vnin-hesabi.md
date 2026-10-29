---
layout: post
title: "Uzay Görevlerinde Otomatik Yakıt Yönetimi: Her Damla Delta-v’nin Hesabı"
math: true
categories: 
  - Bilgi
tags: 
  - uzay
  - algoritma
  - optimizasyon
  - yakıt-yönetimi
  - python
  - otonom-sistemler
toc: true
image: /img/uzay-gorevlerinde-otomatik-23.png
---

Uzay aracında yakıt göstergesinin kırmızıya yaklaşması, otomobilde benzin istasyonu aramaya benzemez; uzayda yol kenarında yakıt satan bir tesis yoktur. Bu nedenle otomatik yakıt yönetimi algoritmaları, görevin başından sonuna kadar her manevrayı planlar, belirsizlikleri hesaba katar ve bilimsel hedeflerle güvenlik arasında sürekli denge kurar.
``

## Yakıt değil, delta-v bütçesi

Görev mühendisleri çoğunlukla yalnızca kilogram cinsinden yakıttan değil, aracın hızını ne kadar değiştirebileceğini gösteren **delta-v** bütçesinden söz eder. Bir yörünge düzeltmesi, istasyon koruma manevrası veya iniş ateşlemesi bu bütçeden harcama yapar.

Roket denklemi, yakıt ile erişilebilir hız değişimi arasındaki ilişkiyi açıklar:

$$Δv = I_{sp} g_0 ln(m_0 / m_f)$$

Burada $I_{sp}$ motorun özgül itkisi, $g_0$ standart yerçekimi ivmesi, $m_0$ başlangıç kütlesi ve $m_f$ yakıt harcandıktan sonraki kütledir. Denklem logaritmik olduğu için iki kat yakıt, iki kat delta-v sağlamaz. Üstelik taşınan ekstra yakıtın kendisi de hızlandırılmalıdır; uzay mühendisliğinin küçük ama pahalı şakası budur.

| Yaklaşım | Avantajı | Dezavantajı |
|---|---|---|
| Sabit bütçe | Basit ve doğrulanabilir | Değişen koşullara uyum sağlayamaz |
| Açgözlü seçim | Anlık olarak ucuz manevrayı seçer | Gelecekteki ihtiyaçları gözden kaçırabilir |
| Dinamik programlama | Çok aşamalı kararları değerlendirir | Durum sayısı hızla büyür |
| Model öngörülü kontrol | Sistemi düzenli olarak yeniden planlar | Yüksek hesaplama gücü gerektirir |

![uzay-gorevlerinde-otomatik-23](/img/uzay-gorevlerinde-otomatik-23.svg)


## Algoritma neyi optimize eder?

Bir görev planlayıcısının amacı yalnızca en az yakıtı harcamak değildir. Manevra süresi, haberleşme penceresi, termal sınırlar, çarpışma riski ve bilimsel kazanç da önemlidir. Bu nedenle maliyet fonksiyonu birkaç hedefi birleştirebilir:

$$J = w_f F + w_t T + w_r R - w_s S$$

$F$ yakıt tüketimini, $T$ süreyi, $R$ riski ve $S$ bilimsel getiriyi temsil eder. $w$ katsayıları ise görev önceliklerini belirler. Bir asteroid sondasında bilimsel getiri ağır basabilirken insanlı görevde güvenlik katsayısı çok daha yüksek tutulur.

Algoritma ayrıca yakıtın tamamını planlanan manevralara dağıtmaz. Motor performansındaki sapmalar, navigasyon hataları ve beklenmeyen yörünge düzeltmeleri için bir **rezerv** bırakır. Böylece teorik olarak mükemmel fakat ilk sürprizde başarısız olan kırılgan planlardan kaçınılır.

## Basitleştirilmiş bir seçim algoritması

Aşağıdaki Python örneği, manevraları bilimsel değerlerinin yakıt maliyetine oranına göre seçer. Bu yöntem gerçek görev yazılımı değildir; yakıt kısıtı altında karar verme mantığını görünür kılan küçük bir modeldir.

```python
def gorevleri_sec(manevralar, toplam_yakit, rezerv_orani=0.20):
    kullanilabilir = toplam_yakit * (1 - rezerv_orani)
    secilenler = []

    # Bir kilogram yakıt başına en fazla değeri üretenleri öne alır.
    sirali = sorted(
        manevralar,
        key=lambda m: m["bilimsel_deger"] / m["yakit"],
        reverse=True
    )

    for manevra in sirali:
        if manevra["yakit"] <= kullanilabilir:
            secilenler.append(manevra["ad"])
            kullanilabilir -= manevra["yakit"]

    return secilenler, kullanilabilir
```

Bu açgözlü yaklaşım hızlıdır; ancak en iyi küresel sonucu garanti etmez. Örneğin düşük değerli görünen bir yörünge düzeltmesi, daha sonra yüksek değerli bir gözlemi mümkün kılabilir. Gerçek sistemler bu bağımlılıkları karma tamsayılı programlama, dinamik programlama veya sezgisel arama yöntemleriyle ele alır.

## Uçuş sırasında yeniden planlama

Uzay ortamı kusursuz tahmin edilemez. Ölçülen konum beklenenden farklı çıktığında algoritma yeni durumu kestirir, kalan yakıtı hesaplar ve gelecekteki manevraları yeniden optimize eder. Model öngörülü kontrolde bu döngü düzenli olarak tekrarlanır: tahmin et, optimize et, ilk komutu uygula ve yeni ölçüm gelince baştan hesapla.

| Durum | Algoritmanın tepkisi |
|---|---|
| Motor beklenenden zayıf | Manevra süresini uzatır veya hedefi küçültür |
| Yakıt kaçağı şüphesi | Rezerv oranını artırır, düşük öncelikleri iptal eder |
| Yeni bilimsel fırsat | Getiri-maliyet hesabını yeniden yapar |
| Çarpışma riski | Güvenliği öne alarak acil manevra planlar |

Sonuç olarak otomatik yakıt yönetimi, bir depo ölçümünden çok daha fazlasıdır. İyi bir algoritma bugünkü manevrayı gerçekleştirirken aylar sonra gereken son düzeltmeyi de düşünür. Uzayda başarı, motoru en uzun süre çalıştırmak değil, doğru anda doğru miktarda çalıştırmaktır.
