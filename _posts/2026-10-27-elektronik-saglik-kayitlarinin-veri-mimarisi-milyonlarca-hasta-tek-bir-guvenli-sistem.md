---
layout: post
title: "Elektronik Sağlık Kayıtlarının Veri Mimarisi: Milyonlarca Hasta, Tek Bir Güvenli Sistem"
math: true
categories: 
  - Bilgi
tags: 
  - elektronik sağlık kaydı
  - veri mimarisi
  - sağlık bilişimi
  - veritabanı
  - fhir
  - hl7
  - siber güvenlik
toc: true
image: /img/elektronik-saglik-kayitlarinin-22.png
---

![elektronik-saglik-kayitlarinin-22](/img/elektronik-saglik-kayitlarinin-22.svg)


Bir hastanenin dijital altyapısını, hiç uyumayan dev bir organizma gibi düşünebiliriz. Muayene notları, laboratuvar sonuçları, reçeteler, röntgen görüntüleri ve alerji bilgileri sürekli bu organizmanın içinde dolaşır. Elektronik sağlık kaydı sistemlerinin görevi, milyonlarca hastaya ait bu verileri yalnızca saklamak değil; doğru kişiye, doğru zamanda ve güvenli biçimde ulaştırmaktır.
``

## Sağlık verisi neden sıradan değildir?

Bir e-ticaret sisteminde yanlış ürün önerilmesi can sıkıcıdır; sağlık sisteminde yanlış ilaç bilgisinin gösterilmesi ise hayati sonuçlar doğurabilir. Bu nedenle veri mimarisi üç temel hedef etrafında kurulur:

- **Tutarlılık:** Aynı hastanın kan grubu farklı ekranlarda farklı görünmemelidir.
- **Erişilebilirlik:** Acil servisteki doktor kayda saniyeler içinde ulaşabilmelidir.
- **Gizlilik:** Veriyi yalnızca yetkili kişiler, izin verilen amaçlarla görebilmelidir.

Bir sistemin kullanılabilirliği kabaca şöyle ifade edilir:

$$A = \frac{MTBF}{MTBF + MTTR}$$

Burada $MTBF$, arızalar arasındaki ortalama süreyi; $MTTR$ ise sistemi onarmak için gereken ortalama süreyi gösterir. Sağlık platformlarında hedef genellikle %99,9 veya daha yüksek kullanılabilirliktir.

## Katmanlı mimari nasıl çalışır?

Modern sağlık sistemleri tek bir dev veritabanından ziyade görevleri ayrılmış katmanlar kullanır.

| Katman | Sorumluluk | Örnek teknoloji |
|---|---|---|
| İstemci | Doktor ve hasta ekranları | Web, mobil uygulama |
| API | İstekleri doğrulama ve yönlendirme | REST, GraphQL, FHIR |
| Servis | Reçete, randevu, laboratuvar işlemleri | Mikroservisler |
| Veri | Yapısal kayıtları saklama | PostgreSQL, Oracle |
| Dosya | Görüntü ve büyük belgeler | Nesne depolama, PACS |
| Analitik | Raporlama ve araştırma | Veri ambarı, veri gölü |

Hasta kimliği gibi ilişkisel ve tutarlı olması gereken bilgiler SQL veritabanlarında tutulabilir. MR görüntüleri ise çok büyük oldukları için PACS veya nesne depolama sistemlerine yerleştirilir; veritabanında yalnızca dosyanın adresi ve açıklayıcı metadatası bulunur.

## Hasta kayıtları nasıl modellenir?

Temel yaklaşım, hastayı benzersiz bir kimlikle diğer klinik olaylara bağlamaktır. Basitleştirilmiş bir tablo şöyle oluşturulabilir:

```sql
CREATE TABLE observations (
    observation_id BIGINT PRIMARY KEY,
    patient_id BIGINT NOT NULL,
    code VARCHAR(50) NOT NULL,
    numeric_value DECIMAL(10, 2),
    measured_at TIMESTAMP NOT NULL,
    version_no INTEGER NOT NULL
);

CREATE INDEX idx_observation_patient_time
ON observations (patient_id, measured_at DESC);
```

Bu indeks, belirli bir hastanın en güncel ölçümlerine hızla ulaşılmasını sağlar. `version_no` alanı ise aynı kayıt eş zamanlı güncellenirken değişikliklerin yanlışlıkla birbirini ezmesini önleyen iyimser kilitlemede kullanılabilir.

## Standartlar neden kritik?

Hastaneler farklı yazılımlar kullandığından sistemlerin ortak bir dil konuşması gerekir. **HL7**, klinik mesajlaşmada uzun süredir kullanılırken **FHIR**, sağlık kaynaklarını modern web API’leri üzerinden paylaşmayı kolaylaştırır. Görüntüleme tarafında ise **DICOM** standardı öne çıkar.

| Standart | Kullanım alanı | Güçlü yanı |
|---|---|---|
| HL7 v2 | Hastane içi mesajlaşma | Yaygın ve olgun |
| FHIR | API tabanlı veri paylaşımı | Web teknolojileriyle uyumlu |
| DICOM | Tıbbi görüntüler | Görüntü ve metadatayı birleştirir |

## Milyonlarca kayıt nasıl ölçeklenir?

Veriler hasta kimliğine veya coğrafi bölgeye göre bölümlenebilir. Bu işleme **sharding** denir. Okuma yükünü azaltmak için replikalar ve önbellekler kullanılır. Yaklaşık depolama ihtiyacı şu şekilde hesaplanabilir:

$$S = N \times R \times B$$

Burada $N$ hasta sayısı, $R$ hasta başına kayıt sayısı, $B$ ise ortalama kayıt boyutudur. Görüntüler hesaba katıldığında ihtiyaç petabayt seviyesine çıkabilir.

## Güvenlik görünmez bir katman değildir

Veriler aktarım sırasında TLS, depolamada ise güçlü şifreleme algoritmalarıyla korunur. Rol tabanlı erişim kontrolü sayesinde doktor, teknisyen ve muhasebe çalışanı aynı bilgileri göremez. Her görüntüleme ve değişiklik denetim günlüğüne yazılır. Yedekler farklı bölgelerde saklanır ve düzenli olarak geri yükleme testleri yapılır.

Sonuç olarak elektronik sağlık kaydı mimarisi; veritabanı, standart, güvenlik ve dağıtık sistem mühendisliğinin birleşimidir. Başarılı bir sistem yalnızca büyük veriyi taşımaz; klinik kararların güvenilir, hızlı ve izlenebilir olmasını sağlar.
