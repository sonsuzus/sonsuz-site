---
layout: post
title: "Copilot Çağında Rubber-Stamp Programming: Yapay Zeka Kod Editörleri Zihni Tembelleştiriyor mu?"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zeka
  - github copilot
  - yazılım geliştirme
  - programlama psikolojisi
  - üretken yapay zeka
  - kod kalitesi
toc: true
image: /img/copilot-caginda-rubber-98.png
---

![copilot-caginda-rubber-98](/img/copilot-caginda-rubber-98.svg)


Üretken yapay zekâ destekli kod editörleri, birkaç yorum satırından fonksiyon üretebiliyor, test yazabiliyor ve sıkıcı tekrarları saniyeler içinde tamamlayabiliyor. Ancak hız göstergesi yükselirken küçük bir uyarı ışığı yanıyor: Yazılımcı, kabul ettiği kodu gerçekten anlıyor mu? Copilot benzeri araçlar tek başına zihinsel tembellik yaratmaz; fakat yanlış kullanım alışkanlıkları geliştiriciyi kodun yazarı olmaktan çıkarıp yalnızca önerilere onay veren bir operatöre dönüştürebilir.

``

## Rubber-stamp programming nedir?

Rubber-stamp programming, yapay zekânın önerdiği kodu mantığını, sınırlarını ve güvenlik sonuçlarını incelemeden kabul etme davranışıdır. Editörde `Tab` tuşuna basmak kolaydır; önerinin neden doğru olduğunu açıklamak ise bilişsel emek ister.

Bu durum psikolojideki **bilişsel yük boşaltma** kavramıyla ilişkilidir. İnsanlar hesap makinesi, navigasyon veya not uygulaması kullanırken bazı zihinsel görevleri dış araçlara devreder. Bu her zaman kötü değildir. Sorun, aracın belleği desteklemek yerine düşünmenin tamamının yerini almasıdır.

Basitleştirilmiş bir modelle öğrenme kazanımını şöyle düşünebiliriz:

$$L = E × R × F$$

Burada $L$ öğrenme düzeyini, $E$ zihinsel çabayı, $R$ aktif hatırlamayı ve $F$ geri bildirimi temsil eder. Yapay zekâ hızı artırırken zihinsel çabayı sıfıra yaklaştırırsa öğrenme kazanımı da düşebilir. Başka bir deyişle, hızlı teslimat ile kalıcı uzmanlık aynı metrik değildir.

## Otomasyon mu, zihinsel tembellik mi?

| Kullanım biçimi | Kısa vadeli sonuç | Uzun vadeli olası etki |
|---|---|---|
| Tekrarlı kodu üretme | Zaman kazandırır | Yaratıcı işlere daha fazla odaklanma |
| Kodu sorgulamadan kabul etme | Görev hızla biter | Kavramsal boşluk ve hata ayıklama zorluğu |
| Alternatif çözüm isteme | Seçenekleri görünür kılar | Tasarım bilgisini geliştirebilir |
| Açıklama ve test talep etme | İnceleme süresini artırır | Aktif öğrenmeyi destekler |
| Her problemi yapay zekâya bırakma | Başlangıçta rahatlık sağlar | Otomasyon yanlılığı ve bağımlılık yaratabilir |

Buradaki önemli psikolojik risk **otomasyon yanlılığıdır**. İnsan, sistem çoğu zaman doğru sonuç verdiğinde hatalı önerileri de doğru kabul etmeye yatkınlaşır. Üstelik akıcı ve özgüvenli görünen kod, gerçekte olmayan bir güven hissi yaratabilir. Sözdiziminin düzgün olması; algoritmanın doğru, güvenli veya ölçeklenebilir olduğu anlamına gelmez.

## Pasif kabul yerine aktif inceleme

Örneğin yapay zekâ aşağıdaki fonksiyonu önermiş olsun:

```javascript
function average(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}
```

Kod kısa ve makul görünür. Fakat boş bir dizi gönderildiğinde sonuç `NaN` olur. Aktif inceleme yapan geliştirici yalnızca kodun ne yaptığına değil, hangi varsayımlarla çalıştığına da bakar:

```javascript
function average(values) {
  if (!Array.isArray(values) || values.length === 0) {
    throw new Error('En az bir sayısal değer gerekli');
  }

  if (!values.every(Number.isFinite)) {
    throw new TypeError('Tüm elemanlar sonlu sayı olmalı');
  }

  return values.reduce((sum, value) => sum + value, 0) / values.length;
}
```

İkinci sürüm yalnızca daha dayanıklı değildir; geliştiriciyi girdi doğrulama, hata politikası ve veri sözleşmesi hakkında düşünmeye zorlar. Öğrenmeyi sağlayan bölüm çoğu zaman kodun üretilmesi değil, bu sorgulama sürecidir.

## Zihinsel kasları koruyan çalışma düzeni

Yapay zekâyı bir otomatik pilot değil, hızlı bir eşli programcı gibi kullanmak gerekir. Öneriyi kabul etmeden önce kodu kendi cümlelerinizle açıklayın. Zaman ve bellek karmaşıklığını tahmin edin, sınır durumlarını listeleyin ve en az bir testi kendiniz yazın. Kritik modüllerde araçtan önce kısa bir çözüm taslağı hazırlayın; böylece ilk öneriye saplanma etkisini azaltabilirsiniz.

Ayrıca düzenli olarak yapay zekâsız çalışma seansları yapmak yararlıdır. Amaç teknolojiyi reddetmek değil, temel becerilerin hâlâ erişilebilir olduğunu doğrulamaktır. Bir pilot otomatik uçuş kullanabilir; yine de uçağı manuel olarak yönetebilmelidir.

Sonuç olarak üretken yapay zekâ, yazılımcıyı kaçınılmaz biçimde tembelleştirmez. Tembellik riski aracın varlığından değil, düşünme sorumluluğunun devredilmesinden doğar. Sağlıklı kullanımda Copilot kod yazma süresini azaltırken inceleme, tasarım ve öğrenme için alan açar. Tehlikeli kullanımda ise geliştirici çok kod üretir, fakat giderek daha az kod anlar.
