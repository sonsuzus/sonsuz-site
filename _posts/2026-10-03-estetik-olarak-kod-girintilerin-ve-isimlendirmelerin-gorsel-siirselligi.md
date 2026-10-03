---
layout: post
title: "Estetik Olarak Kod: Girintilerin ve İsimlendirmelerin Görsel Şiirselliği"
math: true
categories: 
  - Bilgi
tags: 
  - temiz kod
  - girintileme
  - isimlendirme
  - okunabilirlik
  - yazılım geliştirme
  - kod estetiği
toc: true
image: /img/estetik-olarak-kod-17.png
---

İyi yazılmış bir kod parçasına bakmak, düzenli raflarla çevrili sakin bir kütüphaneye girmek gibidir. Girintiler mantıksal sınırları görünür kılar, anlamlı isimler zihnimizde hızlıca imgeler oluşturur ve tutarlı biçimlendirme gözün metin üzerinde zahmetsizce ilerlemesini sağlar. Kod böylece yalnızca bilgisayara verilen talimatlar olmaktan çıkar; geliştiriciler arasında okunan, yorumlanan ve hatta estetik haz uyandıran görsel bir dile dönüşür.
``
## Beyin Önce Şekli Görür

İnsan beyni kodu karakter karakter çözmez. Önce genel şekli, tekrarları, boşlukları ve blok sınırlarını algılar. Gestalt psikolojisindeki **yakınlık ilkesi**, birbirine yakın nesneleri aynı grubun parçaları olarak değerlendirdiğimizi söyler. Girintileme de tam olarak bundan yararlanır: Aynı seviyedeki satırlar, ortak bir davranış grubuna aitmiş gibi görünür.

Okuma sırasında harcadığımız zihinsel çabayı basitçe şöyle düşünebiliriz:

$$Y = K + B + A$$

Burada $Y$ toplam zihinsel yükü, $K$ kodun gerçek karmaşıklığını, $B$ biçimlendirmeyi çözme maliyetini ve $A$ anlam belirsizliğini temsil eder. Algoritmanın karmaşıklığını her zaman azaltamayabiliriz; ancak düzenli girintilerle $B$ değerini, açıklayıcı isimlerle de $A$ değerini küçültebiliriz.

## Girinti: Kodun Ritmi

Girinti yalnızca stil kuralı değildir; kontrol akışının görsel haritasıdır. Aşağıdaki dağınık örnek çalışabilir, fakat okuyucuyu gereksiz bir dedektiflik görevine çıkarır:

```python
def siparis_hazirla(siparis):
 if siparis:
  if siparis.odendi:
   return "Hazırlanıyor"
 return "İşlem yapılamadı"
```

Tutarlı dört boşluk, erken dönüş ve açık koşullar aynı davranışı daha sakin bir kompozisyona dönüştürür:

```python
def siparis_hazirla(siparis):
    if not siparis:
        return "İşlem yapılamadı"

    if not siparis.odendi:
        return "İşlem yapılamadı"

    return "Hazırlanıyor"
```

İkinci sürümde göz, blokların nerede başlayıp bittiğini anında yakalar. Boş satır da burada sessizlik işlevi görür: Müzikteki es gibi, iki düşünce arasına nefes alanı bırakır.

## İsimler Kodun Sözcükleridir

`x`, `tmp` veya `data2` gibi isimler kısa olabilir; ancak okuyucunun sürekli çeviri yapmasına neden olur. `aktif_kullanici_sayisi` ise değerin hem içeriğini hem amacını açıklar. İyi isimlendirme, yoruma duyulan ihtiyacı da azaltır.

| Belirsiz isim | Açık isim | Uyandırdığı soru |
|---|---|---|
| `d` | `gecen_gun_sayisi` | Birim nedir? |
| `liste` | `bekleyen_siparisler` | Hangi öğeler var? |
| `kontrol()` | `stok_yeterli_mi()` | Ne kontrol ediliyor? |
| `sonuc` | `toplam_indirim` | Hangi işlem bitti? |

![estetik-olarak-kod-17](/img/estetik-olarak-kod-17.svg)


İsim uzunluğu ile açıklık arasında denge gerekir. Amaç en uzun adı üretmek değil, bağlamı en az zihinsel sürtünmeyle aktarmaktır. Bunu kabaca $V = A / U$ şeklinde ifade edebiliriz: $V$ ismin verimliliği, $A$ aktardığı anlam, $U$ ise okumak için gereken uğraştır.

## Tutarlılık Neden Güzel Görünür?

Beyin örüntüleri sever. Bir projede fonksiyonlar aynı mantıkla adlandırıldığında, girintiler değişmediğinde ve benzer işlemler benzer biçimde yazıldığında sonraki satır tahmin edilebilir hâle gelir.

| Tutarlı kod | Tutarsız kod |
|---|---|
| Hızlı taranır | Satır satır çözümlenir |
| Hatalar şekil bozukluğu gibi fark edilir | Hatalar gürültü içinde saklanır |
| Güven hissi verir | Tereddüt oluşturur |
| Ekip dilini güçlendirir | Kişisel alışkanlıkları çarpıştırır |

Biçimlendiriciler bu nedenle yalnızca kozmetik araçlar değildir. Prettier, Black veya gofmt gibi araçlar estetik tartışmaları otomatikleştirerek ekibin enerjisini asıl probleme yöneltir.

Sonuçta güzel kod, süslü kod değildir. Güzel kod; niyetini saklamayan, boşluğu bilinçli kullanan ve okuyucusunun zihnine saygı gösteren koddur. Derleyici girintilere kayıtsız kalabilir, fakat kodu bakım yapan insan okur. Bir fonksiyon tek bakışta anlaşılabiliyorsa, orada mühendislikle sanat kısa süreliğine aynı satırda buluşmuş demektir.
