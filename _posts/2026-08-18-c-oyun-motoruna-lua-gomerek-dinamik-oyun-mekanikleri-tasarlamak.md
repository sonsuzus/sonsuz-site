---
layout: post
title: "C++ Oyun Motoruna Lua Gömerek Dinamik Oyun Mekanikleri Tasarlamak"
math: true
categories: 
  - Program
tags: 
  - Lua
  - C++
  - Oyun Geliştirme
  - Scripting
  - Game Engine
---

Bir oyunun tüm kurallarını C++ ile derlemek hızlıdır; ancak zıplama yüksekliği, düşman davranışı veya görev ödülleri için her değişiklikte motoru yeniden derlemek üretim hızını düşürür. Lua, hafif çalışma zamanı ve sade sözdizimiyle bu sorunu çözer: performans kritik çekirdek C++ içinde kalırken, tasarımcıların sık değiştirdiği oyun mantığı betiklere taşınır.
``

## Neden gömülü betik sistemi?

Gömülü scripting yaklaşımında Lua ayrı bir uygulama değildir; oyun motorunuzun işlemi içinde çalışan bir yorumlayıcıdır. Motor, dünyadaki nesneleri ve güvenli API fonksiyonlarını Lua'ya açar. Lua da bu fonksiyonları kullanarak sahne olaylarına tepki verir. Böylece **motor**, fizik, çizim ve bellek yönetimini üstlenir; **betikler** ise kuralları tanımlar.

Bu ayrımın teorik temeli sorumlulukların ayrılmasıdır. Toplam geliştirme maliyetini kabaca $T = T_{derleme} + T_{test} + T_{iterasyon}$ olarak düşünelim. Her küçük dengeleme değişikliğinde C++ derlemek $T_{derleme}$ maliyetini yükseltir. Lua dosyasını yeniden yüklemek ise iterasyon döngüsünü belirgin biçimde kısaltır. Elbette yorumlanan kodun çağrı maliyeti vardır; bu nedenle binlerce nesnenin fizik hesabını Lua'ya taşımak iyi bir fikir değildir.

| Katman | C++ için uygun işler | Lua için uygun işler |
|---|---|---|
| Performans | Fizik, pathfinding, render | Basit karar kuralları |
| Değişim sıklığı | Nadir değişen altyapı | Denge, görev ve diyalog |
| Erişim | Donanım ve motor belleği | Sınırlandırılmış oyun API'si |
| Hata etkisi | Kritik sistem hataları | Kontrollü betik hataları |

## Lua durumunu oluşturmak

C++ tarafında `lua_State`, Lua sanal makinesini temsil eder. Standart kütüphaneleri açmak prototip geliştirmeyi kolaylaştırır; fakat yayın sürümünde `io` veya `os` gibi dosya sistemi erişimi veren kütüphaneleri kapatmak daha güvenlidir.

```cpp
#include <lua.hpp>

lua_State* L = luaL_newstate();
luaL_openlibs(L);

if (luaL_dofile(L, "scripts/player.lua") != LUA_OK) {
    std::cerr << "Lua hatası: " << lua_tostring(L, -1) << "\n";
    lua_pop(L, 1);
}
```

Bu kod `player.lua` dosyasını yükler ve çalıştırır. Hata mesajı Lua yığınının en üstünde bulunur; `lua_pop` çağrısı, sonraki işlemlerde yığının kirlenmesini engeller. Oyuncu hareketini C++ içinde tutup hasar kuralını Lua'ya vermek yaygın bir hibrittir.

## C++ fonksiyonunu Lua'ya açmak

Aşağıdaki köprü fonksiyonu, Lua'nın güvenli biçimde hasar uygulamasını sağlar. Lua doğrudan oyuncu belleğine erişmez; yalnızca motorun sunduğu kapıdan geçer.

```cpp
int ApplyDamage(lua_State* L) {
    int entityId = static_cast<int>(luaL_checkinteger(L, 1));
    float amount = static_cast<float>(luaL_checknumber(L, 2));
    GameWorld::Get().Damage(entityId, std::max(0.0f, amount));
    return 0;
}

lua_register(L, "ApplyDamage", ApplyDamage);
```

Lua tarafında kullanım son derece okunaktır:

```lua
function on_enemy_hit(playerId, enemyLevel)
  local damage = 8 + enemyLevel * 2
  ApplyDamage(playerId, damage)
end
```

Burada `luaL_checkinteger` ve `luaL_checknumber` kritik güvenlik araçlarıdır: yanlış tür gönderildiğinde belirsiz davranış yerine anlamlı Lua hatası üretir. Tasarım formülü $hasar = 8 + 2 \times seviye$ olarak betikte görünür olduğu için dengeleme toplantılarında doğrudan tartışılabilir.

## Yaşam döngüsü, hata ve hot reload

Her karede Lua dosyasını diskten okumayın. Bunun yerine betikleri yükleme anında derleyin, `update(dt)` gibi fonksiyonları çağırın ve yalnızca dosya değiştiğinde yeniden yükleyin. Yeniden yüklemeden önce oyuncu envanteri gibi kalıcı verileri C++ tarafında tutmak, betik yenilense bile oyun durumunun korunmasını sağlar.

Bir diğer önemli konu hata izolasyonudur. `lua_call` yerine `lua_pcall` kullanmak, bozuk bir görev betiğinin tüm oyunu çökertmesini önler. Hata mesajını dosya adı, satır numarası ve nesne kimliğiyle kaydetmek, "büyü neden çalışmadı?" sorusunu dakikalar yerine saniyelerde yanıtlar.

Sonuç olarak Lua, C++ motorun yerine geçen bir teknoloji değil, onun çevikliğini artıran bir ortak katmandır. Doğru API sınırları, kontrollü hata yönetimi ve performans ölçümüyle; oyun mekaniklerini derleme kuyruğuna takılmadan güvenle deneyebilirsiniz.
