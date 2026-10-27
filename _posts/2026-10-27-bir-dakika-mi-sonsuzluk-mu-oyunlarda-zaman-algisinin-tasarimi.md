---
layout: post
title: "Bir Dakika mı, Sonsuzluk mu? Oyunlarda Zaman Algısının Tasarımı"
math: true
categories: 
  - Bilgi
tags: 
  - oyun tasarımı
  - kullanıcı deneyimi
  - zaman algısı
  - yükleme ekranları
  - oyuncu psikolojisi
  - game development
toc: true
image: /img/bir-dakika-mi-15.png
---

Bir oyunda geçen 30 saniye her zaman 30 saniye gibi hissedilmez. Çatışmanın ortasında göz açıp kapayıncaya kadar geçen bu süre, boş bir yükleme ekranında küçük bir sonsuzluğa dönüşebilir. Çünkü oyuncunun sabrı yalnızca kronometreyle değil; dikkat, beklenti, kontrol hissi ve sunulan geri bildirimle yönetilir. İyi oyun tasarımı zamanı hızlandıramasa bile beynin onu nasıl yorumladığını ustalıkla değiştirebilir.


![bir-dakika-mi-15](/img/bir-dakika-mi-15.svg)

``

## Fiziksel zaman ve algılanan zaman

Fiziksel zaman ölçülebilirken algılanan zaman öznel bir deneyimdir. Bunu basitleştirilmiş bir modelle şöyle ifade edebiliriz:

$$T_a = T_g \times \frac{B + D}{E + K}$$

Burada $T_a$ algılanan zamanı, $T_g$ gerçek süreyi, $B$ belirsizliği, $D$ dikkatin beklemeye yönelmesini, $E$ eğlenceyi ve $K$ kontrol hissini temsil eder. Bu bilimsel bir ölçüm formülü değil, tasarım kararlarını düşünmek için kullanışlı bir modeldir. Belirsizlik ve beklemeye odaklanma arttıkça süre uzamış gibi hissedilir. Eğlence ve kontrol hissi yükseldiğinde ise aynı süre daha kısa algılanır.

Örneğin yüzde göstergesi bulunmayan donmuş bir ekran, oyuncuya sistemin çalışıp çalışmadığını düşündürür. Belirsizlik yükselir ve oyuncu her saniyeyi izlemeye başlar. Hareketli bir ipucu, ilerleme çubuğu veya etkileşimli mini oyun ise dikkati dağıtır.

| Bekleme tasarımı | Oyuncunun düşüncesi | Algılanan etki |
|---|---|---|
| Boş ve hareketsiz ekran | “Oyun çöktü mü?” | Süre çok uzun gelir |
| İlerleme çubuğu | “Ne kadar kaldığını biliyorum.” | Belirsizlik azalır |
| Oynanış ipuçları | “Bu bilgiyi kullanabilirim.” | Bekleme faydalı görünür |
| Etkileşimli animasyon | “Hâlâ bir şey yapıyorum.” | Kontrol hissi artar |
| Gizli yükleme koridoru | “Dünyada ilerliyorum.” | Yükleme fark edilmez |

## İlerleme çubuğunun küçük oyunları

İlerleme çubukları her zaman yüklemenin gerçek hızını birebir göstermez. Dosyaların boyutu, disk hızı ve ağ gecikmesi değişken olduğu için doğrusal ilerleme üretmek zordur. Çubuğun uzun süre yüzde 99’da kalması özellikle sinir bozucudur; çünkü arayüz, bitiş sözü vermiş gibi görünür.

Daha dengeli bir gösterge için ölçülen ilerleme doğrudan ekrana verilmek yerine yumuşatılabilir:

$$P_{yeni} = P_{eski} + \alpha(P_{gerçek} - P_{eski})$$

$\alpha$ değeri 0 ile 1 arasındadır. Küçük değerler daha akıcı fakat daha yavaş tepki veren bir animasyon oluşturur. Aşağıdaki JavaScript örneği ani sıçramaları azaltır:

```javascript
let displayedProgress = 0;

function updateLoading(realProgress) {
  const smoothing = 0.12;
  displayedProgress +=
    smoothing * (realProgress - displayedProgress);

  const percent = Math.floor(displayedProgress * 100);
  document.querySelector(".progress-bar").style.width = `${percent}%`;
  document.querySelector(".progress-label").textContent = `${percent}%`;
}
```

Kod, gerçek yükleme oranına bir anda atlamak yerine ona kademeli biçimde yaklaşır. Ancak gösterge kullanıcıyı kandırmamalıdır. Gerçek işlem tamamlanmadan yüzde 100 göstermek, kısa vadede hızlı görünse de güven kaybına yol açabilir.

## Beklemeyi oynanışa dönüştürmek

Bazı oyunlar yüklemeyi dar geçitler, asansör yolculukları veya yavaş açılan kapılar içine saklar. Oyuncu hareket etmeye devam ettiği için teknik bekleme, kurgu dünyasının parçası olur. Buna karşılık aynı numara çok sık kullanılırsa oyuncular “Bu asansör aslında yükleme ekranı” diyerek perdenin arkasını görmeye başlar.

Respawn süreleri de bilinçli biçimde tasarlanır. Anında yeniden doğmak cezayı anlamsızlaştırabilir; aşırı uzun beklemek ise öfke yaratır. Takım oyunlarında bekleme süresi, oyuncuya haritayı izleme ve strateji kurma fırsatı veriyorsa pasif ceza olmaktan çıkar.

Başarılı zaman manipülasyonunun amacı oyuncuyu aldatmak değil, beklemeyi anlaşılır ve tahmin edilebilir kılmaktır. Geri bildirim verin, belirsizliği azaltın, mümkünse küçük bir kontrol alanı sunun. Saat aynı hızda ilerlese de oyuncunun zihnindeki kronometre böylece çok daha insaflı çalışır.
