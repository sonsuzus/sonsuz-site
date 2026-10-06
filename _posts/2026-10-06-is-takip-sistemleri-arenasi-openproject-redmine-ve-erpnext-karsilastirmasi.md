---
layout: post
title: "İş Takip Sistemleri Arenası: OpenProject, Redmine ve ERPNext Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - iş takibi
  - openproject
  - redmine
  - erpnext
  - proje yönetimi
  - açık kaynak
toc: true
image: /img/is-takip-sistemleri-96.png
---

Ekip büyüdükçe görevleri mesajlaşma uygulamalarından takip etmek, çorba çatalla içmeye benzer: Teorik olarak mümkündür ama sonuç genellikle dağınıklıktır. OpenProject, Redmine ve ERPNext; işleri merkezi hâle getiren, sorumlulukları görünür kılan ve “Bu görev kimdeydi?” sorusunu azaltan üç açık kaynak çözüm sunar. Ancak benzer görünen bu araçların odak noktaları ve ideal kullanım senaryoları oldukça farklıdır.

``

## İş takip sisteminin temel mantığı

Bir iş takip sistemi, yapılacak işi tanımlı durumlar arasında ilerleyen bir kayıt olarak ele alır. Basit bir akış şöyle düşünülebilir:

`Yeni → Devam Ediyor → İncelemede → Tamamlandı`

Her işin sorumlusu, önceliği, tahmini süresi, son tarihi ve geçmişi bulunur. Böylece ekip yalnızca görev listesini değil, sürecin nasıl aktığını da görebilir. Planlama kalitesini ölçmek için temel bir oran kullanılabilir:

$$Başarı\ Oranı = Tamamlanan\ İş / Planlanan\ İş$$

Örneğin sprint başında 40 iş planlanıp 32 iş tamamlandıysa başarı oranı $32/40 = 0.8$, yani yüzde 80’dir. Bu değer tek başına performans notu değildir; kapasite tahminlerinin ne kadar gerçekçi olduğunu gösteren bir sinyaldir.

## Üç aracın karakteri

| Özellik | OpenProject | Redmine | ERPNext |
|---|---|---|---|
| Ana odak | Proje yönetimi | Sorun ve görev takibi | Kurumsal kaynak planlama |
| Arayüz | Modern ve görsel | Sade, klasik | Modüler ve iş odaklı |
| Agile desteği | Güçlü | Eklentilerle gelişir | Temel düzeyde kullanılabilir |
| Gantt şeması | Yerleşik | Yerleşik | Proje modülünde mevcut |
| Finans ve stok | Sınırlı | Doğrudan yok | Çok güçlü |
| Özelleştirme | Alanlar ve iş akışları | Eklenti ekosistemi | DocType ve modüller |
| İdeal kullanıcı | Proje ekipleri | Yazılım ve destek ekipleri | Operasyon yöneten şirketler |

![is-takip-sistemleri-96](/img/is-takip-sistemleri-96.svg)


### OpenProject: Planlama meraklısı

OpenProject; yol haritaları, iş paketleri, Gantt şemaları ve çevik panolarıyla kapsamlı proje yönetimine odaklanır. Büyük projelerde bağımlılıkları görmek ve zaman çizelgesini yönetmek isteyen ekipler için güçlüdür. Scrum veya Kanban uygulayan ancak üst düzey raporlamadan da vazgeçmek istemeyen kuruluşlara uygundur.

### Redmine: Sade ve dayanıklı

Ruby on Rails tabanlı Redmine, özellikle hata kaydı ve yazılım işi takibinde yıllardır kullanılan güvenilir bir seçenektir. Proje, sürüm, wiki, zaman kaydı ve rol tabanlı yetkilendirme özellikleri sunar. Arayüzü rakipleri kadar gösterişli değildir; buna karşılık düşük kaynak tüketimi ve geniş eklenti ekosistemi önemli avantajlardır.

Redmine API üzerinden yeni bir iş oluşturmak mümkündür:

```python
import requests

url = "https://redmine.example.com/issues.json"
headers = {"X-Redmine-API-Key": "API_ANAHTARI"}
data = {
    "issue": {
        "project_id": 1,
        "subject": "Ödeme ekranını test et",
        "priority_id": 2
    }
}

response = requests.post(url, json=data, headers=headers)
print(response.status_code)
```

Bu örnek, harici bir test veya izleme aracında oluşan kaydı otomatik olarak Redmine görevine dönüştürür. Gerçek projelerde API anahtarını kaynak koduna yazmak yerine ortam değişkeninde saklamak gerekir.

### ERPNext: Görevden faturaya

ERPNext yalnızca görev yönetmez; müşteri, satış, muhasebe, stok, insan kaynakları ve üretim süreçlerini aynı platformda birleştirir. Bir görev için harcanan zaman çizelgesi, projeye ve müşteriye bağlanabilir; ardından faturalandırma sürecine aktarılabilir. Bu nedenle “İşi kim yapacak?” kadar “Bu işin maliyeti ve geliri nedir?” sorusuyla ilgilenen şirketlerde öne çıkar.

## Hangisini seçmeli?

Seçimi özellik sayısına göre değil, süreç kapsamına göre yapmak gerekir. Ayrıntılı proje planlaması ve modern çevik panolar öncelikliyse **OpenProject**, hızlı hata ve destek kaydı ile eklenti esnekliği aranıyorsa **Redmine**, proje verilerinin muhasebe, satış veya stokla birleşmesi gerekiyorsa **ERPNext** daha mantıklıdır.

Karar vermeden önce küçük bir pilot proje oluşturun; beş kullanıcıyla iki hafta deneyin ve görev açma süresi, tamamlanma oranı, rapor okunabilirliği gibi ölçütleri karşılaştırın. Çünkü en iyi iş takip sistemi, en fazla düğmeye sahip olan değil, ekibin her gün isteyerek güncellediği sistemdir.
