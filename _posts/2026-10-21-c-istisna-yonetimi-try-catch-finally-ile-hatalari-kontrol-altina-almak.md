---
layout: post
title: "C# İstisna Yönetimi: try-catch-finally ile Hataları Kontrol Altına Almak"
math: true
categories: 
  - Bilgi
tags: 
  - csharp
  - exception
  - hata-yönetimi
  - try-catch
  - dotnet
  - özel-istisnalar
toc: true
image: /img/c-istisna-yonetimi-11.png
---

Bir uygulamanın hiç hata üretmemesi neredeyse imkânsızdır; önemli olan, hata ortaya çıktığında sistemin nasıl davrandığıdır. C# istisna yönetimi, beklenmeyen durumları ana program akışından ayırarak uygulamanın kontrollü biçimde tepki vermesini sağlar. Dosya bulunamaması, ağ bağlantısının kesilmesi veya geçersiz kullanıcı girdisi artık birer felaket değil, yönetilebilir senaryolardır.
``
## İstisna nedir?

İstisna, program çalışırken normal akışı bozan olağan dışı bir durumu temsil eden nesnedir. C# içerisindeki bütün istisnalar doğrudan veya dolaylı olarak `System.Exception` sınıfından türetilir.

Bir işlemin başarısız olma olasılığını $P(E)$, hatanın sisteme vereceği zararı da $C(E)$ ile gösterirsek basitleştirilmiş risk hesabı şöyle yazılabilir:

$$R = P(E) \times C(E)$$

İstisna yönetimi hatanın oluşma ihtimalini her zaman azaltmaz; fakat $C(E)$ değerini düşürerek hatanın uygulamanın tamamına yayılmasını engeller.

| Yapı | Görevi | Ne zaman çalışır? |
|---|---|---|
| `try` | Riskli kodu çevreler | Her denemede |
| `catch` | Belirli istisnayı yakalar | Eşleşen hata oluştuğunda |
| `finally` | Kaynak temizliği yapar | Hata olsa da olmasa da |
| `throw` | İstisna oluşturur veya yeniden fırlatır | Koşul sağlandığında |

## try-catch-finally mimarisi

Aşağıdaki örnek bir dosyayı okumayı dener, olası hataları türlerine göre izole eder ve işlem sonunda bilgi verir:

```csharp
try
{
    string metin = File.ReadAllText("ayarlar.json");
    Console.WriteLine(metin);
}
catch (FileNotFoundException ex)
{
    Console.WriteLine($"Dosya bulunamadı: {ex.FileName}");
}
catch (UnauthorizedAccessException)
{
    Console.WriteLine("Dosyaya erişim yetkiniz yok.");
}
catch (IOException ex)
{
    Console.WriteLine($"Girdi/çıktı hatası: {ex.Message}");
}
finally
{
    Console.WriteLine("Dosya okuma denemesi tamamlandı.");
}
```

`catch` blokları özelden genele doğru sıralanmalıdır. Önce `Exception` yakalanırsa daha özel bloklara sıra gelmez. Ayrıca her yerde genel `Exception` yakalayıp hatayı sessizce yutmak, yangın alarmının pilini çıkarmaya benzer: ortam sessizleşir ama yangın devam eder.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Özel istisnayı yakalamak | Anlamlı ve hedefli tepki sağlar | Daha fazla blok gerektirebilir |
| Genel `Exception` yakalamak | Son savunma hattı oluşturur | Gerçek hata nedenini gizleyebilir |
| Hatayı yutmak | Akış görünürde sürer | Teşhis ve veri güvenliği zorlaşır |
| Loglayıp yeniden fırlatmak | Katmanlar arası görünürlük sağlar | Aynı hata birden fazla kez loglanabilir |

Bir istisnayı aynı çağrı yığını bilgisiyle yeniden göndermek için `throw;` kullanılmalıdır. `throw ex;` ifadesi yığın izini değiştirerek hatanın gerçek kaynağını bulmayı zorlaştırabilir.

## Özel hata sınıfları

İş kuralları için hazır istisnalar her zaman yeterince açıklayıcı değildir. Örneğin stok miktarının yetersiz olması teknik değil, alan odaklı bir problemdir:

```csharp
public class YetersizStokException : Exception
{
    public int MevcutStok { get; }

    public YetersizStokException(string mesaj, int mevcutStok)
        : base(mesaj)
    {
        MevcutStok = mevcutStok;
    }
}

public static void SiparisVer(int istenen, int stok)
{
    if (istenen > stok)
    {
        throw new YetersizStokException(
            "İstenen miktar stoktan fazla.", stok);
    }
}
```

Bu sınıf, hataya yalnızca mesaj değil, `MevcutStok` gibi yapılandırılmış bağlam da ekler. Üst katman böylece kullanıcıya uygun bildirim gösterebilir veya işlemi başka bir depoya yönlendirebilir.

## Sağlam kullanım ilkeleri

- İstisnaları yalnızca gerçekten olağan dışı durumlarda kullanın; normal kontrol akışını `throw` ile kurmayın.
- `ArgumentException`, `InvalidOperationException` ve `FileNotFoundException` gibi uygun hazır türleri tercih edin.
- Hataları bağlam bilgisiyle loglayın; parola ve erişim anahtarı gibi hassas verileri kaydetmeyin.
- `IDisposable` kaynaklarında mümkünse `using` kullanın; derleyici gerekli temizliği güvenli biçimde oluşturur.
- Kullanıcıya sade mesaj, geliştiriciye ise ayrıntılı log sağlayın.

Doğru tasarlanmış istisna yönetimi hataları yok etmez; onları sınırlar, görünür kılar ve uygulamanın güvenli biçimde toparlanmasına yardımcı olur. Kısacası `try-catch-finally`, kodun emniyet kemeridir: kazayı engellemeyebilir ama sonucunu ciddi ölçüde kontrol eder.

![c-istisna-yonetimi-11](/img/c-istisna-yonetimi-11.svg)

