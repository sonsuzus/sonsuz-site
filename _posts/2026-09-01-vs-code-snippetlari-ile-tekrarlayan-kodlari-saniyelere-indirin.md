---
layout: post
title: "VS Code Snippet’ları ile Tekrarlayan Kodları Saniyelere İndirin"
math: true
categories: 
  - Bilgi
tags: 
  - vs code
  - snippet
  - üretkenlik
toc: true
---

Aynı React bileşenini, test iskeletini veya hata yakalama bloğunu tekrar tekrar yazıyorsanız parmaklarınız gereksiz mesai yapıyor olabilir. Visual Studio Code snippet’ları, sık kullandığınız kod şablonlarını JSON biçiminde tanımlayıp birkaç karakterle çağırmanızı sağlar. Böylece kopyala-yapıştır arşivlerinde kaybolmadan daha hızlı ve tutarlı kod üretebilirsiniz.
``
## Snippet Mantığı Nasıl Çalışır?

Bir snippet; **tetikleyici**, **gövde** ve **açıklama** olmak üzere üç temel parçadan oluşur. Editörde belirlediğiniz kısa ifadeyi yazıp `Tab` veya `Enter` tuşuna bastığınızda VS Code bu ifadeyi gerçek kod şablonuyla değiştirir.

Basitçe kazancı şu modelle düşünebiliriz:

$$T_{kazanç} = n \times (T_{manuel} - T_{snippet})$$

Burada $n$, şablonun kaç kez kullanıldığını gösterir. Bir kod bloğunu elle yazmak 40 saniye, snippet ile çağırmak 5 saniye sürüyorsa ve bunu günde 10 kez kullanıyorsanız günlük kazanç $10 \times 35 = 350$ saniyedir. Küçük görünen bu süre, haftalar içinde ciddi bir üretkenlik artışına dönüşür.

| Yöntem | Hız | Tutarlılık | Hata riski |
|---|---:|---:|---:|
| Elle yazma | Düşük | Orta | Yüksek |
| Kopyala-yapıştır | Orta | Düşük | Orta |
| VS Code snippet | Yüksek | Yüksek | Düşük |

## İlk Snippet’ınızı Oluşturun

Komut paletini `Ctrl+Shift+P` ile açın ve **Snippets: Configure Snippets** komutunu seçin. Ardından belirli bir dil için dosya seçebilir veya tüm projelerde kullanılacak global bir snippet dosyası oluşturabilirsiniz.

Aşağıdaki örnek, JavaScript için hızlı bir `try/catch` bloğu üretir:

```json
{
  "Async Try Catch": {
    "prefix": "atry",
    "body": [
      "try {",
      "  const ${1:result} = await ${2:operation}();",
      "  return $1;",
      "} catch (${3:error}) {",
      "  console.error($3);",
      "  ${0}",
      "}"
    ],
    "description": "Asenkron işlemler için try/catch şablonu"
  }
}
```

Buradaki `prefix`, snippet’ı çağıran kısaltmadır. `body`, editöre eklenecek satırları içerir. `${1:result}` gibi ifadeler ise **tab stop** olarak adlandırılır. Snippet çağrıldığında imleç önce birinci, sonra ikinci ve üçüncü alana gider. `${0}` son imleç konumudur. Aynı `$1` değişkeninin yeniden kullanılması, ilk alana verdiğiniz değerin otomatik olarak tekrar edilmesini sağlar.

## Değişkenlerle Daha Akıllı Şablonlar

VS Code, dosya ve çalışma alanı bilgilerini otomatik alan hazır değişkenler sunar. Örneğin `$TM_FILENAME_BASE`, uzantısız dosya adını getirir. Bu özellik özellikle sınıf ve test şablonlarında kullanışlıdır:

```json
{
  "Test Suite": {
    "prefix": "suite",
    "body": [
      "describe('$TM_FILENAME_BASE', () => {",
      "  it('${1:beklenen davranış}', () => {",
      "    ${2:// test kodu}",
      "  });",
      "});"
    ],
    "description": "Dosya adına göre test paketi oluşturur"
  }
}
```

Bu şablon, test paketinin adını dosyadan alır; sizin yalnızca davranışı ve test kodunu doldurmanız gerekir.

## Etkili Snippet Taktikleri

Kısaltmaları kısa ama ayırt edilebilir seçin. Örneğin `clg` konsol çıktısı, `rfc` React bileşeni, `apierr` API hata bloğu için kullanılabilir. Ancak her iki satırlık kodu snippet’a çevirmek yerine sık kullanılan ve unutulması kolay şablonlara odaklanın.

Ekip projelerinde `.vscode` klasörü altında proje snippet’ları tutmak da güçlü bir taktiktir. Böylece herkes aynı bileşen, loglama ve test standartlarını kullanır. Snippet’lar yalnızca hız aracı değil, aynı zamanda küçük birer kod standardı muhafızıdır. Bir kez doğru tasarlayın; klavyeniz angaryayla değil, asıl problemle uğraşsın.
