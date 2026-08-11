---
layout: post
title: "Yapay Zeka Temelleri: Turing Testinden Derin Öğrenmeye Uzanan Yol"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zeka
  - makine öğrenmesi
  - turing testi
---

Yapay zeka (YZ), makinelerin yalnızca hesap yapmasını değil; algılamasını, öğrenmesini, karar vermesini ve kimi zaman yaratıcı görünen çıktılar üretmesini hedefleyen disiplinler arası bir alandır. Bugünkü üretken modeller bir anda ortaya çıkmadı: mantık, olasılık, bilişsel bilim, istatistik ve bilgisayar mühendisliğinin onlarca yıllık ortak birikimiyle şekillendi. Bu tarihi anlamak, güncel "akıllı" sistemlerin neden bazen etkileyici, bazen de şaşırtıcı biçimde hatalı davranabildiğini kavramanın en iyi yoludur.
``

## Kavramsal başlangıç: Makineler düşünebilir mi?

Alanı popülerleştiren sorulardan biri Alan Turing’in 1950’deki önerisiydi: Bir makinenin düşünmesini doğrudan tanımlamak yerine, davranışını değerlendirebilir miyiz? **Turing testi**, bir insan sorgulayıcının yazılı konuşmada insan ile makineyi güvenilir şekilde ayırt edememesi fikrine dayanır. Test, zekânın kesin bir ölçümü değil; doğal dil, muhakeme ve sosyal bağlam yeteneği için etkili bir düşünce deneyidir.

1956 Dartmouth çalıştayı ise “artificial intelligence” adının akademik sahneye çıktığı dönüm noktasıdır. İlk iyimserlik dalgasında araştırmacılar, doğru kurallar yeterince çok yazılırsa genel zekâya yaklaşılabileceğini düşündü. Bu yaklaşım **sembolik yapay zekâ** olarak bilinir: Bilgi, açık semboller ve mantıksal kurallarla temsil edilir.

| Yaklaşım | Temel fikir | Güçlü tarafı | Zayıf tarafı |
|---|---|---|---|
| Sembolik YZ | Kurallar ve mantıkla çıkarım | Açıklanabilir kararlar | Gerçek dünyanın belirsizliği |
| Makine öğrenmesi | Veriden örüntü öğrenme | Uyarlanabilirlik | Veri kalitesine bağımlılık |
| Derin öğrenme | Çok katmanlı sinir ağları | Görüntü ve dil başarısı | Yüksek hesaplama maliyeti |

## Kurallardan veriye: Öğrenmenin yükselişi

1980’lerde uzman sistemler, doktorluk veya kredi değerlendirmesi gibi dar alanlarda “eğer-ise” kurallarıyla başarı sağladı. Ancak kural sayısı büyüdükçe sistemlerin bakımı zorlaştı. Buna karşılık makine öğrenmesi, kuralları insanın tek tek yazması yerine örneklerden tahmin etmeyi önerdi.

Denetimli öğrenmede amaç, girdiler $x$ ile hedefler $y$ arasındaki ilişkiyi öğrenen $f_\theta(x)$ fonksiyonunu bulmaktır. Model parametreleri $\theta$, tahmin hatasını azaltacak biçimde güncellenir:

$$
\theta \leftarrow \theta - \eta \nabla_\theta L(y, f_\theta(x))
$$

Burada $L$ kayıp fonksiyonu, $\eta$ öğrenme oranıdır. Formül sade görünse de kritik nokta şudur: Model, eğitim verisini ezberlemek yerine daha önce görmediği örneklere de genellemelidir. Aşırı öğrenme (overfitting), bu dengenin bozulduğu klasik problemdir.

Aşağıdaki küçük Python örneği, eğitim ve test hatası farkını gözlemlemek için temel bir doğrusal model kurar:

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression().fit(X_train, y_train)

train_error = mean_squared_error(y_train, model.predict(X_train))
test_error = mean_squared_error(y_test, model.predict(X_test))
print(train_error, test_error)
```

Bu kodun amacı bir modeli “akıllı” ilan etmek değil, eğitimdeki başarının gerçek dünyadaki başarıyla aynı olmadığını göstermektir. Test hatası belirgin biçimde büyükse veri, model karmaşıklığı veya değerlendirme yöntemi yeniden ele alınmalıdır.

## Modern dönem: Derin ağlar ve üretken modeller

2010’lardan itibaren büyük veri kümeleri, GPU’lar ve daha iyi optimizasyon yöntemleri derin öğrenmeyi hızlandırdı. Evrişimsel ağlar görüntülerde, tekrarlayan ağlar ise sıralı verilerde öne çıktı. Ardından Transformer mimarisi, dikkat (attention) mekanizması sayesinde uzun metin ilişkilerini daha verimli modelledi. Büyük dil modelleri, bir sonraki belirteci tahmin etme hedefinden başlayarak çeviri, özetleme ve kod üretimi gibi çok sayıda beceri sergileyebildi.

Yine de modern YZ, insan benzeri bilinç veya kusursuz muhakeme anlamına gelmez. Önyargılı veri, gizlilik, telif, enerji tüketimi ve yanlış bilgi üretimi; teknolojik başarının yanında ele alınması gereken temel meselelerdir. Turing’in sorusu hâlâ canlıdır, fakat bugün daha iyi bir soru şudur: Bu sistemler hangi koşullarda güvenilir, adil ve denetlenebilir biçimde yararlı olur?
