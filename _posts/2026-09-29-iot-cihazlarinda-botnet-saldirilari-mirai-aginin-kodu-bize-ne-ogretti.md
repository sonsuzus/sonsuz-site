---
layout: post
title: "IoT Cihazlarında Botnet Saldırıları: Mirai Ağının Kodu Bize Ne Öğretti?"
math: true
categories: 
  - Bilgi
tags: 
  - iot
  - mirai
  - botnet
  - ddos
  - siber güvenlik
  - ağ güvenliği
toc: true
image: /img/iot-cihazlarinda-botnet-92.png
---

![iot-cihazlarinda-botnet-92](/img/iot-cihazlarinda-botnet-92.svg)


Bir güvenlik kamerası ne kadar tehlikeli olabilir? Görüntü kaydetmek için tasarlanmış yüz binlerce cihaz, Mirai botnet'i sayesinde aynı anda trafik üretmeye başladığında cevap şaşırtıcıydı: İnternetin önemli servislerini sarsacak kadar. Mirai vakası, karmaşık açıklar yerine varsayılan parolaların, zayıf cihaz yönetiminin ve savunmasız bir ekosistemin nasıl devasa bir saldırı altyapısına dönüşebileceğini gösterdi.
``

## Mirai neden farklıydı?

2016'da görünür hâle gelen Mirai; kameralar, modemler ve DVR cihazları gibi internete açık IoT sistemlerini tarıyordu. Başlıca hedefi, Telnet servisinin kullandığı TCP 23 ve 2323 portlarıydı. Cihazın parolası üreticinin belirlediği varsayılan değerlerden biri olarak bırakılmışsa zararlı yazılım sisteme giriyor, uygun işlemci mimarisine ait bileşeni çalıştırıyor ve cihazı komuta-kontrol ağına bağlıyordu.

Mirai'nin başarısı ileri düzey bir parola kırma algoritmasından değil, ölçek ekonomisinden kaynaklanıyordu. Bir cihazın savunmasız olma olasılığı $p$, taranan cihaz sayısı $N$ ise beklenen kurban sayısı kabaca şöyledir:

$$E[B] = N \times p$$

Örneğin milyonlarca adres tarandığında $p$ çok küçük olsa bile sonuç on binlerce bottan oluşabilir. Botnet'lerin gücü, tek bir güçlü makineden değil, çok sayıda zayıf cihazın koordinasyonundan gelir.

## Mimarinin temel parçaları

Mirai'nin yayımlanan kaynak kodu, görevleri ayrılmış modüler bir yapı ortaya koydu:

1. **Tarayıcı:** Rastgele IPv4 adreslerini kontrol ederek erişilebilir IoT cihazları arıyordu.
2. **Raporlama servisi:** Olası hedeflerin adreslerini merkezi sisteme iletiyordu.
3. **Yükleyici:** Hedefin işlemci mimarisini belirleyip uygun çalıştırılabilir dosyayı gönderiyordu.
4. **Komuta-kontrol sunucusu:** Botlara ne zaman ve hangi hedefe trafik üreteceklerini bildiriyordu.
5. **Saldırı modülleri:** Farklı ağ protokollerini kullanarak yoğun trafik oluşturuyordu.

| Katman | Mirai'nin avantajı | Savunmacının karşılığı |
|---|---|---|
| Keşif | Otomatik ve geniş adres taraması | Gereksiz portları kapatmak |
| Erişim | Varsayılan parola sözlüğü | Benzersiz, güçlü kimlik bilgileri |
| Çalıştırma | Birden fazla CPU mimarisi | İmzalı yazılım ve güvenli önyükleme |
| Kontrol | Merkezi komut dağıtımı | Çıkış trafiği ve DNS izleme |
| DDoS | Çok sayıda dağıtık kaynak | Oran sınırlama ve trafik temizleme |

## DDoS gücü nasıl büyüdü?

Her botun saniyede ortalama $r$ bit trafik ürettiğini ve bot sayısının $B$ olduğunu düşünelim. Teorik toplam trafik:

$$T = B \times r$$

Cihaz başına bant genişliği düşük görünse bile $B$ yüz binlere ulaştığında toplam kapasite yüzlerce Gbps veya daha fazlasına çıkabilir. Üstelik trafik farklı ağlardan geldiği için yalnızca IP engellemek etkisizleşir; meşru kullanıcılarla botları ayırmak zorlaşır.

## Kendi cihazlarımızı güvenli biçimde denetlemek

Aşağıdaki Python örneği, yalnızca sahip olduğumuz cihazlarda riskli yönetim portlarının açık olup olmadığını kontrol eder. Parola denemesi yapmaz; basit bir envanter doğrulamasıdır.

```python
import socket

cihazlar = ["192.168.1.20", "192.168.1.21"]
riskli_portlar = [23, 2323]

for cihaz in cihazlar:
    for port in riskli_portlar:
        with socket.socket() as sock:
            sock.settimeout(0.5)
            acik = sock.connect_ex((cihaz, port)) == 0
            if acik:
                print(f"Uyarı: {cihaz}:{port} erişilebilir")
```

Kod, listedeki cihazlara kısa süreli TCP bağlantısı kurmayı dener. Açık port bulunması tek başına enfeksiyon kanıtı değildir; ancak Telnet'in kapatılması veya yalnızca yönetim ağına sınırlandırılması gerektiğini gösterir.

## Mirai'nin kalıcı dersleri

İlk kurulumda parola değiştirmeyi zorunlu kılmak, uzaktan yönetimi varsayılan olarak kapatmak ve otomatik güncelleme sunmak üreticinin sorumluluğudur. Kullanıcılar ise cihazları ayrı bir VLAN'a yerleştirmeli, UPnP'yi gerekmiyorsa kapatmalı ve destek süresi biten ürünleri değiştirmelidir.

Mirai bize saldırganların her zaman sofistike bir sıfırıncı gün açığına ihtiyaç duymadığını öğretti. Bazen internete açık bir Telnet servisi ve yıllardır değiştirilmeyen parola yeterlidir. IoT güvenliği bu nedenle tek cihazı değil; üretici, kullanıcı, ağ operatörü ve hizmet sağlayıcıdan oluşan bütün zinciri koruma problemidir.
