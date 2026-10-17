---
layout: post
title: "Python Import Tuzakları: Modül Düzeyindeki Kodun Gizli Yan Etkileri"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - import
  - modül
  - yan-etki
  - temiz-kod
  - test
toc: true
image: /img/python-import-tuzaklari-84.png
---

![python-import-tuzaklari-84](/img/python-import-tuzaklari-84.svg)


Python’da bir modülü içe aktarmak çoğu zaman masum görünür: Bir `import` yazarsınız ve ihtiyacınız olan fonksiyonlara ulaşırsınız. Fakat modül düzeyinde bulunan kod; dosya okuma, ağ bağlantısı kurma, veritabanını değiştirme veya ekrana mesaj basma gibi işler yapıyorsa, yalnızca import işlemi bile uygulamanın durumunu beklenmedik biçimde değiştirebilir. Kısacası kapıyı çalarken mutfağın yeniden dekore edilmesi mümkündür!

``

## Import sırasında gerçekte ne olur?

Python bir modülü ilk kez import ettiğinde yalnızca fonksiyon ve sınıf tanımlarını toplamaz. Modül dosyasını yukarıdan aşağıya çalıştırır. Fonksiyonların gövdeleri çağrılana kadar yürütülmez; ancak modül düzeyindeki ifadeler hemen değerlendirilir.

Basitleştirilmiş maliyet modeli şöyle düşünülebilir:

$$T_{import} = T_{dosya} + T_{çalıştırma} + T_{bağımlılıklar}$$

Modül düzeyindeki işlemler ağırlaştıkça $T_{çalıştırma}$ büyür. Ağ veya disk gibi dış kaynaklar kullanılıyorsa import süresi öngörülemez hâle gelir.

```python
# rapor.py
print("Rapor modülü yükleniyor...")

with open("ayarlar.txt", encoding="utf-8") as dosya:
    AYARLAR = dosya.read()

def rapor_uret():
    return f"Ayarlar: {AYARLAR}"
```

Başka bir dosyada yalnızca `import rapor` yazılması hem mesajı ekrana basar hem de `ayarlar.txt` dosyasını açar. Dosya mevcut değilse daha `rapor_uret()` çağrılmadan uygulama çöker.

## Her modül düzeyi kod kötü müdür?

Hayır. Sabit tanımlamak, hafif nesneler oluşturmak ve fonksiyonları kaydetmek genellikle normaldir. Sorun; dış dünyayı değiştiren, başarısız olabilecek veya pahalı işlemlerdir.

| Modül düzeyindeki işlem | Risk | Daha güvenli yaklaşım |
|---|---:|---|
| Sabit tanımlama | Düşük | Doğrudan tanımla |
| Saf hesaplama | Düşük | Maliyeti küçükse kullan |
| Dosya okuma | Orta | Fonksiyon içinde yükle |
| Ağ isteği | Yüksek | Açıkça çağrılan fonksiyona taşı |
| Veritabanına yazma | Çok yüksek | Servis katmanı ve işlem yönetimi kullan |
| Arka plan iş parçacığı başlatma | Çok yüksek | Yaşam döngüsünü uygulama yönetsin |

Bir işlemin yan etkili olup olmadığını şu soruyla anlayabiliriz: “Bu satır çalıştıktan sonra programın dışındaki dünya değişiyor mu?” Dosya yazılıyorsa, e-posta gönderiliyorsa veya global durum değişiyorsa cevap büyük ihtimalle evettir.

## İşlemleri fonksiyonların arkasına saklayın

Yan etkiyi tamamen yok etmek her zaman mümkün değildir; önemli olan onu açık ve kontrol edilebilir yapmaktır.

```python
# ayarlar.py
def ayarlari_yukle(dosya_yolu="ayarlar.txt"):
    """Ayarları yalnızca açıkça istendiğinde diskten okur."""
    with open(dosya_yolu, encoding="utf-8") as dosya:
        return dosya.read()
```

Bu sürümde `import ayarlar` disk erişimi yapmaz. Dosya yalnızca `ayarlari_yukle()` çağrıldığında açılır. Böylece hata yönetimi, test ve alternatif dosya kullanımı kolaylaşır.

## `__name__ == "__main__"` koruması

Bir dosyanın hem çalıştırılabilir betik hem de import edilebilir modül olması gerekiyorsa giriş noktasını koruma altına alın:

```python
def main():
    print("Veriler işleniyor...")
    # Ağ, dosya veya veritabanı işlemleri burada yapılır.

if __name__ == "__main__":
    main()
```

Dosya doğrudan çalıştırıldığında `__name__` değeri `"__main__"` olur ve `main()` çağrılır. Modül olarak import edildiğinde ise bu blok atlanır.

## Önbellek davranışını unutmayın

Python, yüklenen modülleri `sys.modules` içinde saklar. Aynı süreçte tekrarlanan sıradan import işlemleri modülü genellikle yeniden çalıştırmaz:

$$ÇalıştırmaSayısı \approx 1$$

Ancak test araçları, `importlib.reload()` kullanımı ve farklı süreçler bu güveni bozabilir. “Nasıl olsa bir kere çalışır” düşüncesi, tehlikeli yan etkileri kabul etmek için iyi bir gerekçe değildir.

Sağlıklı bir modül import edildiğinde sessiz, hızlı ve tahmin edilebilir olmalıdır. Ağ çağrılarını, dosya işlemlerini, süreç başlatmayı ve kalıcı veri değişikliklerini açık fonksiyonlara taşıyın. Böylece import, sürpriz yumurtadan tekrar sıradan ve güvenilir bir bağımlılık bildirimine dönüşür.
