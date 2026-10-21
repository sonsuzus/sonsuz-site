---
layout: post
title: "Robotik Sinir Ağı Kontrolünde Kararlılık: Zeki Ama Garantisi Nerede?"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - yapay sinir ağları
  - kontrol teorisi
  - kararlılık
  - lyapunov
  - makine öğrenmesi
toc: true
image: /img/robotik-sinir-agi-70.png
---

Bir robot kolunun sinir ağıyla kusursuz biçimde bardak taşıdığını düşünün. Etkileyici, değil mi? Peki kol daha ağır bir bardakla, eğitilmediği bir açıyla veya gürültülü sensörlerle karşılaşırsa ne olur? Yapay sinir ağı tabanlı kontrolcüler yüksek performans gösterebilse de klasik kontrol teorisinin sevdiği türden matematiksel kararlılık garantilerini çoğu zaman beraberinde getirmez.

``

## Kararlılık neden bu kadar önemli?

Bir dinamik sistemi genel olarak

$$\dot{x}=f(x,u)$$

şeklinde ifade edebiliriz. Burada $x$ sistemin durumu, $u$ ise kontrol girişidir. Kontrolcünün görevi, örneğin robotun eklem açılarını hedeflenen denge noktasına taşımaktır.

Klasik yaklaşımda $u=K(x)$ seçilir ve kapalı çevrim sisteminin davranışı matematiksel olarak incelenir. Lyapunov teorisi bunun en güçlü araçlarından biridir. Pozitif tanımlı bir $V(x)$ fonksiyonu için

$$V(x)>0, \qquad \dot{V}(x)<0$$

koşulları sağlanıyorsa sistemin denge noktasına doğru ilerlediği gösterilebilir. Başka bir ifadeyle enerji benzeri bir değer sürekli azalır. Robot, matematiksel bir yokuştan aşağı yuvarlanarak hedefe yaklaşır.

Sinir ağı kontrolcüsünde ise giriş genellikle

$$u=\pi_\theta(x)$$

biçimindedir. Çok katmanlı ve doğrusal olmayan $\pi_\theta$ fonksiyonu, milyonlarca parametre içerebilir. Bu nedenle tüm durum uzayında $\dot{V}(x)<0$ olduğunu kanıtlamak oldukça zordur.

## Klasik ve öğrenen kontrolcü karşılaştırması

| Özellik | Klasik kontrol | Sinir ağı tabanlı kontrol |
|---|---|---|
| Model ihtiyacı | Genellikle açık model gerekir | Veriden öğrenebilir |
| Kararlılık analizi | Lyapunov, kutup ve frekans yöntemleri güçlüdür | Ağın karmaşıklığı analizi zorlaştırır |
| Genelleme | Tasarım bölgesiyle sınırlıdır | Eğitim dışı durumlarda belirsizdir |
| Açıklanabilirlik | Görece yüksektir | Çoğu zaman kara kutudur |
| Performans | Karmaşık görevlerde sınırlanabilir | Yüksek boyutlu görevlerde başarılı olabilir |

Buradaki temel sorun sinir ağlarının mutlaka kararsız olması değildir. Sorun, eğitim başarısının kanıt anlamına gelmemesidir. Bir kontrolcünün milyonlarca simülasyonda hata yapmaması, henüz denenmemiş bir durumda güvenli kalacağını garanti etmez. Özellikle dağılım kayması, sensör arızası, model belirsizliği ve dış bozucular robotu eğitim verisinin dışına taşıyabilir.

## Simülasyon testi neden yeterli değildir?

Aşağıdaki basit Python kodu, öğrenilmiş bir kontrolcüyü farklı başlangıç durumlarında deneyerek son durum normunu ölçer:

```python
import numpy as np

def controller(x):
    # Gerçekte burada eğitilmiş sinir ağı çalıştırılır.
    return -1.8 * x + 0.15 * np.tanh(4 * x)

def simulate(x, dt=0.01, steps=1000):
    for _ in range(steps):
        u = controller(x)
        x = x + dt * (-0.4 * x + u)
    return x

for x0 in np.linspace(-5, 5, 21):
    final_state = simulate(x0)
    print(x0, abs(final_state))
```

Bu deney faydalıdır; çünkü başarısız başlangıç bölgelerini ortaya çıkarabilir. Ancak yalnızca 21 nokta test edilir. Sürekli durum uzayında sonsuz sayıda olasılık bulunduğundan, başarılı sonuçlar biçimsel bir ispat oluşturmaz. Test güven verir, kanıt ise sınırları tanımlar.

## Garantiyi güçlendiren yaklaşımlar

Araştırmacılar bu açığı kapatmak için birkaç yöntemi birlikte kullanıyor:

- **Lyapunov tabanlı öğrenme:** Ağ, yalnızca görev ödülünü değil, $\dot{V}(x)<0$ koşulunu da dikkate alarak eğitilir.
- **Control Barrier Function:** Kontrol girişleri güvenli durum kümesinde kalacak şekilde filtrelenir.
- **Hibrit mimari:** Sinir ağı yüksek performanslı komut üretirken klasik kontrolcü güvenlik katmanı olarak çalışır.
- **Doğrulama araçları:** Aralık analizi, erişilebilirlik analizi ve karma tamsayılı programlama ile ağın belirli bölgelerdeki çıktıları sınırlandırılır.
- **Gürbüzlük analizi:** Bozucular altında durumun sınırlı kaldığını göstermek için input-to-state stability gibi kavramlardan yararlanılır.

Pratikte en güvenli yaklaşım, sinir ağını tek başına direksiyona oturtmak yerine ona matematik bilen bir yardımcı pilot vermektir. Öğrenen kontrolcü çeviklik ve uyarlanabilirlik sağlarken klasik katman fiziksel sınırları, tork kısıtlarını ve güvenli çalışma bölgesini korur.

Sonuç olarak robotikte başarı ölçütü yalnızca görevi tamamlamak değildir. Kontrolcünün hangi koşullarda güvenli olduğunu bilmek de gerekir. Sinir ağları güçlü sürücülerdir; fakat kararlılık kanıtı olmadan emniyet kemerleri henüz tam bağlanmış sayılmaz.

![robotik-sinir-agi-70](/img/robotik-sinir-agi-70.svg)

