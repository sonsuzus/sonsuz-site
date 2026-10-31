---
layout: post
title: "Bir Gövde, Birçok Görev: Modüler Robot Tasarımının Esnekliği"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - modüler tasarım
  - mekatronik
  - python
  - otomasyon
toc: true
image: /img/bir-govde-bircok-15.png
---

![bir-govde-bircok-15](/img/bir-govde-bircok-15.svg)


Bir robotun sabah depoda kutu taşıyıp öğleden sonra serada bitki kontrolü yaptığını düşünün. Bunu iki ayrı makineyle çözmek mümkün; ancak modüler tasarım, aynı gövdenin hareket, algılama ve tutma bileşenlerini değiştirerek farklı görevlere uyarlanmasını sağlar. Robot biraz LEGO setine benzer, fakat burada parçaların yalnızca birbirine oturması değil, birlikte güvenle çalışması gerekir.
``

## Modülerlik: Parçalardan Daha Büyük Bir Fikir

Modüler robot, belirli işlevleri bağımsız birimlere ayıran robot mimarisidir. Tekerlek takımı hareketi, kamera çevreyi algılamayı, kavrayıcı ise nesnelerle etkileşimi üstlenebilir. Her birimin görev sınırı ve bağlantı kuralları açıkça tanımlanır. Böylece bir bileşeni değiştirmek, robotun tamamını yeniden tasarlamayı gerektirmez. Buradaki temel ilke, **işlevsel ayrıştırma ve standart arayüzlerdir**.

Bu yaklaşımın iki yaygın biçimi vardır. Sabit gövdeli sistemlerde uç araçlar ve sensörler değiştirilir. Yeniden yapılandırılabilir sistemlerde ise bağlantılı modüller robotun fiziksel biçimini de değiştirebilir. İlk yaklaşım endüstriyel uygulamalarda daha kolay yönetilirken ikincisi daha geniş hareket olanakları sunar; buna karşılık kontrol ve bağlantı tasarımı zorlaşır.

Mimariyi $G=(V,E)$ grafiğiyle düşünebiliriz: $V$ modülleri, $E$ ise aralarındaki bağlantıları temsil eder. Bağlantının mekanik, elektriksel veya veri taşıyan niteliği önemlidir. Bir kameranın takılabilmesi, kontrol yazılımının onu kullanabileceği anlamına gelmez!

| Özellik | Sabit tasarım | Modüler tasarım |
|---|---|---|
| Görev değişimi | Yeni tasarım gerekebilir | Uygun parça değiştirilebilir |
| Bakım | Bütün sisteme müdahale gerekebilir | Arızalı birim ayrılabilir |
| Optimizasyon | Tek görevde yüksek olabilir | Arayüzlerden kaynaklanan ödünleşimler vardır |
| Başlangıç geliştirmesi | Daha sade olabilir | Standartlaştırma yatırımı ister |

## Esnekliğin Gizli Kahramanı: Arayüzler

Başarılı modülerlik, bağlantı noktasında başlar. Mekanik arayüz; ölçüleri, kilitleme yöntemini ve taşınabilecek yükü belirlemelidir. Elektriksel arayüz; gerilim, akım sınırı, kutuplama ve koruma düzenini tanımlar. Veri arayüzü ise mesaj biçimini, haberleşme hızını ve hata davranışını kapsar. CAN veya Ethernet kullanmak tek başına yeterli değildir; modüllerin aynı mesajların anlamında da anlaşması gerekir.

Yazılım tarafında sürücüler, donanım ayrıntılarını ortak yeteneklere dönüştürebilir. Örneğin farklı kavrayıcılar aynı “aç”, “kapat” ve “durum oku” işlemlerini sunar. Böylece görev planlayıcısı marka veya model yerine yeteneklerle çalışır. Yine de kavrama kuvveti ve konum hassasiyeti gibi sınırlar ayrıca bildirilmelidir.

Fizik kuralları ise tak-çıkar heyecanına kapılmaz. Bir kolun yükten kaynaklanan torku basitçe $T=F r$ ile hesaplanır. Burada $F$ kuvvet, $r$ dönme eksenine olan dik uzaklıktır. Aynı yükü iki kat uzağa taşımak, tork ihtiyacını iki katına çıkarır. Dolayısıyla daha uzun modül, daha güçlü motor veya daha düşük taşıma kapasitesi gerektirebilir.

## Python ile Göreve Uygun Yapılandırma

Aşağıdaki örnek, seçilen modüllerin besleme gerilimini ve görev yeteneklerini denetler. Donanımı hareket ettirmez; yapılandırmanın yazılım düzeyindeki bir ön kontrolüdür. Python 3.9 ve üzeriyle çalışır.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Module:
    name: str
    capabilities: frozenset[str]
    voltage: int = 24

modules = {
    "drive": Module("Tekerlek", frozenset({"hareket"})),
    "gripper": Module("Kavrayıcı", frozenset({"kavrama"})),
    "camera": Module("Kamera", frozenset({"görüntüleme"})),
}

def configure(names, required):
    selected = [modules[name] for name in names]
    if any(module.voltage != 24 for module in selected):
        raise ValueError("Besleme gerilimi uyumsuz")
    available = frozenset().union(
        *(module.capabilities for module in selected)
    )
    missing = set(required) - available
    if missing:
        raise ValueError(f"Eksik yetenekler: {sorted(missing)}")
    return [module.name for module in selected]

print(configure(["drive", "gripper"], {"hareket", "kavrama"}))
print(configure(["drive", "camera"], {"hareket", "görüntüleme"}))
```

İlk çağrı taşıma, ikinci çağrı gözlem görevine uygun parçaları seçer. Gerçek uygulamada bu kontrole mekanik uyumluluk, akım bütçesi, haberleşme protokolü ve güvenlik kısıtları da eklenmelidir. Yetenek etiketi, performans garantisi değildir.

## Parça Değiştiğinde Ne Yeniden Kontrol Edilmeli?

Modül değişimi sonrasında robotun kütlesi, ağırlık merkezi ve durma mesafesi değişebilir. Kamera değişirse kalibrasyon; kavrayıcı değişirse kuvvet sınırları ve araç koordinat sistemi güncellenmelidir. Yapılandırma kaydı tutmak, hangi donanımın hangi yazılım sürümüyle test edildiğini izlemeyi kolaylaştırır. Bu kayıtlar bakım ekibinin “Dün çalışıyordu!” bilmecesini çözmesinde özellikle değerlidir.

Sistem özel olarak enerjiliyken değişime uygun tasarlanmamışsa parçalar güç kesilerek değiştirilmelidir. Ardından bağlantılar doğrulanmalı, düşük hızda işlev testi yapılmalı ve güvenlik sınırları yeniden değerlendirilmelidir.

Modülerlik her durumda daha ucuz veya daha hafif değildir. Ek bağlantılar maliyet, boşluk ve arıza noktası yaratabilir. Ancak görevler sık değişiyorsa ortak gövdeyi korumak ciddi avantaj sağlar. İyi tasarlanmış modüler robot, her işi kusursuz yapan sihirli makine değil; yeni işleri kontrollü biçimde öğrenebilen bir mühendislik platformudur.
