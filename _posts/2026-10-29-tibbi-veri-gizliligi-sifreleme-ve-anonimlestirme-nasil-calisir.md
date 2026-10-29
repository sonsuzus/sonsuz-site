---
layout: post
title: "Tıbbi Veri Gizliliği: Şifreleme ve Anonimleştirme Nasıl Çalışır?"
math: true
categories: 
  - Bilgi
tags: 
  - tıbbi veri
  - veri gizliliği
  - şifreleme
  - anonimleştirme
  - siber güvenlik
  - sağlık teknolojileri
toc: true
image: /img/tibbi-veri-gizliligi-10.png
---

Bir hastane kaydında yalnızca tanı ve tahlil sonuçları bulunmaz; ad, kimlik numarası, genetik özellikler, kullanılan ilaçlar ve hatta psikolojik değerlendirmeler de yer alabilir. Bu bilgiler yanlış ellere geçtiğinde kredi kartı gibi kolayca değiştirilemez. İşte bu nedenle tıbbi verilerin korunması, kapıya güçlü bir kilit takmaktan çok daha fazlasını gerektirir.

``

## Önce tehdit modelini anlayalım

Veri güvenliği planlanırken “Neyi kimden koruyoruz?” sorusu sorulur. Saldırgan dışarıdan sisteme sızan biri olabileceği gibi gereğinden fazla yetkiye sahip bir çalışan veya yanlış yapılandırılmış bir bulut servisi de olabilir.

Tıbbi veriler genellikle üç durumda korunur:

- **Depolanan veri:** Veritabanı, disk, yedek veya arşiv içindeki kayıtlar.
- **Aktarılan veri:** Hastane ile laboratuvar arasında dolaşan bilgiler.
- **İşlenen veri:** Bir uygulamanın belleğinde aktif olarak kullanılan kayıtlar.

Şifreleme ilk iki durumda oldukça etkilidir. İşlenen veride ise erişim kontrolü, denetim kayıtları ve güvenli çalışma ortamları devreye girer.

## Şifreleme: Veriyi okunamaz hâle getirmek

Şifreleme, açık veriyi bir anahtar yardımıyla anlamsız görünen şifreli metne dönüştürür. Basitleştirilmiş biçimiyle:

$$C = E_K(P)$$

Burada $P$ açık tıbbi kayıt, $K$ anahtar, $E$ şifreleme işlemi ve $C$ şifreli çıktıdır. Yetkili taraf aynı veya ilişkili anahtarla veriyi çözer.

| Yöntem | Temel özellik | Sağlık sistemindeki kullanım |
|---|---|---|
| Simetrik şifreleme | Aynı anahtar kullanılır, hızlıdır | Veritabanı ve yedek şifreleme |
| Asimetrik şifreleme | Açık ve özel anahtar çifti kullanır | Anahtar paylaşımı, dijital imza |
| TLS | Aktarım kanalını korur | Hasta portalı ve laboratuvar bağlantıları |
| Hash | Tek yönlü özet üretir | Bütünlük kontrolü, parola doğrulama |

![tibbi-veri-gizliligi-10](/img/tibbi-veri-gizliligi-10.svg)


Şifrelenmiş verinin güvenliği algoritmanın gizli tutulmasına değil, anahtarın korunmasına dayanmalıdır. Anahtarı şifreli verinin yanında düz metin olarak saklamak, kasanın anahtarını kapağına bantlamaya benzer. Üretim sistemlerinde anahtar yönetim servisleri, düzenli anahtar döndürme ve donanımsal güvenlik modülleri tercih edilir.

## Anonimleştirme ile kimliği ayırmak

Anonimleştirme, bir kişinin makul yöntemlerle yeniden belirlenememesini amaçlar. Ad ve kimlik numarasını silmek tek başına yeterli değildir. Nadir bir hastalık, posta kodu ve doğum tarihi bir araya geldiğinde kişi tekrar bulunabilir.

**Takma adlandırma (pseudonymization)** işleminde kimlik, rastgele bir kodla değiştirilir; eşleştirme anahtarı korunduğu sürece işlem geri alınabilir. Gerçek anonimleştirmede ise geri dönüş bağlantısının ortadan kaldırılması hedeflenir.

| Teknik | Ne yapar? | Sınırlaması |
|---|---|---|
| Maskeleme | Değerin bir bölümünü gizler | Bağlam kimliği ele verebilir |
| Genelleştirme | Yaşı 47 yerine 40–50 yapar | Analiz hassasiyeti azalır |
| $k$-anonimlik | Her kaydı en az $k-1$ kayda benzetir | Hassas değer çeşitliliğini garanti etmez |
| Diferansiyel gizlilik | Sonuçlara kontrollü gürültü ekler | Gizlilik-doğruluk dengesi gerekir |

Diferansiyel gizlilikte küçük bir $epsilon$ değeri daha güçlü gizliliği, fakat daha fazla gürültüyü ifade eder. Temel düşünce, tek bir kişinin veri kümesine eklenmesinin istatistiksel sonucu belirgin biçimde değiştirmemesidir.

## Basit bir takma adlandırma örneği

Aşağıdaki Python kodu hasta numarasını gizli bir anahtarla HMAC özetine dönüştürür. Aynı numara aynı kodu üretir; böylece kayıtlar gerçek kimlik gösterilmeden ilişkilendirilebilir.

```python
import hmac
import hashlib

def hasta_kodu(hasta_no: str, gizli_anahtar: bytes) -> str:
    ozet = hmac.new(
        gizli_anahtar,
        hasta_no.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return ozet[:16]

kod = hasta_kodu("HASTA-1042", b"ornek-gizli-anahtar")
print(kod)
```

Bu örnek eğitim amaçlıdır. Gerçek sistemlerde anahtar kaynak koduna yazılmaz; güvenli bir kasada tutulur. Ayrıca çıktı kısaltılırken çakışma riski değerlendirilmelidir.

## Tek teknoloji yetmez

Sağlık verilerini korumak katmanlı savunma gerektirir: en az ayrıcalık ilkesi, çok faktörlü kimlik doğrulama, erişim kayıtları, yedekleme, sızıntı izleme ve çalışan eğitimi birlikte uygulanmalıdır. Araştırma için yalnızca gerekli alanlar paylaşılmalı, saklama süresi dolan kayıtlar güvenli biçimde silinmelidir.

Kısacası şifreleme veriyi kilitler, anonimleştirme kişiyle arasındaki bağı zayıflatır. Doğru anahtar yönetimi ve yeniden kimliklendirme riskinin düzenli ölçümü olmadan ise bu iki güçlü araç, beyaz önlük giymiş bir güvenlik illüzyonuna dönüşebilir.
