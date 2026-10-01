---
layout: post
title: "CAP Teoreminden PACELC’ye: Ağ Bölünmesi Yokken Hangi Bedeli Ödüyoruz?"
math: true
categories: 
  - Bilgi
tags: 
  - cap-teoremi
  - pacelc
  - dağıtık-sistemler
  - tutarlılık
  - gecikme
  - erişilebilirlik
toc: true
image: /img/cap-teoreminden-pacelcye-54.png
---

Dağıtık sistem tasarlarken CAP teoremi genellikle sahnenin yıldızıdır: Ağ bölünmesi yaşandığında tutarlılık mı, erişilebilirlik mi? Fakat sistemler hayatlarının büyük bölümünü ağ felaketi yaşamadan geçirir. İşte PACELC, projektörü bu sakin anlara çevirir ve rahatsız edici soruyu sorar: “Ağ düzgün çalışırken düşük gecikme mi, güçlü tutarlılık mı istiyorsun?” Çünkü dağıtık sistemlerde ücretsiz öğle yemeği yoktur; yalnızca faturanın farklı zamanlarda gelmesi vardır.
``
## CAP neden tek başına yeterli değil?

CAP teoremindeki üç özellik şöyledir:

- **Consistency (C):** Her istemci aynı anda aynı güncel veriyi görür.
- **Availability (A):** Her istek, başarılı veya başarısız, mutlaka bir yanıt alır.
- **Partition Tolerance (P):** Düğümler arasındaki iletişim kopsa bile sistem çalışmayı sürdürür.

Bir ağ bölünmesi oluştuğunda sistemin temel seçimi kabaca şöyle ifade edilir:

$$P \Rightarrow C \;\text{veya}\; A$$

Gerçek dünyadaki dağıtık sistemlerde ağ bölünmelerini tamamen yok sayamayız. Bu nedenle “CA sistemi kurarım” demek çoğu durumda bölünme toleransından vazgeçmek değil, problemi halının altına süpürmektir. CAP’in asıl mesajı, **bölünme sırasında** C ile A arasında karar verilmesidir.

Ancak CAP, ağ sağlıklıyken yapılan tercih hakkında fazla konuşmaz. PACELC tam bu boşluğu doldurur.

## PACELC açılımı

PACELC şu mantığı temsil eder:

$$\text{if Partition: Availability or Consistency; else: Latency or Consistency}$$

Kısa gösterimiyle:

$$P \Rightarrow A/C, \qquad E \Rightarrow L/C$$

Buradaki **E**, “Else”, yani ağ bölünmesi yoksa anlamına gelir. Sistem normal çalışırken bile güçlü tutarlılık için düğümlerin haberleşmesi, onay vermesi ve bazen lider üzerinde uzlaşması gerekir. Bu koordinasyon gecikmeyi artırır.

| Durum | Birinci tercih | İkinci tercih | Temel bedel |
|---|---|---|---|
| Ağ bölünmesi var | Erişilebilirlik | Tutarlılık | Eski veri veya reddedilen istek |
| Ağ bölünmesi yok | Düşük gecikme | Tutarlılık | Koordinasyon süresi |
| Yerel okuma | Çok hızlı yanıt | Olası eski veri | Zayıf tutarlılık |
| Liderden okuma | Güncel veri | Ek ağ turu | Yüksek gecikme |

## Gecikme neden tutarlılığın rakibi?

Üç kopyalı bir sistemde yazma işleminin çoğunluk tarafından onaylanmasını beklediğimizi düşünelim. Kopya sayısı $N$, yazma çoğunluğu $W$ ve okuma çoğunluğu $R$ olsun. Güçlü okuma garantisi için yaygın koşul şudur:

$$R + W > N$$

Örneğin $N=3$, $W=2$ ve $R=2$ seçilirse okuma ile yazma kümeleri en az bir düğümde kesişir. Bu, güncel sürüme ulaşmayı kolaylaştırır; fakat iki düğümden yanıt beklemek, yalnızca en yakın düğüme sormaktan daha yavaştır.

Aşağıdaki basitleştirilmiş Python örneği bu farkı gösterir:

```python
replica_latencies = [12, 35, 80]  # Milisaniye

def quorum_latency(latencies, required):
    """Gerekli en hızlı kopyaların tamamlanma süresini hesaplar."""
    selected = sorted(latencies)[:required]
    return max(selected)

print("Yerel okuma:", quorum_latency(replica_latencies, 1), "ms")
print("Çoğunluk okuması:", quorum_latency(replica_latencies, 2), "ms")
```

Yerel okuma yaklaşık 12 ms sürerken çoğunluk okuması 35 ms’ye çıkar. Kod gerçek bir veritabanının tüm karmaşıklığını modellemez; koordinasyon için daha fazla kopya beklemenin gecikmeyi nasıl büyüttüğünü görünür kılar.

## Sistemler PACELC’de nereye yerleşir?

Dynamo tarzı sistemler ve birçok Cassandra yapılandırması genellikle **PA/EL** karakteri gösterir: Bölünmede erişilebilirliği, normal durumda düşük gecikmeyi öne çıkarır. Buna karşılık güçlü lider koordinasyonu veya senkron çoğaltma kullanan sistemler **PC/EC** tarafına yaklaşır. Google Spanner gibi sistemler, küresel ölçekte güçlü tutarlılığı korumak için zaman senkronizasyonu ve koordinasyon maliyetini bilinçli biçimde üstlenir.

Bu sınıflandırmalar mutlak değildir. Cassandra’da consistency level, veritabanlarında senkron veya asenkron çoğaltma ve okuma politikaları tercihi sorgu bazında değiştirebilir.

## Sonuç: Sakin havanın da bir maliyeti var

PACELC, mimari kararları yalnızca felaket senaryolarına göre vermememizi söyler. Ağ bölünmesi nadir olabilir; fakat gecikme her istekte hissedilir. Banka bakiyesi için birkaç milisaniyelik koordinasyon kabul edilebilirken sosyal medya beğeni sayısında eski bir değer çoğu zaman sorun değildir. Doğru seçim, “en güçlü” modeli seçmek değil; iş gereksiniminin hangi hatayı, ne kadar süreyle tolere edebildiğini açıkça belirlemektir.

![cap-teoreminden-pacelcye-54](/img/cap-teoreminden-pacelcye-54.svg)

