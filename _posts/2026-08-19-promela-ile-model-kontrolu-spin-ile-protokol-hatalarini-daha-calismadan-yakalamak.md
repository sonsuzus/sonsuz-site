---
layout: post
title: "Promela ile Model Kontrolü: Spin ile Protokol Hatalarını Daha Çalışmadan Yakalamak"
math: true
categories: 
  - Bilgi
tags: 
  - Promela
  - Spin
  - Model Kontrolü
---

Dağıtık sistemlerde ve eşzamanlı programlarda hata çoğu zaman kodun tek bir satırında değil, olayların talihsiz sıralanışında saklanır. Bir istemci mesajı erken gönderir, sunucu zaman aşımına düşer, iki iş parçacığı aynı kaynağı bekler ve sistem sessizce kilitlenir. Promela (Process Meta Language) ile çalışan Spin model denetleyicisi, bu tür senaryoları rastgele test etmeye bırakmak yerine sistemin olası durumlarını sistematik biçimde tarar. Böylece protokolünüzü henüz üretime taşımadan mantıksal açıdan sorgulayabilirsiniz.

``

## Model kontrolü neyi farklı yapar?

Birim testleri belirlediğiniz örnek girdileri yürütür. Model kontrolü ise tanımladığınız modeldeki **tüm ulaşılabilir durumları** ve süreçler arası olası zamanlama sıralarını araştırır. Amaç, güvenlik ve canlılık özelliklerini doğrulamaktır.

- **Güvenlik (safety):** “Kötü bir şey asla olmaz.” Örneğin iki süreç aynı anda kritik bölgede bulunamaz.
- **Canlılık (liveness):** “İyi bir şey sonunda olur.” Örneğin istek gönderen bir istemci, uygun koşullarda sonunda yanıt alır.

Bir sistemin durum uzayı kabaca süreçlerin yerel durumları, paylaşılan değişkenler ve kanal içeriklerinin çarpımıdır. Basit bir sezgisel ifade ile:

$$|S| \approx \prod_{i=1}^{n}|L_i| \times |G| \times \prod_{j=1}^{m}|C_j|$$

Burada $L_i$ süreçlerin yerel durumlarını, $G$ ortak durumu, $C_j$ ise iletişim kanallarının olası içeriklerini temsil eder. Bu sayı hızla büyür; buna **durum uzayı patlaması** denir. Spin, kısmi sıralama indirgeme gibi tekniklerle gereksiz eşdeğer zamanlamaları azaltmaya çalışır.

| Yaklaşım | Temel soru | Güçlü yanı | Sınırı |
|---|---|---|---|
| Birim testi | Bu girdi doğru mu? | Hızlı ve uygulama odaklıdır | Yarış koşullarını kaçırabilir |
| Yük testi | Sistem yoğunlukta dayanıklı mı? | Performansı ölçer | Mantıksal doğruluk garantisi vermez |
| Spin ile model kontrolü | Her olası sıralamada özellik korunuyor mu? | Eşzamanlılık hatalarını bulur | Modelin doğru soyutlanması gerekir |

## Promela ile küçük bir karşılıklı dışlama modeli

Aşağıdaki örnekte iki süreç kritik bölgeye girmek ister. `in_cs` değişkeni, kritik bölgede kaç süreç olduğunu takip eder. `assert` ifadesi, bu sayının hiçbir zaman birden büyük olmaması gerektiğini söyler.

```promela
byte in_cs = 0;

proctype Worker() {
  do
  :: atomic {
       in_cs++;
       assert(in_cs == 1);
       /* kritik bölge */
       in_cs--
     }
  od
}

init {
  run Worker();
  run Worker();
}
```

Bu model ilk bakışta güvenlidir; çünkü artırma, kontrol ve azaltma `atomic` bloğunda tek adım gibi ele alınır. Ancak `atomic` ifadesini kaldırırsanız Spin, iki sürecin `in_cs++` işlemini art arda yapabildiği bir yürütme izi bulabilir. Bu iz, hatanın yalnızca “var olduğunu” değil, hangi işlem sırasıyla oluştuğunu da gösterir.

```bash
spin -a mutex.pml
cc -o pan pan.c
./pan -a
```

İlk komut Promela modelinden doğrulayıcı C kodu üretir. İkinci komut bunu derler; son komut ise tüm durum uzayını tarar. Hata bulunduğunda Spin, tekrar oynatılabilir bir trail dosyası üretir. `spin -t mutex.pml` ile karşı örneği adım adım inceleyebilirsiniz.

## Kanallar, doğrulamalar ve LTL

Promela’da süreçler çoğunlukla kanallar üzerinden haberleşir. `chan q = [1] of { byte };` tanımı, bir elemanlık tamponlu bir mesaj kuyruğu oluşturur. Sıfır kapasiteli kanallar ise gönderen ve alıcının aynı anda buluşmasını gerektiren senkron iletişim sunar.

Zamansal özellikleri LTL ile ifade edebilirsiniz. Örneğin `request` olduktan sonra sonunda `grant` olmasını istemek için:

$$\Box(request \rightarrow \Diamond grant)$$

Spin sözdiziminde bu fikir şöyle yazılabilir:

```promela
ltl eventually_granted { [] (request -> <> grant) }
```

Bu ifade, her isteğin gelecekte bir izinle sonuçlanmasını bekler. Elbette modelde sonsuza kadar beklemeye yol açan bir zamanlama varsa Spin bunu canlılık ihlali olarak raporlayabilir.

Başarılı bir Promela modeli, üretim kodunun kopyası değildir; onun davranışsal özeti olmalıdır. Mesaj türlerini, durum geçişlerini, tampon sınırlarını ve hata senaryolarını modelleyin; ayrıntılı veri işleme mantığını soyutlayın. Önce güvenlik özelliklerini `assert` ile kurun, ardından LTL ile ilerleme beklentilerini ekleyin. Spin’in verdiği karşı örnekleri bir başarısızlık değil, protokol tasarımınızın ücretsiz dedektif raporu olarak görün.
