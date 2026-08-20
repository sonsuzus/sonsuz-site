---
layout: post
title: "Erlang ile Dağıtık Mesajlaşma Sistemi: Telekom Dayanıklılığıyla Anlık İletişim"
math: true
categories: 
  - Program
tags: 
  - erlang
  - dağıtık sistemler
  - mesajlaşma
  - otp
  - fault tolerance
toc: true
---

Anlık mesajlaşma sunucusu yazmak, ekrana iki baloncuk düşürmekten çok daha fazlasıdır: Kullanıcılar çevrimdışı olabilir, makineler kapanabilir, ağ paketleri kaybolabilir ve en kritik anda bir süreç çökebilir. Erlang tam bu kaosun içinden doğdu. Telekom santrallerinin yıllarca durmadan çalışması hedefiyle tasarlanan dil; hafif süreçler, mesaj geçirme, denetim ağaçları ve dağıtık düğümler sayesinde sohbet sistemlerine doğal bir dayanıklılık kazandırır.

``

Erlang'ın temel modeli **paylaşılan bellek yerine mesajlaşma**dır. Her kullanıcı oturumu veya sohbet odası bağımsız bir Erlang süreci olabilir. Süreçlerin belleği izoledir; dolayısıyla bir odadaki hatalı veri diğer odanın durumunu doğrudan bozmaz. Bu yaklaşımın ölçeklenme fikri kabaca $N$ kullanıcı için $N$ veya daha fazla hafif süreç oluşturabilmektir. Bir düğümdeki teorik işlem yükü $L = \lambda \times c$ olarak düşünülebilir; burada $\lambda$ saniyedeki mesaj sayısı, $c$ ise bir mesajın ortalama işleme maliyetidir. Yük yükseldiğinde odaları veya kullanıcıları başka düğümlere dağıtmak mümkündür.

## Neden Erlang ve OTP?

OTP (Open Telecom Platform), yalnızca bir kütüphane paketi değil, üretim ortamında hata yönetimi için bir mimari sözleşmedir. Temel ilke şudur: **Hataları tamamen engellemeye çalışma; onları küçük, denetlenebilir alanlara hapset ve iyileştir.** Bir süreç beklenmedik biçimde sonlandığında supervisor onu yeniden başlatabilir. Bu mekanizma, tek bir mesaj ayrıştırma hatasının tüm sunucuyu devirmesini önler.

| Geleneksel yaklaşım | Erlang/OTP yaklaşımı | Sonuç |
|---|---|---|
| Tek büyük sunucu süreci | Çok sayıda izole süreç | Hata etki alanı küçülür |
| `try/catch` ile her şeyi yutmak | Çökme, raporlama, supervisor ile yeniden başlatma | Hatalar görünür ve iyileştirilebilir |
| Paylaşılan durum kilitleri | Süreç posta kutuları | Yarış koşulları azalır |
| Elle servis yönetimi | Supervision tree | Öngörülebilir toparlanma |

Aşağıdaki örnek, bir sohbet odasının gelen mesajları üyelere yayınlayan basit bir `gen_server` davranışını gösterir. Gerçek sistemde üyelik, yetkilendirme ve kalıcı geçmiş ayrı süreçler veya servisler olmalıdır.

```erlang
-module(chat_room).
-behaviour(gen_server).

-export([start_link/1, join/2, send_message/3]).
-export([init/1, handle_cast/2, handle_call/3]).

start_link(RoomId) ->
    gen_server:start_link({local, RoomId}, ?MODULE, [], []).

join(RoomId, UserPid) ->
    gen_server:call(RoomId, {join, UserPid}).

send_message(RoomId, From, Text) ->
    gen_server:cast(RoomId, {message, From, Text}).

init([]) ->
    {ok, #{members => []}}.

handle_call({join, Pid}, _From, State = #{members := Members}) ->
    monitor(process, Pid),
    {reply, ok, State#{members => lists:usort([Pid | Members])}}.

handle_cast({message, From, Text}, State = #{members := Members}) ->
    [Pid ! {chat_message, From, Text} || Pid <- Members],
    {noreply, State}.
```

Burada `gen_server`, sürecin yaşam döngüsünü standartlaştırır. `monitor/2` çağrısı üyeyi izler; istemci kapanırsa `DOWN` mesajı işlenerek listeden çıkarılabilir. Böylece ölü bağlantılara sürekli mesaj yollamak yerine oturum temizliği yapılır.

## Çökme senaryosu ve dağıtım

Bir sohbet odası süreci çökerse supervisor onu yeniden başlatır; ancak yalnızca bellekte tutulan üyeler kaybolur. Bu nedenle geçici durum ile kalıcı durumu ayırmak gerekir. Mesaj geçmişi bir veritabanına, kullanıcı oturumları ise Redis veya Mnesia gibi bir katmana yazılabilir. Teslim garantisi için mesajlara kimlik verilir ve istemci teslim onayı gönderir. En az bir kez teslimatta yinelenen mesaj görülebileceğinden, istemci tarafı $id$ alanına göre idempotent davranmalıdır.

Dağıtık Erlang düğümleri birbirini `node@host` adlarıyla tanır ve uzak süreçlere yerelmiş gibi mesaj gönderebilir. Yine de ağ bölünmesini sihirli biçimde çözmez: bağlantı koptuğunda hangi tarafın doğru olduğuna dair bir politika gerekir. Kritik sohbet verisinde çoğunluk temelli kararlar, zaman aşımı ve yeniden bağlanınca senkronizasyon uygulanmalıdır.

Sonuçta Erlang'ın gücü, “asla çökmez” vaadinde değil; çöktüğünde küçük bir parçayı hızlıca ayağa kaldırıp hizmeti sürdürmesindedir. Telekom dünyasının bu disiplinini mesajlaşma sisteminize taşıdığınızda, kullanıcılar arka plandaki arızayı fark etmeden sohbet etmeye devam eder.
