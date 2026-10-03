---
layout: post
title: "Bilgi İstifçiliği: Yer İmlerinden Gerçek Öğrenmeye"
math: true
categories: 
  - Bilgi
tags: 
  - bilgi istifçiliği
  - fomo
  - yazılım öğrenme
  - üretkenlik
  - teknik makale
  - öğrenme psikolojisi
toc: true
image: /img/bilgi-istifciligi-yer-75.png
---

![bilgi-istifciligi-yer-75](/img/bilgi-istifciligi-yer-75.svg)


Tarayıcınızın yer imleri klasörü küçük çaplı bir yazılım üniversitesine mi dönüştü? React performansı, Kubernetes, yapay zekâ, sistem tasarımı ve adını henüz telaffuz edemediğiniz üç JavaScript çatısı… Hepsi özenle kaydedilmiş, fakat hiçbiri uygulanmamış olabilir. Bilgi çağında teknik içerik biriktirmek, öğrenmeye benzeyen fakat çoğu zaman öğrenme üretmeyen rahatlatıcı bir alışkanlıktır.
``

## Yer imi neden öğrenilmiş gibi hissettirir?

Bir makaleyi kaydettiğimizde beynimiz içeriğe yeniden ulaşabileceğimizi bilir. Bu erişilebilirlik, bilgiyi gerçekten kavradığımız yanılgısını doğurur. Psikolojide buna bilişsel akıcılıkla ilişkili bir **aşinalık yanılsaması** diyebiliriz: Başlığı tanımak, fikri açıklayabilmekle karıştırılır.

FOMO, yani gelişmeleri kaçırma korkusu, bu döngüyü güçlendirir. Yazılım dünyasında her gün yeni bir araç yayımlandığı için geliştirici şöyle düşünür: “Şimdi okuyamam ama sonra kesin lazım olur.” Yer imi düğmesine basmak kaygıyı geçici olarak azaltır. Ancak “sonra”, çoğunlukla yeni içeriklerin geldiği başka bir gündür.

Gerçek öğrenmeyi basitçe şöyle modelleyebiliriz:

$$L = I \times U \times G$$

Burada $I$ incelenen bilgiyi, $U$ uygulama oranını, $G$ ise geri çağırma ve gözden geçirmeyi temsil eder. Yüz makale kaydedip hiçbirini uygulamazsak $U=0$ olur; dolayısıyla öğrenme çıktısı da yaklaşık olarak $L=0$ kalır. Acımasız ama yer imi klasörünüz kadar dürüst bir denklem!

| Davranış | Yarattığı his | Gerçek öğrenme etkisi |
|---|---|---|
| Makaleyi kaydetmek | Hazırlıklı olma | Çok düşük |
| Hızla göz gezdirmek | Konuya hâkim olma | Düşük |
| Not alarak okumak | Kavrama | Orta |
| Örneği değiştirmek | Aktif öğrenme | Yüksek |
| Sıfırdan proje yapmak | Yetkinlik geliştirme | Çok yüksek |

## Tüketimden üretime geçiş

Bir tutorial’ın değeri, okunan paragraf sayısıyla değil, klavyede alınan kararlarla ortaya çıkar. Örneğin Docker hakkında beş yazı kaydetmek yerine bir uygulamayı konteynerleştirmek daha öğreticidir. Çünkü uygulama sırasında belirsizliklerle karşılaşır, hata mesajlarını yorumlar ve zihinsel modelinizi sınarsınız.

Kullanışlı bir yöntem **1-1-1 kuralıdır**:

1. Bir teknik içerik seç.
2. İçerikten bir fikri kendi örneğinle uygula.
3. Öğrendiğini bir paragrafla anlat.

Ayrıca yer imlerini görünür hâle getirerek istifçiliği ölçebilirsiniz. Aşağıdaki Python kodu, dışa aktardığınız yer imi HTML dosyasındaki bağlantıları sayar:

```python
from pathlib import Path
from bs4 import BeautifulSoup

file_path = Path('bookmarks.html')
html = file_path.read_text(encoding='utf-8')
soup = BeautifulSoup(html, 'html.parser')

links = soup.find_all('a')
print(f'Toplam bağlantı: {len(links)}')

for link in links[:10]:
    print('-', link.get_text(strip=True), link.get('href'))
```

Kod, `BeautifulSoup` ile bağlantı etiketlerini bulur, toplamı gösterir ve ilk on kaydı listeler. Amaç yalnızca sayı üretmek değil; koleksiyonunuzun gerçek boyutuyla yüzleşmektir. Çalıştırmak için `pip install beautifulsoup4` komutuyla gerekli paketi kurabilirsiniz.

## Küçük bir bilgi diyeti

Her hafta yalnızca üç teknik içerik seçin. Okumadan önce “Bunu hangi problem için kullanacağım?” sorusunu sorun. Net bir cevabınız yoksa içeriği kaydetmeyin. Okuduğunuz materyal için kısa bir not, çalışan bir kod örneği veya küçük bir Git deposu üretin.

Yer imlerine de son kullanma tarihi koyabilirsiniz: Otuz gün içinde açılmayan bağlantı otomatik olarak silinmeye adaydır. Çünkü ihtiyaç duyduğunuz bilgiye ileride yeniden erişebilirsiniz; internetteki son Kubernetes makalesini kurtarmak sizin göreviniz değildir.

Bilgi istifçiliğinin panzehiri daha hızlı okumak değil, daha az içerikle daha derin çalışmaktır. Bir fikri uygulamak, on makaleyi kaydetmekten değerlidir. Bir hatayı çözmek ise yüz başlığı tanımaktan daha kalıcıdır. Yer imi klasörünüzü müze olmaktan çıkarın; onu deneylerin başladığı küçük bir atölyeye dönüştürün.
