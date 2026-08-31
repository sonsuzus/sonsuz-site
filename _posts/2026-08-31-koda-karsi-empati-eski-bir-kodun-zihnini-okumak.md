---
layout: post
title: "Koda Karşı Empati: Eski Bir Kodun Zihnini Okumak"
math: true
categories: 
  - Bilgi
tags: 
  - temiz kod
  - theory of mind
  - yazılım psikolojisi
toc: true
---

Yıllar önce yazılmış karmaşık bir fonksiyonla karşılaştığınızda yalnızca değişkenleri ve koşulları çözmezsiniz. Görünmeyen bir geliştiricinin ne bildiğini, neden belirli risklerden kaçındığını ve hangi baskılar altında karar verdiğini de tahmin etmeye çalışırsınız. Başka insanların inanç ve niyetlerini modelleme becerisi psikolojide **zihin kuramı** (*theory of mind*) olarak adlandırılır. Eski kod okumak da biraz dijital arkeoloji, biraz dedektiflik ve şaşırtıcı ölçüde empati gerektirir.

``

## Kod yalnızca talimatlardan oluşmaz

Kaynak kod, bilgisayara verilen komutların yanında geçmiş kararların bıraktığı izleri taşır. Garip görünen bir `if`, artık bilinmeyen bir üretim hatasını engelliyor olabilir. Gereksiz sandığınız bir kopyalama işlemi, yıllar önce kullanılan bir kütüphanenin yan etkilerinden korunmak için eklenmiş olabilir.

Zihin kuramı burada üç soruyla devreye girer:

1. **Yazar ne biliyordu?** O dönemin gereksinimleri, araçları ve sistem sınırları nelerdi?
2. **Yazar neye inanıyordu?** Hangi girdilerin geleceğini veya hangi bileşenin güvenilmez olduğunu düşünüyordu?
3. **Yazar neyi amaçlıyordu?** Hız, güvenlik, teslim tarihi ya da geriye dönük uyumluluk mu öncelikliydi?

Okur, gözlemlediği koddan olası niyeti çıkarır. Bu süreç kabaca Bayesçi bir çıkarım gibi düşünülebilir:

$$
P(\text{niyet}\mid\text{kod}) \propto P(\text{kod}\mid\text{niyet})P(\text{niyet})
$$

Yani kodu gördükten sonra bir niyet tahmin ederiz; fakat tahminimiz geçmiş deneyimlerimizden gelen ön kabullere de bağlıdır. Performans sorunlarına alışkın biri her tuhaflığı optimizasyon, güvenlik uzmanı ise savunma mekanizması sanabilir.

## Yargılamak ile anlamaya çalışmak

| İlk tepki | Empatik yaklaşım |
|---|---|
| “Bunu neden böyle saçma yazmış?” | “Bu yapı hangi problemi önlüyor olabilir?” |
| “Hemen sadeleştireyim.” | “Davranışı testlerle güvenceye alayım.” |
| “Yazar dili bilmiyormuş.” | “Dönemin dil sürümü hangi imkânları sunuyordu?” |
| “Bu kontrol gereksiz.” | “Kontrolün kapsadığı eski bir uç durum var mı?” |

Empati, kötü kodu romantikleştirmek değildir. Amaç her satırı savunmak değil, değiştirmeden önce satırın var olma nedenini araştırmaktır. Çünkü anlaşılmadan yapılan “temizlik”, çalışan bir güvenlik ağını dekorasyon sanıp sökmeye benzeyebilir.

## Bir kod bloğunun niyetini okumak

Aşağıdaki JavaScript fonksiyonuna bakalım:

```javascript
function getUserName(user) {
  // Eski kayıtlarda profile bulunmayabilir.
  if (!user) return 'Misafir';
  if (!user.profile) return user.name || 'Misafir';
  return user.profile.displayName || user.name || 'Misafir';
}
```

İlk bakışta peş peşe kontroller dağınık görünebilir. Modern sözdizimiyle fonksiyon tek satıra indirilebilir:

```javascript
function getUserName(user) {
  return user?.profile?.displayName ?? user?.name ?? 'Misafir';
}
```

İkinci sürüm daha kısa olsa da doğru değişiklik olduğundan henüz emin değiliz. Eski çalışma ortamı optional chaining desteklemiyor olabilir. Ayrıca `||` ile `??` aynı davranışı göstermez: boş metin `||` için geçersiz, `??` için geçerli bir değerdir. Demek ki “sadeleştirme”, kullanıcı arayüzünde fark edilebilir bir davranış değişikliğine dönüşebilir.

Bu nedenle önce test yazar, sürüm geçmişini inceler ve mümkünse `git blame` ile ilgili değişikliğin bağlamına ulaşırız. Araç burada suçlu bulmak için değil, geçmişteki zihinsel modeli yeniden kurmak için kullanılır.

## Empatik kod okuma rutini

Karmaşık bir blokla karşılaştığınızda şu sırayı deneyin:

- Kodu değiştirmeden mevcut davranışı örneklerle kaydedin.
- Değişken adlarını değil, veri akışını takip edin.
- Hangi uç durumların özellikle ele alındığını listeleyin.
- Commit mesajları, hata kayıtları ve eski belgeleri inceleyin.
- “Ben olsaydım” yerine “Bu koşullarda biri neden?” diye sorun.
- Varsayımınızı testle doğrulamadan refaktör etmeyin.

Sonuçta bakım yapılabilir yazılım yalnızca makineler için doğru çalışan yazılım değildir; farklı zamanlarda yaşayan geliştiriciler arasında anlaşılabilir bir iletişimdir. Eski kodun zihnini okumaya çalışmak sabır kazandırır, aceleci refaktörleri azaltır ve bizim de gelecekte daha açıklayıcı kod yazmamızı sağlar. Bugünün gizemli geliştiricisi başkası olabilir; yarının gizemli geliştiricisi ise büyük ihtimalle biziz.
