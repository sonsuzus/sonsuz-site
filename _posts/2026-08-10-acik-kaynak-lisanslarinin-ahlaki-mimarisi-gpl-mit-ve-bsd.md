---
layout: post
title: "Açık Kaynak Lisanslarının Ahlaki Mimarisi: GPL, MIT ve BSD"
math: true
categories: 
  - Bilgi
tags: 
  - açık kaynak
  - gpl
  - mıt lisansı
  - bsd lisansı
  - yazılım hukuku
toc: true
---

Bir depoyu herkese açık yapmak, kodu ahlaki olarak “sahipsiz” ilan etmek değildir. Açık kaynak lisansları, üreticinin emeği ile topluluğun yeniden kullanma hakkı arasında kurulan sosyal sözleşmelerdir. GPL, MIT ve BSD aynı kaynak koduna erişim fikrini paylaşsa da özgürlüğün ne anlama geldiği konusunda farklı bir mimari önerir: Özgürlük, sonraki kullanıcıya garanti edilen bir hak mıdır; yoksa ilk kullanıcının olabildiğince az engelle karşılaşması mı?

``

Bu ayrımı anlamak için iki eksenli bir model kurabiliriz. Bir eksende yeniden kullanım serbestliği, diğerinde türev eserin kaynak kodunu paylaşma zorunluluğu bulunur. Basitleştirilmiş biçimde lisansın “koruyuculuk” düzeyini şöyle düşünebiliriz:

$$K = S - R$$

Burada $S$, paylaşım zorunluluğunu; $R$ ise kapalı kaynaklı yeniden kullanım serbestliğini temsil eder. Bu hukuki bir formül değil, zihinsel bir pusuladır. GPL’de $S$ yüksektir; MIT ve BSD’de ise $R$ belirgin biçimde yüksektir. Dolayısıyla lisans seçimi yalnızca teknik değil, ürünün gelecekte kimlere ve hangi koşullarla hizmet edeceğine ilişkin etik bir karardır.

## GPL: Özgürlüğü Zincirleme Koruyan Yaklaşım

GNU General Public License (GPL), **copyleft** fikrinin en bilinen temsilcisidir. Temel vaadi şudur: Bir kişi GPL’li kodu dağıtır, değiştirir veya türev bir çalışmanın parçası olarak sunarsa, ilgili türevi de GPL koşullarıyla kaynak koduyla birlikte paylaşmalıdır. Bu yaklaşım, özgürlüğün sadece ilk indiren kişiye değil, sonraki tüm kullanıcılara ulaşmasını hedefler.

GPL’nin ahlaki sezgisi güçlüdür: Topluluktan alınan değer, topluluğa geri dönmelidir. Ancak bu geri dönüş şartı bazı şirketler için ticari entegrasyon maliyeti yaratabilir. Özellikle kendi ürününün kaynak kodunu açmak istemeyen bir firma, GPL bileşenini doğrudan kullanmaktan kaçınabilir. Buradaki sınır, salt “kod kullandım” cümlesinden daha karmaşıktır; bağlama, dağıtıma ve türev eser ilişkisinin niteliğine göre değerlendirme gerekebilir.

## MIT ve BSD: İzin Odaklı Özgürlük

MIT lisansı kısa, anlaşılır ve izin verici bir lisans modelidir. Kodu kullanma, değiştirme, birleştirme, satma ve kapalı kaynaklı ürünlerde dağıtma hakkı verir; temel şart genellikle telif ve lisans bildirimini korumaktır. BSD lisansları da benzer bir ailede yer alır. Özellikle 2 maddeli BSD, MIT’e çok yakın bir serbestlik sunar; 3 maddeli BSD ise proje veya katkıcı adlarının izinsiz reklam amacıyla kullanılmasını engeller.

Bu lisansların ahlaki tezi farklıdır: En büyük kamusal fayda, kodun mümkün olan en geniş alanda dolaşıma girmesiyle doğar. Bir şirket kodu kapalı bir ürüne dönüştürse bile teknoloji yayılır, bakım bütçesi oluşabilir ve ekosistem büyüyebilir. Eleştiri ise açıktır: Topluluğun ürettiği değer, hiçbir geri paylaşım olmadan özel bir ürüne dönüşebilir.

| Ölçüt | GPL | MIT | BSD (2/3 maddeli) |
|---|---|---|---|
| Kaynak kodunu kullanma | Serbest | Serbest | Serbest |
| Türev dağıtımda kaynak paylaşımı | Genellikle zorunlu | Zorunlu değil | Zorunlu değil |
| Kapalı kaynak ürünle kullanım | Sınırlı/koşullu | Uygun | Uygun |
| Lisans bildirimi | Korunmalı | Korunmalı | Korunmalı |
| Ana etik vurgu | Kalıcı özgürlük | Maksimum benimsenme | Esnek yeniden kullanım |

Bir projeye lisans dosyası eklemek teknik olarak basittir; fakat metni değiştirmek ya da rastgele bir lisans etiketi yazmak doğru değildir. Örneğin MIT lisansı kullanan bir Node.js paketinde bildirimi paketle birlikte taşımak gerekir:

```json
{
  "name": "ornek-arac",
  "version": "1.0.0",
  "license": "MIT",
  "files": ["dist", "LICENSE"]
}
```

Bu yapı, paketin dağıtımına `LICENSE` dosyasını dahil ederek kullanıcıların hangi haklara sahip olduğunu görünür kılar. `package.json` içindeki alan tek başına lisans metninin yerini tutmaz; bir işaret levhasıdır, sözleşmenin tamamı değildir.

## Sınır Nerede Başlar?

Doğru lisans, “en özgür” olan değil, projenin vermek istediği sözü en dürüst biçimde taşıyandır. Katkıların kapalı ürünlere akmasını sorun etmiyorsanız MIT veya BSD mantıklıdır. Kodun her türevde kamusal kalmasını istiyorsanız GPL daha tutarlı bir tercihtir. Ayrıca bağımlılıkların lisanslarını, şirket politikalarını ve dağıtım biçimini incelemek gerekir. Lisans seçimi bir rozet değil; başkalarının emeğinizle ne yapabileceğini, sizin de onların emeğine karşı hangi sorumluluğu üstlendiğinizi belirleyen mimari bir karardır.
