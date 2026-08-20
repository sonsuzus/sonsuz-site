---
layout: post
title: "F# ile Finansal Modelleme: Birim Tipleriyle Güvenli Kur ve Risk Hesapları"
math: true
categories: 
  - Program
tags: 
  - f#
  - finansal modelleme
  - birim tipleri
  - risk yönetimi
  - type safety
toc: true
---

Finans yazılımlarında küçük görünen bir hata, büyük bir bilanço sorununa dönüşebilir: Euro tutarını dolar sanmak, yüzde ile ondalık oranı karıştırmak veya günlük volatiliteyi yıllık değer gibi kullanmak oldukça pahalıdır. F#; fonksiyonel yaklaşımı, değişmez verileri ve özellikle **birim tipleri** (units of measure) sayesinde bu hataları daha derleme aşamasında yakalamaya yardımcı olur. Böylece hesap motorunuz yalnızca sonuç üretmez; hangi sonuçların anlamlı olduğunu da denetler.

``

## Neden birim tipi kullanmalıyız?

Birim tipleri, sayılara bağlam ekler. `100m` tek başına sadece bir ondalıktır; ancak `100m<USD>` bunun dolar olduğunu açıkça anlatır. Derleyici de USD ile EUR'yu toplamanıza, metreyi faiz oranına bölmenize veya yıllık volatiliteyi doğrudan günlük getiriyle karşılaştırmanıza engel olur.

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Sadece `decimal` kullanmak | Hızlı prototip | Para birimleri sessizce karışabilir |
| `string` para birimi alanı eklemek | Esnek görünür | Kontrol çalışma zamanına kalır |
| F# birim tipleri | Derleme zamanı güvenliği | Dönüşüm fonksiyonları açıkça tanımlanmalıdır |

Örneğin iki tutarın toplanması matematiksel olarak ancak aynı birimde anlamlıdır:

$$V_{toplam} = V_{USD,1} + V_{USD,2}$$

Buna karşılık USD ve EUR toplamı için önce bir kur gerekir. Eğer $r_{USD/EUR}$, bir USD'nin EUR karşılığıysa:

$$V_{EUR} = V_{USD} \times r_{USD/EUR}$$

## Para birimi dönüşümünü tipe taşıma

Aşağıdaki örnek, para birimlerini ve kuru doğrudan F# tip sistemine tanıtır. `decimal`, finansal tutarlarda ikili kayan nokta hassasiyet sorunlarını azaltmak için tercih edilir.

```fsharp
[<Measure>] type USD
[<Measure>] type EUR

let eurPerUsd = 0.92M<EUR/USD>

let convertUsdToEur (amount: decimal<USD>) : decimal<EUR> =
    amount * eurPerUsd

let invoice = 1250.00M<USD>
let invoiceInEur = convertUsdToEur invoice

printfn "EUR tutarı: %M" (float invoiceInEur)
```

Burada `convertUsdToEur`, yanlışlıkla EUR kabul eden bir fonksiyon değildir: parametresi açıkça `decimal<USD>` olmalıdır. Ayrıca dönüşüm sonucu `decimal<EUR>` olarak işaretlenir. Örneğin `invoice + invoiceInEur` yazmak derlenmez; bu, finansal uygulama için son derece faydalı bir “hayır”dır.

Gerçek sistemlerde kur bilgisini tarih, veri kaynağı ve alış/satış yönü ile saklamak iyi bir fikirdir. Bir merkez bankası kuru ile bankanın satış kuru aynı değildir. Bu nedenle hesaplamanın yanında kullanılan varsayımı da kaydetmek, denetlenebilirlik sağlar.

## Risk hesabında ölçek hatalarını önlemek

Risk analizinde yaygın metriklerden biri parametrik Value at Risk (VaR) değeridir. Normal dağılım varsayımı altında basitleştirilmiş formül şöyledir:

$$VaR = z_{\alpha} \times \sigma \times V \times \sqrt{T}$$

Burada $z_{\alpha}$ güven düzeyi katsayısı, $\sigma$ volatilite, $V$ portföy değeri ve $T$ gün sayısıdır. Volatilite yıllıksa, günlük hesap için önce $\sqrt{252}$ ile ölçeklenmelidir.

```fsharp
[<Measure>] type Day

let annualVolatility = 0.18M
let tradingDays = 252.0M<Day>
let horizon = 10.0M<Day>
let confidenceZ = 2.326M // %99 güven düzeyi

let dailyVolatility = annualVolatility / sqrt (float tradingDays)

let valueAtRisk (portfolio: decimal<USD>) =
    let scaledVol = decimal dailyVolatility * sqrt (float horizon)
    confidenceZ * scaledVol * portfolio

let portfolioValue = 2_000_000M<USD>
let var99 = valueAtRisk portfolioValue
```

Bu örnekte VaR sonucu USD cinsindedir. Ancak dikkat: normal dağılım, sabit volatilite ve likit piyasa varsayımları kriz dönemlerinde zayıflayabilir. Bu yüzden VaR'ı kesin kayıp tahmini değil, belirli varsayımlar altındaki bir risk göstergesi olarak yorumlayın.

## Sağlam aracın son adımı: test

Birim tipleri birçok sınıf hatayı engeller, fakat kurun güncelliğini veya model varsayımlarını doğrulamaz. Dönüşüm testleri, sınır durumları ve negatif pozisyon senaryoları ekleyin. F# ile amaç yalnızca hesap yapmak değildir; yanlış hesapların mümkün olduğu alanı sistematik biçimde daraltmaktır.
