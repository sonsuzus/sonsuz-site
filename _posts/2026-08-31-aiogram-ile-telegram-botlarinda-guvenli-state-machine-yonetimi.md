---
layout: post
title: "Aiogram ile Telegram Botlarında Güvenli State Machine Yönetimi"
math: true
categories: 
  - Program
tags: 
  - aiogram
  - telegram-bot
  - fsm
toc: true
---

Bir Telegram botunun kullanıcıya art arda sorular sorması ilk bakışta basit görünür: adı sor, yanıtı kaydet, yaşı sor ve işlemi tamamla. Fakat aynı anda yüzlerce kullanıcı konuşmaya başladığında hangi yanıtın hangi soruya ait olduğunu bilmek zorlaşır. Aiogram’un Finite State Machine, yani FSM sistemi, her kullanıcı için konuşmanın mevcut adımını ve geçici verilerini düzenli biçimde yönetmemizi sağlar.

``

## FSM mantığı nedir?

Sonlu durum makinesi, bir sistemin belirli sayıdaki durumdan yalnızca birinde bulunabileceği modeldir. Botumuzun durum kümesini şöyle gösterebiliriz:

$$S = \{başlangıç, ad\_bekleniyor, yaş\_bekleniyor, tamamlandı\}$$

Bir mesaj geldiğinde geçiş fonksiyonu mevcut durum ve girdiye bakar:

$$\delta(durum, mesaj) = yeni\ durum$$

Örneğin kullanıcı `/kayit` komutunu gönderdiğinde bot `ad_bekleniyor` durumuna geçer. Kullanıcının sonraki mesajı artık sıradan bir sohbet mesajı değil, ad bilgisi olarak değerlendirilir. Böylece handler’lar yalnızca ilgilendikleri durumda çalışır.

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Global değişken | Kurulumu kolaydır | Kullanıcı verileri karışabilir |
| MemoryStorage | Geliştirme için hızlıdır | Uygulama kapanınca veriler silinir |
| RedisStorage | Kalıcı, hızlı ve ölçeklenebilirdir | Ayrı Redis servisi gerektirir |

## Durumları tanımlamak

Aiogram 3 sürümünde durumlar `StatesGroup` sınıfıyla gruplanabilir:

```python
from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    waiting_name = State()
    waiting_age = State()
```

Bu sınıf kayıt sürecinin haritasıdır. Durum adlarının açık olması, büyüyen projelerde `state1`, `state2` gibi gizemli isimlerle dedektifçilik yapmamızı engeller.

## Handler’larla adım adım veri toplamak

Aşağıdaki örnek kullanıcıdan önce adını, ardından yaşını ister. `FSMContext`, aktif durumu değiştirmek ve geçici verileri saklamak için kullanılır:

```python
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()

@router.message(Command('kayit'))
async def start_registration(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Registration.waiting_name)
    await message.answer('Adınız nedir?')

@router.message(Registration.waiting_name, F.text)
async def receive_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(Registration.waiting_age)
    await message.answer('Yaşınız kaç?')

@router.message(Registration.waiting_age, F.text)
async def receive_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Lütfen yaşı sayı olarak yazın.')
        return

    age = int(message.text)
    data = await state.get_data()
    await message.answer(
        f"Kayıt tamamlandı: {data['name']}, {age} yaşında."
    )
    await state.clear()
```

`update_data()` bilgiyi mevcut kullanıcı ve sohbet bağlamında saklar. `clear()` ise işlem tamamlandığında hem durumu hem de geçici verileri temizler. Temizleme yapılmazsa kullanıcı eski durum içinde sıkışabilir.

## Güvenli depolama seçimi

Yerel geliştirmede `MemoryStorage` yeterlidir:

```python
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

dp = Dispatcher(storage=MemoryStorage())
```

Üretimde birden fazla bot süreci çalışacaksa Redis tercih edilmelidir:

```python
from aiogram.fsm.storage.redis import RedisStorage

storage = RedisStorage.from_url('redis://localhost:6379/0')
dp = Dispatcher(storage=storage)
```

Redis, farklı süreçlerin ortak durum verisine ulaşmasını sağlar. Bağlantı adresi kaynak koda gömülmemeli; ortam değişkeninden okunmalıdır. Telefon, parola veya kimlik numarası gibi hassas bilgiler FSM’de gereğinden uzun tutulmamalıdır.

Son olarak `/iptal` komutu ekleyip `state.clear()` çağırmak kullanıcıya güvenli bir çıkış sunar. Girdileri doğrulamak, beklenmeyen mesaj türlerini yakalamak ve tamamlanan akışları temizlemek; FSM’i yalnızca çalışan değil, dayanıklı bir konuşma altyapısına dönüştürür.
