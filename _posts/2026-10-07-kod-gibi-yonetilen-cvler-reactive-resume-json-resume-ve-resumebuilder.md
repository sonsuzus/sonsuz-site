---
layout: post
title: "Kod Gibi Yönetilen CV’ler: Reactive Resume, JSON Resume ve ResumeBuilder"
math: true
categories: 
  - Program
tags: 
  - cv
  - reactive-resume
  - json-resume
  - resumebuilder
  - açık-kaynak
  - kariyer
toc: true
image: /img/kod-gibi-yonetilen-64.png
---

CV hazırlamak bazen yazılım geliştirmekten daha yorucu olabilir: Bir başlığı düzeltirsiniz, tarih sağa kaçar; yeni proje eklersiniz, ikinci sayfa ortaya çıkar. Reactive Resume, JSON Resume ve ResumeBuilder bu karmaşayı farklı yaklaşımlarla çözer. Biri görsel düzenleyiciye, biri standart veri modeline, diğeri ise hızlı şablon üretimine odaklanır.


![kod-gibi-yonetilen-64](/img/kod-gibi-yonetilen-64.svg)

``

## CV oluşturma sistemlerinin temel mantığı

Modern CV sistemlerinde içerik ile sunumun ayrılması hedeflenir. İsim, deneyim ve eğitim gibi bilgiler **veri katmanında**; renkler, yazı tipleri ve sütunlar ise **sunum katmanında** tutulur. Bu yaklaşım, web geliştirmedeki HTML ve CSS ayrımına benzer.

Bir CV’nin kalitesini basitleştirilmiş biçimde şöyle modelleyebiliriz:

$$Q = 0.45C + 0.30R + 0.15D + 0.10P$$

Burada $C$ içerik kalitesini, $R$ okunabilirliği, $D$ tasarım tutarlılığını ve $P$ taşınabilirliği temsil eder. Görsel olarak şahane fakat içeriği zayıf bir CV’nin neden yeterli olmadığını bu ağırlıklar açıklar.

## Üç yaklaşımın karşılaştırması

| Sistem | Temel yaklaşım | Güçlü yönü | En uygun kullanıcı |
|---|---|---|---|
| Reactive Resume | Görsel editör ve yapılandırılmış veri | Kullanım kolaylığı, özelleştirme ve self-hosting | Tasarım kontrolü isteyen geliştirici |
| JSON Resume | Açık JSON şeması ve tema ekosistemi | Taşınabilirlik ve otomasyon | CV’sini kod gibi yönetmek isteyen kişi |
| ResumeBuilder | Form tabanlı hızlı oluşturma | Düşük öğrenme eşiği | Hızlıca standart CV hazırlamak isteyen kullanıcı |

**Reactive Resume**, sürükleyip düzenlemeye yakın bir deneyim sunarken verileri yapılandırılmış biçimde saklar. Açık kaynaklı olması ve kendi sunucunuza kurulabilmesi, gizlilik açısından önemli bir avantajdır. Birden fazla CV sürümü üretmek isteyenler için de pratiktir.

**JSON Resume** ise tek başına klasik bir tasarım aracı değil, standartlaştırılmış bir öz geçmiş veri formatıdır. Aynı JSON dosyasını farklı temalarla HTML, PDF veya web sayfasına dönüştürebilirsiniz. Böylece CV’niz Git deposunda sürüm kontrollü şekilde yaşayabilir.

**ResumeBuilder** adıyla sunulan araçlar çoğunlukla kullanıcıyı adım adım yönlendiren form ve şablon sistemleridir. Teknik bilgi gerektirmezler; ancak veri dışa aktarma, tema özgürlüğü ve self-hosting seçenekleri ürüne göre sınırlı olabilir.

## JSON ile CV hazırlamak

Aşağıdaki örnek, kişisel bilgiler ile iş deneyimini makine tarafından okunabilir biçimde saklar:

```json
{
  "basics": {
    "name": "Deniz Kaya",
    "label": "Backend Developer",
    "email": "deniz@example.com"
  },
  "work": [
    {
      "name": "Örnek Teknoloji",
      "position": "Yazılım Geliştirici",
      "startDate": "2023-01",
      "summary": "API performansını yüzde 35 artırdı."
    }
  ]
}
```

Bu blokta `basics` iletişim bilgilerini, `work` ise deneyimleri taşır. Veriyi ayrı tutmanın güzelliği şudur: Yazım hatasını bir kez düzeltir, bütün temalara otomatik yansıtırsınız. Ayrıca Git sayesinde değişiklik geçmişini görebilir ve farklı pozisyonlar için dallar oluşturabilirsiniz.

Örneğin JSON Resume komut satırı araçlarıyla tema kullanarak çıktı üretme fikri şöyledir:

```bash
# CV verisini doğrular
resume validate resume.json

# Seçilen tema ile HTML çıktısı oluşturur
resume export cv.html --theme elegant
```

Komutlar, kullanılan CLI sürümüne ve temaya göre değişebilir; bu nedenle ilgili aracın güncel belgeleri kontrol edilmelidir.

## Hangisini seçmelisiniz?

Görsel arayüz, gizlilik ve kişiselleştirme istiyorsanız **Reactive Resume** güçlü bir dengedir. CI/CD, Git ve otomatik yayınlama gibi geliştirici alışkanlıklarını CV’ye taşımak istiyorsanız **JSON Resume** daha uygundur. Sadece bilgileri girip dakikalar içinde PDF indirmek istiyorsanız **ResumeBuilder** tarzı araçlar yeterlidir.

En esnek yöntem ise hibrit yaklaşımdır: Ana veriyi JSON biçiminde saklayın, görsel düzenleme veya son rötuş için Reactive Resume benzeri bir araca aktarın. Böylece CV’niz yalnızca bir belge değil; güncellenebilir, taşınabilir ve sürüm kontrollü küçük bir yazılım projesi olur.
