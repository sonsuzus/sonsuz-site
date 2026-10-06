---
layout: post
title: "Açık Kaynak Randevu Sistemleri: Cal.com, EasyAppointments ve LibreBooking Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - randevu sistemi
  - cal.com
  - easyappointments
  - librebooking
  - açık kaynak
  - self-hosted
toc: true
image: /img/acik-kaynak-randevu-85.png
---

Bir randevu sistemi yalnızca takvimde boş bir kutu bulup doldurmaz; insanları, hizmetleri, odaları ve zamanı aynı denklemde buluşturur. Cal.com, EasyAppointments ve LibreBooking bu problemi farklı açılardan çözen, kendi sunucunuza kurabileceğiniz güçlü seçeneklerdir. Peki hangisi işletmeniz için doğru? Takvimlerimizi açalım ve adayları masaya yatıralım.
``
## Randevu sisteminin temel mantığı

Her randevu uygulamasının merkezinde **uygunluk hesaplama motoru** bulunur. Sistem; çalışma saatlerini, mevcut rezervasyonları, hizmet süresini, molaları ve kaynak kapasitesini birlikte değerlendirir.

Basitleştirilmiş biçimde günlük teorik kapasite şöyle hesaplanabilir:

$$K = (T - M) / (S + A)$$

Burada $T$ toplam çalışma süresi, $M$ mola süresi, $S$ hizmet süresi ve $A$ randevular arasındaki hazırlık süresidir. Örneğin 480 dakikalık iş gününde 60 dakika mola, 45 dakika hizmet ve 15 dakika hazırlık varsa kapasite $K = 7$ randevudur.

İyi bir sistem bunun üzerine zaman dilimi dönüşümü, çakışma kontrolü, iptal politikası, bildirim ve tekrar eden rezervasyon gibi katmanlar ekler. Kısacası ekranda gördüğümüz küçük takvim, arka planda minik bir lojistik operasyonudur.

## Üç adayın karakteri

| Özellik | Cal.com | EasyAppointments | LibreBooking |
|---|---|---|---|
| Temel odak | Modern bireysel ve ekip planlama | Hizmet veren işletmeler | Oda, cihaz ve ortak kaynaklar |
| Arayüz | Modern ve cilalı | Sade, pratik | İşlev odaklı |
| Entegrasyon | Geniş ekosistem ve API | Google Calendar, API, webhook | LDAP ve kaynak yönetimi |
| Kurulum yapısı | Node.js, veritabanı, Docker | PHP, MySQL | PHP, MySQL |
| Öğrenme eğrisi | Orta | Kolay | Orta |
| İdeal kullanım | Danışmanlık, satış, ekip görüşmeleri | Klinik, kuaför, servis | Laboratuvar, okul, toplantı odası |

![acik-kaynak-randevu-85](/img/acik-kaynak-randevu-85.svg)


### Cal.com

Cal.com, Calendly benzeri modern bir deneyim isteyenler için öne çıkar. Bire bir toplantılar, ekip rotasyonu, ortak uygunluk, ödeme ve görüntülü görüşme entegrasyonları sunar. API tabanlı yaklaşımı sayesinde başka ürünlerin içine randevu akışı yerleştirmek de mümkündür.

Bunun karşılığında kurulum ve bakım diğer iki seçeneğe göre daha fazla kaynak isteyebilir. Docker, ortam değişkenleri, e-posta sağlayıcısı ve veritabanı yapılandırması konusunda rahat olmak avantaj sağlar. Lisans ve kurumsal özelliklerin güncel koşulları dağıtımdan önce ayrıca incelenmelidir.

### EasyAppointments

EasyAppointments, “Bir hizmet seç, çalışan seç, saat seç” akışını yalın biçimde uygular. Kuaför, danışman, klinik veya teknik servis gibi hizmet tabanlı işletmeler için oldukça uygundur. PHP ve MySQL destekleyen sıradan bir sunucuda çalışabilmesi, onu erişilebilir kılar.

Aşağıdaki örnek, Docker Compose ile temel servis yapısını gösterir:

```yaml
services:
  app:
    image: alextselegidis/easyappointments:latest
    ports:
      - '8080:80'
    environment:
      DB_HOST: db
      DB_NAME: appointments
  db:
    image: mariadb:11
    environment:
      MARIADB_DATABASE: appointments
      MARIADB_ROOT_PASSWORD: guclu-bir-parola
```

Bu yapı uygulamayı `8080` portunda yayınlar ve verileri ayrı MariaDB servisinde saklar. Gerçek kullanımda kalıcı disk, HTTPS, yedekleme ve gizli değişken yönetimi mutlaka eklenmelidir.

### LibreBooking

LibreBooking, klasik müşteri randevusundan çok **kaynak rezervasyonu** konusunda parlar. Toplantı odası, laboratuvar cihazı, spor sahası veya şirket aracı ayırtmak istiyorsanız güçlü bir adaydır. Tekrar eden rezervasyonlar, kota kuralları, kaynak grupları ve onay süreçleri sunar.

Örneğin bir cihazın aynı anda yalnızca bir kişi tarafından kullanılabilmesi kapasite kısıtıyla ifade edilir:

$$R(t) \leq C$$

Burada $R(t)$ belirli andaki rezervasyon sayısı, $C$ ise kaynak kapasitesidir. Bir mikroskop için $C=1$, on kişilik eğitim salonu için kullanım modeline bağlı olarak $C=10$ seçilebilir.

## Hangisini seçmelisiniz?

Modern entegrasyonlar, ekip takvimleri ve geliştirici deneyimi önceliğinizse **Cal.com**; hızlı kurulan klasik hizmet randevuları istiyorsanız **EasyAppointments**; oda ve ekipman gibi ortak varlıkları yönetiyorsanız **LibreBooking** daha doğru başlangıçtır.

Son karardan önce küçük bir pilot kurulum yapın. Gerçek çalışma saatlerini, iptalleri, e-posta teslimatını ve mobil deneyimi test edin. Çünkü en iyi randevu sistemi, özellik listesi en uzun olan değil, kullanıcıların randevu alırken takvime savaş ilan etmediği sistemdir.
