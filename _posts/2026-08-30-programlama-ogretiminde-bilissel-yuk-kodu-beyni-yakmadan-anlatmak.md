---
layout: post
title: "Programlama Öğretiminde Bilişsel Yük: Kodu Beyni Yakmadan Anlatmak"
math: true
categories: 
  - Bilgi
tags: 
  - programlama eğitimi
  - bilişsel yük teorisi
  - öğretim tasarımı
---

Bir öğrenciye `for` döngüsünü anlatırken aynı anda değişken türleri, sayaç mantığı, koşullar, süslü parantezler ve hata mesajlarıyla saldırmak, iyi niyetli bir öğretim kazasına dönüşebilir. Öğrenci konuyu “anlamıyor” değildir; çoğu zaman çalışma belleği dolmuştur. Bilişsel Yük Teorisi, programlama eğitiminde bilgiyi küçük, anlamlı ve yönetilebilir parçalar hâlinde sunarak bu tıkanmayı azaltmamıza yardım eder.

``

Bilişsel Yük Teorisi, çalışma belleğinin kapasitesinin sınırlı olduğu fikrine dayanır. Öğrenci yeni bir kod parçasını incelerken hem sözdizimini hem problem çözme adımlarını hem de önceki bilgilerini zihninde tutmaya çalışır. Toplam zihinsel yük kabaca şöyle düşünülebilir:

$$Y_{toplam} = Y_{içsel} + Y_{dışsal} + Y_{yararlı}$$

Burada **içsel yük**, konunun doğal karmaşıklığıdır: iç içe döngüler gerçekten tek bir `if` ifadesinden daha zordur. **Dışsal yük**, öğretimin gereksiz zorluğudur: dağınık slaytlar, açıklamasız kod veya aynı anda beş yeni kavram. **Yararlı yük** ise öğrencinin şema kurmak için harcadığı verimli zihinsel çabadır. Hedef, içsel yükü adımlara bölmek, dışsal yükü azaltmak ve yararlı yükü artırmaktır.

| Öğretim yaklaşımı | Çalışma belleğine etkisi | Daha iyi alternatif |
|---|---:|---|
| Tam uygulamayı bir anda göstermek | Çok yüksek | Önce tek fonksiyon, sonra birleşim |
| Kodla açıklamayı farklı yerlerde vermek | Gereksiz arama maliyeti | Açıklamayı ilgili satırın yanına koymak |
| “Deneyin bakalım” diye başlamak | Acemide belirsizlik yaratır | Önce çözümlü örnek sunmak |
| Her örnekte farklı isimlendirme kullanmak | Şema oluşumunu yavaşlatır | Tutarlı değişken isimleri kullanmak |

İlk güçlü yöntem **parçalama**dır. Örneğin öğrenciden doğrudan “listedeki çift sayıların toplamını bulan program” yazmasını istemek yerine görevi mikro hedeflere ayırın: listeyi tanı, bir elemanı oku, çiftlik kontrolü yap, toplam değişkenini güncelle. Her adım, önceki adımın üstüne yerleşir. Bu yaklaşım, bilişsel yükü azaltırken öğrencinin “kod büyüsü” yerine neden-sonuç ilişkisi kurmasını sağlar.

```python
sayilar = [3, 8, 5, 12]
toplam = 0

for sayi in sayilar:
    if sayi % 2 == 0:
        toplam = toplam + sayi

print(toplam)
```

Bu örneği tek seferde açıklamak yerine bir **kod izleme tablosu** kullanın. Öğrenci, programın zaman içindeki durumunu görür; özellikle değişken güncellemeleri soyut olmaktan çıkar.

| Tur | `sayi` | Çift mi? | `toplam` |
|---:|---:|---|---:|
| Başlangıç | - | - | 0 |
| 1 | 3 | Hayır | 0 |
| 2 | 8 | Evet | 8 |
| 3 | 5 | Hayır | 8 |
| 4 | 12 | Evet | 20 |

İkinci yöntem, **çözümlü örnekten kademeli bağımsızlığa** geçmektir. Başlangıç seviyesinde boş ekrana bakıp algoritma üretmek pahalıdır. Önce öğretmen çalışan çözümü sesli düşünerek açıklar: “`toplam` neden sıfırdan başlıyor? Çünkü birikim için nötr değer gerekiyor.” Ardından bazı satırlar boş bırakılır. Son aşamada öğrenci benzer problemi tek başına çözer. Buna örnek soldurma denir.

```python
# Aşama 1: Öğrenci yalnızca koşulu tamamlar
for sayi in sayilar:
    if ________:
        toplam += sayi
```

Üçüncü yöntem **ön bilgi aktivasyonu**dur. Yeni bir yapı tanıtmadan önce gereken mini bilgileri hatırlatın. Fonksiyon anlatmadan önce parametre, dönüş değeri ve değişken kapsamını aynı derste uzun uzun öğretmeyin. Önce bu kavramları kısa, ayrı örneklerle oturtun; sonra fonksiyonda birleştirin. Öğrencinin zihninde oluşan şemalar, sonraki problemlerde yükü dramatik biçimde düşürür.

Son olarak hata ayıklamayı da dozlayın. Başlangıçta sözdizimi hatası, mantık hatası ve çalışma zamanı hatasını aynı örnekte karıştırmak yerine tek hata türüne odaklanın. İyi programlama öğretimi, en çok kodu gösteren değil; öğrencinin her anda **hangi fikre odaklanacağını** en iyi seçen öğretimdir.
