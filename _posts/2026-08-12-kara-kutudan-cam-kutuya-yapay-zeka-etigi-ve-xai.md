---
layout: post
title: "Kara Kutudan Cam Kutuya: Yapay Zeka Etiği ve XAI"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zeka
  - xaı
  - etik
  - makine öğrenmesi
image: /img/kara-kutudan-cam-47.png
---

Yapay zeka sistemleri kredi başvurularından işe alıma, tıbbi önceliklendirmeden içerik önerilerine kadar hayatı etkileyen kararlar veriyor. Ancak yüksek doğruluk oranı, tek başına güvenilirlik anlamına gelmez: Bir modelin *neden* belirli bir sonucu ürettiğini anlayamıyorsak, hatayı, önyargıyı ve sorumluluğu da izleyemeyiz. Açıklanabilir Yapay Zeka (XAI), bu kara kutuyu herkesin tüm matematiğini ezberlemesini beklemeden denetlenebilir bir “cam kutuya” dönüştürme çabasıdır.

![kara-kutudan-cam-47](/img/kara-kutudan-cam-47.svg)

``

## Etik neden sadece doğruluk değildir?

Bir sınıflandırıcının doğruluğu basitçe şu şekilde ölçülebilir:

$$Accuracy = \frac{TP + TN}{TP + TN + FP + FN}$$

Burada doğru pozitifler ($TP$) ve doğru negatifler ($TN$) artsa da model, belirli bir gruba karşı sistematik biçimde hatalı davranabilir. Örneğin işe alım modeli geçmişte çoğunlukla belirli bir grubun işe alındığı verilerle eğitilmişse, başarı etiketi aslında yetenekten çok tarihsel ayrımcılığı taşıyabilir. Model bunu kötü niyetle yapmaz; fakat verideki kalıbı verimli biçimde yeniden üretir. İşte bu yüzden “algoritma tarafsızdır” cümlesi, test edilmesi gereken bir varsayımdır.

| Kavram | Sorduğu soru | Örnek risk |
|---|---|---|
| Doğruluk | Tahmin ne kadar isabetli? | Başarılı görünen ama adaletsiz model |
| Adalet | Hata yükü gruplara eşit mi? | Bir gruba daha fazla yanlış ret |
| Şeffaflık | Sistem nasıl çalışıyor? | Gizli kuralların denetlenememesi |
| Hesap verebilirlik | Hata olunca kim sorumlu? | “Model öyle dedi” savunması |

Adalet için kullanılan ölçütlerden biri, gruplar arasındaki olumlu karar oranlarını karşılaştıran **demografik parite**dir:

$$P(\hat{Y}=1 \mid A=a) \approx P(\hat{Y}=1 \mid A=b)$$

Fakat bu ölçütün her durumda yeterli olduğunu söylemek yanıltıcıdır. Grupların gerçek dağılımları, hataların maliyeti ve yasal bağlam farklıdır. Etik, tek bir metrik düğmesine basmak değil; etkilenen kişilerle birlikte değer çatışmalarını değerlendirmektir.

## XAI hangi sorulara yanıt verir?

Açıklamalar iki ölçekte üretilir. **Küresel açıklama**, modelin genel davranışını anlatır: Gelir artınca kredi onayı eğilimi yükseliyor mu? **Yerel açıklama** ise tekil kararı inceler: Bu başvuru neden reddedildi? LIME ve SHAP gibi yöntemler, bir tahminde özelliklerin etkisini yaklaşık olarak gösterir. Ancak açıklama, kararın otomatik olarak doğru ya da adil olduğu anlamına gelmez; yalnızca inceleme için bir iz bırakır.

| Yaklaşım | Güçlü yanı | Sınırlılığı |
|---|---|---|
| Karar ağacı | Doğal olarak okunabilir kurallar | Karmaşık ilişkilerde zayıflayabilir |
| SHAP | Özellik katkılarını karşılaştırır | Hesaplama maliyeti yüksek olabilir |
| LIME | Tek karar için hızlı içgörü | Farklı örneklemelerde değişkenlik gösterebilir |
| Model kartı | Amaç, veri ve sınırları belgeler | Tek başına canlı denetim sağlamaz |

Aşağıdaki örnek, bir tahminin basit ve okunabilir biçimde nasıl gerekçelendirilebileceğini gösterir. Gerçek hayatta bu skorun eğitim verisi, eşikleri ve grup bazlı hata oranları ayrıca denetlenmelidir.

```python
def kredi_gerekcesi(gelir, gecikme_sayisi):
    skor = 0
    nedenler = []

    if gelir >= 40000:
        skor += 2
        nedenler.append("gelir eşiğin üzerinde")
    if gecikme_sayisi == 0:
        skor += 2
        nedenler.append("gecikmiş ödeme kaydı yok")

    karar = "onay" if skor >= 3 else "manuel inceleme"
    return karar, nedenler
```

Bu kodun faydası yalnızca sonucu vermesi değil, sonucu etkileyen kuralları açıkça sunmasıdır. Yine de gelir gibi bir değişken, sosyal eşitsizlikleri dolaylı biçimde yansıtabilir. Açıklanabilirlik bu nedenle “hangi özellik etkili?” sorusundan sonra “bu özelliği kullanmak meşru mu?” sorusunu da doğurur.

## Sorumlu bir XAI süreci

Sağlıklı yaklaşım; veri kökenini belgelemek, hassas gruplardaki hata oranlarını ölçmek, kullanıcıya anlaşılır itiraz kanalı sunmak ve modeli zaman içinde izlemektir. Özellikle yüksek riskli alanlarda insan denetimi, göstermelik bir onay düğmesi değil, kararı değiştirebilecek yetki olmalıdır. İyi XAI, modelin karmaşıklığını makyajlamaz; sınırlarını dürüstçe görünür kılar. Çünkü güven, yalnızca doğru tahminden değil, gerekçesi sorgulanabilen ve hatası düzeltilebilen kararlardan doğar.
