---
layout: post
title: "Structural Typing ve Nominal Typing: “Neyi Biliyorsun?” mu “Kimsin?” mi?"
math: true
categories: 
  - Bilgi
tags: 
  - structural typing
  - nominal typing
  - typescript
  - java
  - tip sistemleri
  - programlama
toc: true
---

Bir nesne kapıya geldiğinde tip sistemi ona iki farklı soru sorabilir: “Gerekli özelliklere sahip misin?” veya “Hangi sınıfa mensupsun?” Structural typing ilk soruyla, nominal typing ise ikinci soruyla ilgilenir. Bu ayrım yalnızca akademik bir sınıflandırma değildir; kodun yeniden kullanılabilirliğini, güvenliğini ve API tasarımını doğrudan etkiler.

``

## İki farklı kimlik anlayışı

**Structural typing**, bir değerin tipini sahip olduğu yapıya göre değerlendirir. Alanlar ve metotlar beklenen yapıyla uyuşuyorsa değerin nerede tanımlandığı önemli değildir. TypeScript, bu yaklaşımın en tanınmış örneklerinden biridir.

**Nominal typing** ise tip uyumluluğunu açık kimlik veya kalıtım ilişkileri üzerinden belirler. İki sınıf tamamen aynı üyeleri taşısa bile farklı isimlerle tanımlanmışlarsa otomatik olarak aynı tip kabul edilmezler. Java, C# ve C++ ağırlıklı olarak bu modeli kullanır.

Bunu matematiksel biçimde ifade edersek structural uyumluluk kabaca şöyle düşünülebilir:

$$
A \preceq B \iff \text{üyeler}(B) \subseteq \text{üyeler}(A)
$$

Yani `A`, `B` tarafından istenen bütün üyeleri sağlıyorsa `B` beklenen yerde kullanılabilir. İlginç biçimde daha fazla özelliğe sahip olmak çoğu zaman sorun değildir.

Nominal sistemdeyse ilişki daha çok şuna benzer:

$$
A \preceq B \iff A = B \;\lor\; A \text{, } B\text{'den türemiştir}
$$

Burada yalnızca benzemek yetmez; aile nüfusuna kayıtlı olmak gerekir.

## TypeScript: Neyi yapabildiğini göster

Aşağıdaki fonksiyon, `yaz` metoduna sahip herhangi bir değeri kabul eder:

```typescript
interface Yazici {
  yaz(metin: string): void;
}

class KonsolRobotu {
  yaz(metin: string): void {
    console.log(`Robot: ${metin}`);
  }

  sarjOl(): void {
    console.log("Şarj ediliyor...");
  }
}

function raporla(yazici: Yazici): void {
  yazici.yaz("Sistem hazır");
}

raporla(new KonsolRobotu());
```

`KonsolRobotu`, `Yazici` arayüzünü açıkça uyguladığını söylemez. Buna rağmen gerekli `yaz` metoduna sahip olduğu için uyumludur. `sarjOl` metodunun fazladan bulunması da çağrıyı bozmaz. Bu yaklaşım ördek testini hatırlatır: Ördek gibi yürüyüp ördek gibi ses çıkarıyorsa muhtemelen yeterince ördektir.

## Java: Rozetini göstermeden geçemezsin

Aynı düşünce Java'da açık bir ilişki gerektirir:

```java
interface Yazici {
    void yaz(String metin);
}

class KonsolRobotu implements Yazici {
    public void yaz(String metin) {
        System.out.println("Robot: " + metin);
    }
}
```

Sınıfın doğru imzaya sahip bir `yaz` metodu bulunması tek başına yeterli değildir. `implements Yazici` ifadesi, nominal kimliği oluşturur. Böylece geliştiricinin niyeti açıkça belgelenir ve tesadüfi benzerlikler uyumluluk sayılmaz.

## Hızlı karşılaştırma

| Özellik | Structural typing | Nominal typing |
|---|---|---|
| Temel soru | “Neyi yapabiliyorsun?” | “Hangi tipsin?” |
| Uyumluluk | Üye ve imza eşleşmesi | İsim, kalıtım veya uygulama ilişkisi |
| Esneklik | Yüksek | Daha kontrollü |
| Yeniden kullanım | Kolay ve örtük | Açık sözleşmelerle yapılır |
| Başlıca risk | Tesadüfi uyumluluk | Gereksiz sınıf ve adaptör yükü |
| Örnek diller | TypeScript, Go | Java, C#, Kotlin |

## Hangisi daha iyi?

Tek bir kazanan yoktur. Structural typing; küçük arayüzler, eklenti sistemleri, test doubles ve farklı kaynaklardan gelen veriler için oldukça pratiktir. Özellikle `oku()`, `yaz()` veya `kaydet()` gibi davranış odaklı sözleşmelerde düşük bağımlılık sağlar.

Nominal typing ise `KullaniciId`, `SiparisId` ve `Para` gibi yapısal olarak benzer fakat anlamsal olarak farklı değerleri ayırırken avantajlıdır. İki değerin ikisi de sayı olsa bile birbirinin yerine kullanılmasını istemeyebilirsiniz. Kimlik burada bürokrasi değil, güvenlik bariyeridir.

Kısacası structural typing yeteneğe, nominal typing aidiyete bakar. API'nizde önemli olan davranışsa yapısal yaklaşım; kavramsal kimlik ve açık niyetse nominal yaklaşım daha uygun olabilir. İyi tasarım, kapıdaki görevlinin hangi soruyu ne zaman sorması gerektiğini bilmektir.
