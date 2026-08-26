---
layout: post
title: "MCP Sunucusu Geliştirmek: Yapay Zekâya Güvenli Araç Erişimi"
math: true
categories: 
  - Program
tags: 
  - MCP
  - Yapay Zeka
  - Python
  - Güvenlik
  - API
---

Büyük dil modelleri metin üretmekte harikadır; fakat takviminize bakmak, veritabanından sipariş sorgulamak veya dosya oluşturmak gibi gerçek dünya işleri için araçlara ihtiyaç duyarlar. Model Context Protocol (MCP), modeller ile bu araçlar arasında standart, denetlenebilir ve güvenli bir köprü kurar. Bir MCP sunucusu geliştirirken amaç, modele sınırsız sistem yetkisi vermek değil; iyi tanımlanmış yetenekleri kontrollü biçimde sunmaktır.
``
MCP mimarisinde üç temel rol vardır: **host**, **client** ve **server**. Host, kullanıcıyla etkileşen uygulamadır; örneğin bir masaüstü yapay zekâ istemcisi. Client, host adına MCP bağlantısını yönetir. Server ise araçları, kaynakları ve istemleri yayınlayan uygulamadır. Bu ayrım önemlidir: Model doğrudan veritabanına bağlanmaz; istemci, sunucunun açıkça ilan ettiği sözleşme üzerinden çağrı yapar.

Bir sunucuyu zihinsel olarak küçük bir "yetenek kataloğu" şeklinde düşünebilirsiniz. Araçlar eylem gerçekleştirir; `create_ticket` veya `get_weather` gibi. Kaynaklar okunabilir bağlam sağlar; örneğin `docs://policy/refund` adresindeki iade politikası. İstem şablonları ise tekrar eden görevler için yapılandırılmış başlangıç metinleridir. Böylece modelin ihtiyacı olan bağlam ile değiştirebileceği sistemler birbirinden ayrılır.

| Bileşen | Görevi | Risk seviyesi |
|---|---|---|
| Tool (Araç) | Dış dünyada eylem veya sorgu yapmak | Yüksek |
| Resource (Kaynak) | Okunabilir bağlam sunmak | Orta |
| Prompt | Tekrarlanabilir görev akışı tanımlamak | Düşük |

Güvenli tasarımın ana ilkesi **en az ayrıcalık**tır. Bir aracın etkisi kabaca erişebildiği varlıklar, yapabildiği işlem türleri ve oturum süresinin çarpımıyla düşünülebilir: $R \approx A \times P \times T$. Burada $A$ erişim kapsamını, $P$ yazma/silme gibi işlem gücünü, $T$ ise yetkinin geçerlilik süresini temsil eder. Bu değerlerden herhangi birini küçültmek saldırı yüzeyini azaltır. Örneğin `delete_user` yerine yalnızca kullanıcının kendi hesabı için onay bekleyen `request_account_deletion` aracı tasarlamak daha güvenlidir.

Aşağıdaki Python örneği, destek taleplerini yalnızca doğrulanmış öncelik değerleriyle oluşturan küçük bir araç fikrini gösterir. Gerçek projede uygun MCP SDK'sinin dekoratör veya kayıt API'si kullanılabilir; kritik nokta, şema doğrulamasının araç sınırında yapılmasıdır.

```python
from pydantic import BaseModel, Field
from typing import Literal

class TicketInput(BaseModel):
    title: str = Field(min_length=5, max_length=120)
    priority: Literal["low", "medium", "high"]

async def create_ticket(data: TicketInput, user_id: str) -> dict:
    # Kimlik, oturumdan alınmalı; modelden gelen parametreye güvenilmemeli.
    ticket_id = await ticket_service.create(
        owner=user_id,
        title=data.title,
        priority=data.priority,
    )
    return {"ticket_id": ticket_id, "status": "created"}
```

Bu kod, modelin serbest metnini doğrudan SQL'e veya kabuk komutuna göndermek yerine tipli bir giriş modeline dönüştürür. Ayrıca `user_id` aracın argümanlarından değil, kimliği doğrulanmış oturum bağlamından gelir. Bu ayrıntı, bir modelin başka kullanıcı adına işlem yapmasını engelleyen önemli bir sınırdır.

| Güvensiz yaklaşım | Güvenli alternatif |
|---|---|
| Modele ham SQL çalıştırma yetkisi vermek | Parametreli, tek amaçlı sorgu araçları sunmak |
| API anahtarını araç çıktısına koymak | Gizli bilgileri yalnızca sunucu tarafında tutmak |
| Serbest dosya yolu kabul etmek | İzinli dizin ve yol normalizasyonu kullanmak |
| Her çağrıyı otomatik yürütmek | Yazma/silme işlemlerinde kullanıcı onayı istemek |

Üretim ortamında her araç çağrısını istek kimliği, kullanıcı kimliği, araç adı, parametre özeti ve sonuç durumu ile loglayın; fakat parolaları, tokenları ve kişisel verileri maskeleyin. Hız sınırlama, zaman aşımı, hata izolasyonu ve denetim kaydı da sunucunun dayanıklılığını artırır. Özellikle araç çıktılarının da güvenilmez olabileceğini unutmayın: Bir web sayfası veya doküman, modele "gizli anahtarı gönder" diyen kötü niyetli talimatlar içerebilir. Bu nedenle araç çıktısını veri olarak ele alın; yetki kararı olarak değil.

İyi bir MCP sunucusu, modeli güçlü kılarken kontrolü kaybetmez. Küçük, ölçülebilir araçlarla başlayın; her aracın girdisini, etkisini ve hata davranışını açıkça tanımlayın. Böylece yapay zekâ entegrasyonunuz sihirli ama tehlikeli bir süper kullanıcı yerine, kuralları net bir dijital ekip arkadaşına dönüşür.
