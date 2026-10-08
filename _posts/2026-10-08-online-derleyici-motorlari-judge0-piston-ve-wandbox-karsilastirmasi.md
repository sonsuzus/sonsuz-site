---
layout: post
title: "Online Derleyici Motorları: Judge0, Piston ve Wandbox Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - online derleyici
  - judge0
  - piston
  - wandbox
  - api
  - sandbox
  - programlama
toc: true
image: /img/online-derleyici-motorlari-70.png
---

Tarayıcıya birkaç satır kod yazıp saniyeler içinde sonucu görmek basit bir sihir numarası gibi görünür. Oysa perdenin arkasında derleyiciler, işlem kuyrukları, güvenlik katmanları ve kaynak sınırlamaları çalışır. Judge0, Piston ve Wandbox bu işi farklı önceliklerle çözen üç popüler sistemdir. Gelin kodlarımızın sunucuda çıktığı bu kısa ama maceralı yolculuğu inceleyelim.

``

## Online derleyici nasıl çalışır?

Bir online derleyici temel olarak kaynak kodunu ve kullanıcı girdisini alır, uygun çalışma ortamını seçer ve işlemi yalıtılmış bir alanda yürütür. Derlenen dillerde süreç genellikle şu şekildedir:

$$T_{toplam} = T_{kuyruk} + T_{derleme} + T_{çalıştırma} + T_{iletişim}$$

Python gibi yorumlanan dillerde derleme adımı görünür olmayabilir; ancak ortam hazırlama ve süreç başlatma maliyeti devam eder. Sistem, çalıştırma sonunda standart çıktıyı, standart hatayı, durum kodunu, süreyi ve bellek tüketimini döndürür.

Yalıtım kritik önemdedir. Kullanıcının gönderdiği kod sonsuz döngüye girebilir, dosya sistemini kurcalayabilir veya bir fork bombası başlatmayı deneyebilir. Bu nedenle container, namespace, cgroup, seccomp ve ayrıcalıksız kullanıcı gibi mekanizmalar kullanılır. Basitleştirilmiş bir kaynak koşulu şöyledir:

$$CPU \leq C_{maks}, \quad RAM \leq M_{maks}, \quad T \leq T_{maks}$$

Bu sınırlardan biri aşılırsa çalıştırma sonlandırılır. Kısacası sistem yalnızca kodu çalıştırmaz; ona güvenli bir oyun alanı da çizer.

## Üç sistemin karakteri

| Özellik | Judge0 | Piston | Wandbox |
|---|---|---|---|
| Ana yaklaşım | Kod değerlendirme API'si | Hafif çalıştırma motoru | Çok sürümlü derleyici servisi |
| Uygun kullanım | Yarışma, ödev, test platformu | Editör, bot, küçük servis | Derleyici ve sürüm denemeleri |
| Kendi sunucuna kurulum | Güçlü ve yaygın seçenek | Görece sade | Mümkün, ancak daha özel amaçlı |
| Sonuç modeli | Durum ve kaynak ölçümleri ayrıntılı | Basit çalıştırma sonucu | Derleyici seçenekleri ayrıntılı |
| Öne çıkan yön | Kuyruk ve değerlendirme mantığı | Temiz API ve pratiklik | Derleyici sürümü çeşitliliği |

![online-derleyici-motorlari-70](/img/online-derleyici-motorlari-70.svg)


### Judge0

Judge0, özellikle otomatik değerlendirme sistemlerine yakışır. Bir gönderim oluşturur, dil kimliğini, kaynak kodunu ve girdiyi iletirsiniz. Sonucu eşzamanlı alabilir veya daha ölçeklenebilir biçimde bir token üzerinden sorgulayabilirsiniz. Zaman ve bellek sınırları, derleme çıktısı ve çalışma durumu gibi alanlar eğitim platformları için oldukça değerlidir.

### Piston

Piston, farklı dillerde kod çalıştırmayı anlaşılır bir HTTP API arkasında toplar. Dil paketleri ve sürümleri yönetilebilir; bu da onu web tabanlı editörler, Discord botları veya hızlı prototipler için çekici yapar. Judge0 kadar yarışma odaklı bir değerlendirme modeli sunmak yerine, “kodu ver, çıktıyı al” deneyimine yaklaşır.

Aşağıdaki JavaScript örneği, Piston uyumlu bir uç noktaya Python kodu gönderir:

```javascript
const response = await fetch("https://example.com/api/v2/execute", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    language: "python",
    version: "3.x",
    files: [{ content: "print(sum([4, 8, 15, 16, 23, 42]))" }]
  })
});

const result = await response.json();
console.log(result.run.stdout);
```

Kod, çalıştırılacak dosyayı JSON gövdesine yerleştirir ve dönen standart çıktıyı gösterir. Gerçek sürüm değeri ile uç nokta, kullandığınız Piston kurulumundan sorgulanmalıdır.

### Wandbox

Wandbox özellikle C++ dünyasında farklı derleyicileri, sürümleri ve bayrakları karşılaştırırken parlar. Aynı kodu GCC ve Clang ile deneyip standart sürümünü değiştirmek, taşınabilirlik sorunlarını yakalamayı kolaylaştırır. Bu nedenle klasik bir sınav motorundan çok etkileşimli bir derleyici laboratuvarına benzer.

## Hangisini seçmelisiniz?

Otomatik puanlama, test senaryoları ve ayrıntılı durum yönetimi istiyorsanız Judge0 güçlü adaydır. Küçük ve anlaşılır bir kod çalıştırma servisi arıyorsanız Piston daha rahat hissettirebilir. Derleyici sürümleri ve bayraklarla deney yapacaksanız Wandbox öne çıkar.

Hangi sistemi seçerseniz seçin API'yi doğrudan sınırsız biçimde internete açmayın. Kimlik doğrulama, istek kotası, çıktı boyutu sınırı, zaman aşımı ve düzenli imaj güncellemeleri ekleyin. Çünkü online derleyicide en zor soru “Kod çalıştı mı?” değil, “Kod çalışırken sunucu hâlâ güvende mi?” sorusudur.
