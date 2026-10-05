---
layout: post
title: "Kendi Video Paylaşım Siteni Kur: PeerTube, MediaCMS ve ClipBucket Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - peertube
  - mediacms
  - clipbucket
  - video
  - açık kaynak
  - self-hosted
  - streaming
toc: true
image: /img/kendi-video-paylasim-97.png
---

![kendi-video-paylasim-97](/img/kendi-video-paylasim-97.svg)


YouTube benzeri bir platform kurmak kulağa yalnızca “videoyu yükle ve oynat” kadar kolay gelebilir. Oysa perde arkasında kod dönüştürme, depolama, bant genişliği, moderasyon ve ölçeklendirme gibi birçok hareketli parça bulunur. Neyse ki PeerTube, MediaCMS ve ClipBucket gibi açık kaynaklı çözümler sayesinde sıfırdan bir video motoru yazmak yerine hazır bir altyapıyı özelleştirebiliriz.

``

## Video platformunun temel çalışma mantığı

Kullanıcı tarafından yüklenen bir video genellikle doğrudan yayınlanmaz. Önce FFmpeg gibi bir araçla farklı çözünürlük ve bit hızlarına dönüştürülür. Böylece yavaş bağlantıya sahip kullanıcı 480p, hızlı bağlantıya sahip kullanıcı ise 1080p sürümü izleyebilir. Bu yaklaşım **uyarlanabilir akış** olarak adlandırılır.

Bir videonun yaklaşık dosya boyutu şu formülle hesaplanabilir:

$$
D = \frac{b \times t}{8}
$$

Burada $D$ dosya boyutunu, $b$ saniye başına bit hızını ve $t$ video süresini ifade eder. Örneğin 4 Mbps bit hızına sahip 10 dakikalık bir video yaklaşık olarak:

$$
D = \frac{4 \times 600}{8} = 300\text{ MB}
$$

alan kaplar. Aynı videonun birkaç farklı çözünürlükte saklanması, depolama ihtiyacını kolayca iki veya üç katına çıkarabilir. Kısacası sunucunun diski, video platformunun gizli final bölüm canavarıdır.

## Üç platformun karşılaştırması

| Özellik | PeerTube | MediaCMS | ClipBucket |
|---|---|---|---|
| Ana teknoloji | Node.js, PostgreSQL | Python, Django | PHP, MySQL |
| Dağıtık yapı | ActivityPub ve WebTorrent | Yok | Yok |
| Kurulum kolaylığı | Orta | Orta | Kolay-Orta |
| Modern arayüz | Güçlü | Güçlü | Temaya bağlı |
| En uygun kullanım | Federasyon ve topluluk | Kurumsal medya arşivi | Klasik video portalı |
| Ölçeklendirme yaklaşımı | Eşler arası dağıtım | Sunucu ve depolama odaklı | Geleneksel web mimarisi |

### PeerTube

PeerTube’un en dikkat çekici özelliği merkezi olmayan yapısıdır. ActivityPub protokolü sayesinde farklı PeerTube sunucuları birbirini takip edebilir. WebTorrent desteği ise izleyicilerin video parçalarını birbirleriyle paylaşmasına olanak tanır. Bu durum teorik olarak ana sunucunun bant genişliği yükünü azaltır.

Toplam sunucu trafiğini basitleştirerek şöyle düşünebiliriz:

$$
T_s = T_i \times (1-p)
$$

$T_i$ izleyicilerin toplam trafiği, $p$ ise eşler tarafından karşılanan trafik oranıdır. $p$ arttıkça sunucunun yükü azalır. Ancak az izlenen videolarda yeterli eş bulunmayacağı için mucize beklememek gerekir.

### MediaCMS

MediaCMS; eğitim kurumları, şirket içi video portalları ve düzenli medya arşivleri için oldukça mantıklıdır. Django tabanlı olması, Python ekosistemine aşina ekiplerin yeni özellikler geliştirmesini kolaylaştırır. Kategori, etiket, oynatma listesi, altyazı ve rol yönetimi gibi içerik odaklı araçları hazır sunar.

Docker ile servisleri yönetmek için temel yaklaşım şöyledir:

```bash
# Projeyi indirir ve yapılandırma klasörüne geçer.
git clone https://github.com/mediacms-io/mediacms.git
cd mediacms

# Web, veritabanı ve arka plan servislerini başlatır.
docker compose up -d
```

Bu komutlar örnek niteliğindedir; üretim ortamında alan adı, HTTPS, kalıcı diskler ve e-posta ayarları ayrıca yapılandırılmalıdır.

### ClipBucket

ClipBucket, geleneksel YouTube klonu yaklaşımına daha yakındır. PHP tabanlı olduğu için klasik LAMP sunucularına kurulabilir ve yaygın hosting bilgisiyle yönetilebilir. Tema ve eklenti yapısı avantaj sağlasa da sürüm seçerken bakım durumu, güvenlik yamaları ve kullanılan FFmpeg uyumluluğu dikkatle kontrol edilmelidir.

## Hangisini seçmelisin?

Federasyon, topluluklar arası etkileşim ve bant genişliği paylaşımı istiyorsan **PeerTube** öne çıkar. Eğitim portalı, şirket içi medya merkezi veya düzenli bir video arşivi hedefliyorsan **MediaCMS** daha uygun bir temel sunar. PHP ekosistemine hâkimsen ve klasik video sitesi deneyimi arıyorsan **ClipBucket** değerlendirilebilir.

Hangi yazılımı seçersen seç, ters proxy, HTTPS, yedekleme, nesne depolama ve moderasyon planını baştan oluşturmalısın. Çünkü başarılı bir video sitesi yalnızca oynatma düğmesinden değil, görünmeyen altyapının uyum içinde çalışmasından doğar.
