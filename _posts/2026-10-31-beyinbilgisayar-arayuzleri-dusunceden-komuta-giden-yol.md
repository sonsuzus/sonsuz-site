---
layout: post
title: "Beyin–Bilgisayar Arayüzleri: Düşünceden Komuta Giden Yol"
math: true
categories: 
  - Bilgi
tags: 
  - beyin-bilgisayar-arayüzü
  - eeg
  - makine-öğrenmesi
  - sinyal-işleme
  - nöroteknoloji
  - python
toc: true
image: /img/beyinbilgisayar-arayuzleri-dusunceden-37.png
---

Klavyeye dokunmadan bir imleci hareket ettirmek mümkün mü? Evet; ancak bilgisayar zihninizdeki bütün cümleleri okumuyor. Beyin–bilgisayar arayüzleri, belirli sinirsel etkinlik örüntülerini ölçüp sınırlı komutlara dönüştürüyor. Yani mesele telepati değil, gürültülü biyolojik sinyallerle çalışan dikkatli bir mühendislik projesi. Beyninizin gizli bir USB portu yok; keşke kurulum bu kadar kolay olsaydı!

``

## Önce beklentiyi doğru ayarlayalım

Bir beyin–bilgisayar arayüzü, İngilizce kısaltmasıyla **BCI**, kas hareketlerini zorunlu tutmadan sinirsel etkinlik üzerinden iletişim kurmayı hedefler. Örneğin kullanıcı sağ veya sol elini hareket ettirdiğini hayal eder; sistem bu iki durumu ayırt etmeye çalışır. Bazı sistemlerdeyse kullanıcı yanıp sönen seçeneklerden birine odaklanır. Buradaki bilgi, serbest düşüncenin içeriği değil, önceden tanımlanmış bir görevle ilişkili örüntüdür.

Ölçüm yöntemleri aynı kapıya farklı yollardan ulaşır:

| Yöntem | Nasıl ölçer? | Avantaj | Temel sınırlama |
|---|---|---|---|
| EEG | Saçlı derideki elektrotlarla | Ameliyat gerektirmez | Gürültü ve düşük uzamsal çözünürlük |
| ECoG | Beyin yüzeyindeki elektrotlarla | Daha yerel sinyaller | Cerrahi işlem gerekir |
| Beyin içi elektrotlar | Sinir dokusu içinden | Ayrıntılı kayıt potansiyeli | Cerrahi risk ve uzun dönem kararlılık |

## Sinyalden komuta: küçük bir çeviri fabrikası

Tipik işlem zinciri şöyledir:

**Ölçüm → temizleme → özellik çıkarımı → sınıflandırma → komut → geri bildirim.**

EEG, tek bir nöronun konuşması değildir. Çok sayıda kaynağın elektriksel etkileri, ölçüm noktasında birbirine karışır. Göz kırpması, çene kasları ve elektrik şebekesi de bu karışıma katılabilir. Dolayısıyla yüksek genlik, otomatik olarak güçlü bir niyet anlamına gelmez.

Motor imgelemede sık incelenen özellikler, yaklaşık **8–13 Hz mu** ve **13–30 Hz beta** bantlarındaki güç değişimleridir. Bu değişimler kişiye ve göreve göre farklılaşır; sabit bir düşünce sözlüğü oluşturmazlar. Özellik vektörünü $h$ ile gösterirsek, basit bir ikili sınıflandırıcı şöyle yazılabilir:

$$z = w^T h + b$$

$$p = 1/(1 + e^{-z})$$

Burada $w$ öğrenilen ağırlıkları, $b$ sabit terimi, $p$ ise modelin bir sınıfa verdiği olasılık tahminini temsil eder. Bu tahminin güvenilirliği ayrıca değerlendirilmelidir. Model, kişinin niyetini doğrudan bilmez; eğitim verisindeki ilişkilere dayanarak karar verir. **Korelasyon, zihin okuma değildir.**

## Python ile bant gücünden sınıflandırmaya

Aşağıdaki örnek, NumPy, SciPy ve scikit-learn kullanır. Dosyada artefaktları önceden ele alınmış EEG denemeleri bulunmalıdır: `X` boyutu `(deneme, kanal, örnek)`, `y` sağ/sol imgeleme etiketleri, `oturum` kayıt oturumu kimlikleri, `fs` örnekleme frekansıdır. En az üç farklı oturum gerekir.

```python
import numpy as np
from scipy.signal import welch
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold, cross_val_score

d = np.load("eeg_denemeleri.npz")
X, y, oturum = d["X"], d["y"], d["oturum"]
fs = float(d["fs"])
f, psd = welch(X, fs=fs,
               nperseg=min(256, X.shape[-1]), axis=-1)

bantlar = []
for alt, ust in [(8, 13), (13, 30)]:
    sec = (f >= alt) & (f < ust)
    guc = np.trapezoid(psd[..., sec], f[sec], axis=-1)
    bantlar.append(np.log(guc + 1e-12))
F = np.concatenate(bantlar, axis=1)

model = make_pipeline(StandardScaler(),
                      LogisticRegression(max_iter=1000))
skorlar = cross_val_score(
    model, F, y, groups=oturum,
    cv=GroupKFold(n_splits=3), scoring="balanced_accuracy"
)
print(skorlar.mean())
```

Welch yöntemi güç spektrumunu tahmin eder; bant integralleri kanal başına özellik üretir. Logaritma, güç değerlerinin geniş aralığını sıkıştırır. Pipeline, ölçekleyicinin yalnızca eğitim bölümünde öğrenilmesini sağlar. Oturum bazlı bölme ise aynı kaydın benzer parçalarının eğitim ve teste karışmasını önler. Kod, NumPy 2 veya üzerindeki `trapezoid` işlevini kullanır.

## Laboratuvardan gerçek hayata geçiş

Yüksek test başarısı, kullanışlı bir arayüz için tek başına yeterli değildir. Gecikme, yanlış komut sıklığı, kalibrasyon süresi ve kullanıcı yorgunluğu da ölçülmelidir. Dengeli doğruluk, sınıfların ayrı ayrı başarılarını eşit ağırlıkla değerlendirir. Rastgele deneme bölmek yerine yeni oturumlarda sınamak, günlük kullanım performansını anlamaya daha çok yardımcı olur.

Gerçek zamanlı sistemde kararsız tahminler komuta dönüştürülmeyebilir. Kullanıcıya geri bildirim vermek ve gerektiğinde onay istemek, özellikle tekerlekli sandalye gibi fiziksel sonuç doğuran uygulamalarda önemlidir. Bu örnek, güvenlik doğrulaması yapılmış bir kontrol sistemi değildir.

Sinirsel kayıtlar da hassas verilerdir: açık rıza, sınırlı saklama ve güvenli erişim tasarımın parçası olmalıdır. Klinik uygulamalarda profesyonel değerlendirme gerekir. Sonuç olarak düşünceden komuta geçmek mümkün; fakat başarılı BCI, sihirli bir okuyucu değil, kullanıcıyla birlikte öğrenen kontrollü bir çevirmen gibi çalışır.

![beyinbilgisayar-arayuzleri-dusunceden-37](/img/beyinbilgisayar-arayuzleri-dusunceden-37.svg)

