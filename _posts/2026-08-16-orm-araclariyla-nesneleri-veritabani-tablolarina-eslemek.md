---
layout: post
title: "ORM Araçlarıyla Nesneleri Veritabanı Tablolarına Eşlemek"
math: true
categories: 
  - Bilgi
tags: 
  - ORM
  - Veritabanı
  - Nesne Yönelimli Programlama
---

Uygulama geliştirirken nesnelerle çalışmak doğal gelir: `User`, `Order` ve `Product` gibi sınıflar tanımlar, davranışlarını metotlarda toplarız. Veritabanı ise daha farklı düşünür; satırlar, sütunlar, tablolar ve anahtarlarla konuşur. ORM (Object-Relational Mapping), bu iki dünyanın arasında çalışan tercümandır. Doğru kullanıldığında SQL tekrarını azaltır, veri erişimini okunur kılar ve geliştiricinin iş kurallarına odaklanmasına yardım eder.
``

ORM'nin temel fikri basittir: Bir sınıf çoğunlukla bir tabloya, sınıfın alanları tablonun sütunlarına, nesne örneği ise bir satıra karşılık gelir. Örneğin `User` sınıfındaki `id`, `name` ve `email` alanları, `users` tablosundaki sütunlarla eşlenebilir. Bir kullanıcı nesnesini kaydetmek, arka planda `INSERT`; güncellemek `UPDATE`; silmek ise `DELETE` sorgusuna dönüşür.

Matematiksel olarak eşleme, sınıf özellikleri kümesi ile tablo sütunları kümesi arasındaki bir fonksiyon gibi düşünülebilir:

$$f: P \rightarrow C$$

Burada $P$, nesnenin özelliklerini; $C$ ise veritabanı sütunlarını temsil eder. İyi tasarlanmış bir modelde her önemli özellik için tutarlı bir sütun bulunur. Ancak kalıtım, gömülü nesneler ve koleksiyonlar devreye girdiğinde bu fonksiyon bire bir olmaktan çıkabilir. ORM araçlarının asıl marifeti de bu karmaşıklığı yönetmektir.

| Nesne yönelimli dünya | İlişkisel veritabanı dünyası | ORM karşılığı |
|---|---|---|
| Sınıf | Tablo | Model/Entity |
| Nesne örneği | Satır | Kayıt |
| Özellik | Sütun | Field/Column mapping |
| Nesne referansı | Foreign key | İlişki tanımı |
| Koleksiyon | Birden çok ilişkili satır | One-to-many / many-to-many |

Python ve SQLAlchemy ile sade bir örneğe bakalım. Aşağıdaki model, `users` tablosunu sınıf üzerinden tanımlar ve ORM'nin sütun eşlemesini nasıl kurduğunu gösterir:

```python
from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120), unique=True)

engine = create_engine("sqlite:///app.db", echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    user = User(name="Ada", email="ada@example.com")
    session.add(user)
    session.commit()
```

Bu kodda `__tablename__`, sınıfın hangi tabloya bağlı olduğunu belirtir. `mapped_column(primary_key=True)` ise `id` alanını birincil anahtar yapar. `session.add()` ile nesne takip edilmeye başlanır; `commit()` çağrısı sırasında ORM değişikliği algılar ve uygun SQL komutunu üretir. `echo=True` seçeneği eğitim sırasında özellikle faydalıdır: Üretilen SQL'i terminalde görerek soyutlamanın arkasında ne olduğunu anlayabilirsiniz.

İlişkiler, ORM kullanımının en güçlü taraflarından biridir. Bir kullanıcının birçok siparişi varsa ilişki şu mantıkla ifade edilir: $User\;1 \rightarrow N\;Order$. `orders` tablosunda bulunan `user_id` yabancı anahtarı, nesne tarafında `user.orders` koleksiyonu olarak görünür. Böylece geliştirici çoğu zaman elle `JOIN` yazmadan ilişkili verilere erişebilir.

| Yaklaşım | Avantaj | Dikkat edilmesi gereken nokta |
|---|---|---|
| Ham SQL | Tam kontrol, karmaşık sorgularda netlik | Tekrar eden kod ve güvenlik hatası riski |
| ORM | Hızlı geliştirme, model odaklı tasarım | Üretilen SQL'i takip etmek gerekir |
| Hibrit kullanım | Esneklik ve performans dengesi | Takım standartları belirlenmelidir |

ORM sihirli değnek değildir. Özellikle N+1 sorgu problemi önemlidir: Bir kullanıcı listesi alıp her kullanıcı için ayrı ayrı sipariş sorgusu çalıştırmak, $1 + N$ adet sorgu üretebilir. Çözüm olarak eager loading, örneğin SQLAlchemy'de `selectinload`, kullanılabilir. Büyük raporlar, toplu güncellemeler veya veritabanına özgü özelliklerde ham SQL daha doğru seçim olabilir.

Özetle ORM, veritabanını unutmak değil, onunla daha düzenli konuşmaktır. Model isimlerini, ilişki türlerini, indeksleri ve oluşan SQL'i bilinçli tasarlarsanız; hem nesne yönelimli kodunuz hem de veri katmanınız temiz, sürdürülebilir ve performanslı kalır.
