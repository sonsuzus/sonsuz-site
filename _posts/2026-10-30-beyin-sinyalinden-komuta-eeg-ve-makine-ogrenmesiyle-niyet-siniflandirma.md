---
layout: post
title: "Beyin Sinyalinden Komuta: EEG ve Makine Öğrenmesiyle Niyet Sınıflandırma"
math: true
categories: 
  - Bilgi
tags: 
  - eeg
  - beyin-bilgisayar arayüzü
  - makine öğrenmesi
  - sinyal işleme
  - python
  - sınıflandırma
toc: true
image: /img/beyin-sinyalinden-komuta-26.png
---

Bir robot kolunu yalnızca hareket etmeyi hayal ederek yönlendirmek, bilim kurgu kulübünden çıkıp araştırma laboratuvarlarına taşındı. Beyin-bilgisayar arayüzleri, EEG sinyallerindeki örüntüleri makine öğrenmesiyle komutlara dönüştürüyor. Ancak burada küçük bir sürpriz var: Sistem, zihninizdeki cümleleri okumuyor; belirli görevlerle ilişkili istatistiksel izleri tanımayı öğreniyor.

``

## EEG gerçekten neyi ölçer?

Elektroensefalografi, kafa derisine yerleştirilen elektrotlarla elektriksel potansiyel farklarını kaydeder. Ölçülen sinyal, çok sayıda nöronun toplu etkinliğinden doğar; tek bir nöronun konuşmasını dinlemek değildir. Kafatası, dokular ve elektrot konumları bu etkinliği karıştırır. Basitleştirilmiş modelimiz $x(t)=As(t)+n(t)$ olsun: $s(t)$ kaynakları, $A$ karışımı, $n(t)$ ise gürültüyü temsil eder.

Dolayısıyla EEG sınıflandırması, kalabalık bir kafede belirli bir konuşma tarzını ayırt etmeye benzer. Üstelik göz kırpmaları ve çene kasları da masaya davetsiz katılır!

| Yaklaşım | Aranan örüntü | Tipik kullanım |
|---|---|---|
| Motor imgeleme | Mü ve beta ritimlerindeki değişim | Sağ/sol hareket niyeti |
| P300 | Hedef uyaran sonrası olay ilişkili yanıt | Harf veya seçenek seçimi |
| SSVEP | Yanıp sönen hedefin frekansıyla ilişkili yanıt | Ekrandaki hedefi seçme |

![beyin-sinyalinden-komuta-26](/img/beyin-sinyalinden-komuta-26.svg)


Bu yaklaşımların eğitim düzenekleri farklıdır; tek bir modelin hepsini kendiliğinden anlayacağını varsayamayız.

## Ham sinyalden öğrenilebilir örneğe

Motor imgelemede kullanıcı, örneğin sağ veya sol elini hareket ettirmeyi hayal eder. Sensörimotor bölgelerdeki yaklaşık 8–13 Hz mü ve 13–30 Hz beta ritimleri bu görev sırasında değişebilir. **Etiket**, tahmin edilen düşünce değil, deneyde kullanıcıya verilen görevdir.

İşlem hattını dört aşamada kurabiliriz:

1. **Kayıt ve etiketleme:** Elektrot konumları, örnekleme hızı ve görev başlangıçları kaydedilir. Hatalı zamanlama, modele yanlış hikâyeyi anlatır.
2. **Ön işleme:** Motor imgeleme için örneğin 8–30 Hz bant geçiren filtre uygulanır. Göz ve kas artefaktları incelenir; öğrenilen temizleme dönüşümleri yalnızca eğitim verisine uydurulur.
3. **Epoklama:** Sürekli kayıt, görev başlangıcına göre zaman pencerelerine ayrılır. Pencerelerin gerçekten hedeflenen imgeleme dönemini kapsaması önemlidir.
4. **Öznitelik ve sınıflandırma:** Bant gücü veya uzamsal filtrelerle çıkarılan özellikler, görev etiketleriyle eşleştirilir.

Filtrelenmiş bir banttaki yaklaşık güç şöyle hesaplanabilir:

$$P_b=\frac{1}{N}\sum_{i=1}^{N}x_b[i]^2$$

Burada $N$ örnek sayısıdır. Güç, ritmin ne kadar baskın olduğunu özetler; fakat tek başına niyetin kesin kanıtı değildir.

## CSP ve LDA: İyi bir başlangıç ikilisi

**Common Spatial Patterns**, iki sınıfın varyanslarını birbirinden ayıran uzamsal filtreler öğrenir. Örneğin bir bileşenin varyansı sağ el imgelemesinde yüksek, sol el imgelemesinde düşük olabilir. Log-varyans özellikleri daha sonra **Linear Discriminant Analysis** sınıflandırıcısına verilir. LDA, sınıfların kovaryans yapısına ilişkin varsayımlarla doğrusal bir karar sınırı kurar. Derin öğrenmeden daha mütevazı görünür, ama küçük EEG veri kümelerinde güçlü bir başlangıçtır.

Aşağıdaki örnek, önceden filtrelenmiş MNE epoklarını kullanır. `labels` görev etiketlerini, `session_ids` oturum kimliklerini içerir. En az üç oturum ve uygun sınıf dağılımı gerekir.

```python
from mne.decoding import CSP
from sklearn.pipeline import Pipeline
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import StratifiedGroupKFold, cross_val_score

X = epochs.get_data(copy=True)  # deneme × kanal × zaman

model = Pipeline([
    ("csp", CSP(n_components=4, reg="oas", log=True)),
    ("lda", LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto"))
])

cv = StratifiedGroupKFold(n_splits=3, shuffle=True, random_state=42)
scores = cross_val_score(
    model, X, labels, groups=session_ids,
    cv=cv, scoring="balanced_accuracy"
)
print(f"Dengeli doğruluk: {scores.mean():.3f}")
```

Pipeline, CSP'nin her katlamada yalnızca eğitim bölümünden öğrenilmesini sağlar. Kovaryans düzenlileştirmesi tahminleri daha kararlı hâle getirebilir. Oturumlara göre ayırma ise aynı kaydın benzer parçalarının eğitim ve teste dağılmasını önler. Yeni kullanıcıya genelleme ölçülecekse gruplama kullanıcı düzeyinde yapılmalıdır.

## Başarı yalnızca doğruluk değildir

Dengeli doğruluk, sınıfların eşit sayıda olmadığı durumlarda yararlıdır. Karışıklık matrisi, hangi komutların birbirine karıştığını gösterir. Ancak gerçek arayüzlerde gecikme, yanlış aktivasyon sıklığı ve kullanıcı yorgunluğu da değerlendirilmelidir. Çevrimdışı yüksek skor, çevrimiçi kullanım garantisi vermez; canlı sistemde nedensel filtreleme ve zaman bütçesi ayrıca sınanmalıdır.

Son aşamada model çıktısı, güven eşiği ve ardışık kararların birleştirilmesiyle komuta dönüştürülebilir. Düşük güvende “komut verme” seçeneği güvenliği artırabilir. EEG verisi hassastır; açık rıza ve sınırlı erişim gerekir. Kısacası başarılı arayüz, sihirli bir zihin okuyucu değil, dikkatle kalibre edilmiş bir örüntü tanıma sistemidir.
