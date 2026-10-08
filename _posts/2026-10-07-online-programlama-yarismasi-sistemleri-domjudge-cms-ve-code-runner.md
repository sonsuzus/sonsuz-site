---
layout: post
title: "Online Programlama Yarışması Sistemleri: DOMjudge, CMS ve Code Runner"
math: true
categories: 
  - Program
tags: 
  - programlama
  - domjudge
  - cms
  - code-runner
  - algoritma
  - docker
  - güvenlik
toc: true
image: /img/online-programlama-yarismasi-42.png
---

![online-programlama-yarismasi-42](/img/online-programlama-yarismasi-42.svg)


Bir programlama yarışmasında ekranda yalnızca sorular, puanlar ve heyecan görünür. Perdenin arkasında ise gönderilen kodu derleyen, güvenli biçimde çalıştıran, test eden ve birkaç saniye içinde karar üreten küçük bir altyapı orkestrası vardır. DOMjudge, CMS ve özel bir Code Runner bu orkestrayı yönetmek için kullanılan üç farklı yaklaşımdır.

``

## Temel çalışma mantığı

Yarışmacı kaynak kodunu sisteme gönderdiğinde değerlendirme süreci genel olarak şu adımlardan oluşur:

1. Gönderi veritabanına kaydedilir.
2. Uygun derleyici seçilir.
3. Kod izole bir ortamda derlenir.
4. Program gizli test girdileriyle çalıştırılır.
5. Çıktı, beklenen sonuçla karşılaştırılır.
6. süre, bellek ve doğruluk bilgileri puana dönüştürülür.

Bir testin kabul edilmesini basitçe şöyle ifade edebiliriz:

$$Accepted = CorrectOutput \land (t \leq T) \land (m \leq M)$$

Burada $t$ çalışma süresi, $T$ süre sınırı, $m$ kullanılan bellek ve $M$ bellek sınırıdır. Yalnızca doğru çıktı üretmek yetmez; çözüm kaynak sınırlarına da uymalıdır.

Toplam değerlendirme maliyeti yaklaşık olarak $O(S \times C)$ düşünülebilir. $S$ gönderi sayısını, $C$ ise gönderi başına test ve çalıştırma maliyetini temsil eder. Yarışmacı sayısı büyüdükçe değerlendirme sunucularını yatay olarak çoğaltmak kritik hâle gelir.

## Üç yaklaşımın karşılaştırması

| Özellik | DOMjudge | CMS | Özel Code Runner |
|---|---|---|---|
| Ana kullanım | ICPC tarzı yarışmalar | IOI tarzı olimpiyatlar | Eğitim veya özel platformlar |
| Kurulum | Görece kolay | Daha karmaşık | Tamamen geliştiriciye bağlı |
| Puanlama | Problem ve gönderi odaklı | Alt görev ve kısmi puan odaklı | İstenildiği gibi tasarlanabilir |
| Arayüz | Hazır yönetim paneli | Güçlü yarışma araçları | Sıfırdan geliştirilir |
| Esneklik | Orta | Yüksek | Çok yüksek |
| Bakım yükü | Düşük-orta | Orta-yüksek | Yüksek |

### DOMjudge

DOMjudge, özellikle ICPC formatında oldukça pratiktir. Takım hesapları, balon sistemi, skor tablosu dondurma, jüri cevapları ve çoklu değerlendirme makineleri hazır gelir. Klasik doğru-yanlış problemler için hızlıca ayağa kaldırılabilir. Üniversite yarışması düzenliyorsanız, tekerleği yeniden icat etmek yerine güçlü bir başlangıç sunar.

### CMS

Contest Management System, yani CMS, olimpiyat tipi yarışmalara daha uygundur. Alt görevler, kısmi puanlar, çıktı odaklı problemler ve ayrıntılı puanlama modellerinde öne çıkar. Örneğin bir problemde ilk alt görev 20, ikincisi 30, üçüncüsü 50 puan olabilir:

$$Score = 20s_1 + 30s_2 + 50s_3, \quad s_i \in \{0,1\}$$

Bu esneklik değerlidir; ancak kurulum ve operasyon bilgisi gereksinimi DOMjudge’a göre daha yüksektir.

### Özel Code Runner

Code Runner, tek başına tam bir yarışma sistemi değildir. Kodu çalıştıran değerlendirme motorudur; kullanıcı yönetimi, soru paneli, skor tablosu ve itiraz süreçleri ayrıca geliştirilir. Buna karşılık eğitim platformları, otomatik ödevler veya şirkete özgü mülakat senaryoları için mükemmel esneklik sağlar.

Aşağıdaki örnek, Docker kullanarak Python kodunu ağ erişimi olmadan ve kaynak sınırlarıyla çalıştırır:

```bash
docker run --rm \
  --network none \
  --memory 256m \
  --cpus 0.5 \
  --read-only \
  -v ./submission:/app:ro \
  python:3.12-alpine \
  timeout 2s python /app/main.py
```

Bu komut belleği 256 MB ile sınırlar, işlemci kotası uygular, dosya sistemini salt okunur bağlar ve programı iki saniye sonra durdurur. Yine de Docker tek başına kusursuz bir güvenlik duvarı değildir; seccomp, AppArmor, kullanıcı yetkileri ve mümkünse gVisor ya da sanal makine izolasyonu eklenmelidir.

## Hangisini seçmeli?

Hızlı bir ICPC yarışması için **DOMjudge**, olimpiyat ve kısmi puanlama için **CMS**, ürüne özel değerlendirme akışları için **Code Runner** mantıklı seçimdir. En önemli kriter yalnızca özellik sayısı değil; ekibin bakım kapasitesi, güvenlik bilgisi ve beklenen gönderi trafiğidir. Çünkü yarışma günü en zor algoritma bazen sorularda değil, çöken değerlendirme kuyruğundadır!
