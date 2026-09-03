---
layout: post
title: "Ansible ile Altyapı Otomasyonu: SSH Üzerinden Yüzlerce Sunucuyu Yönetmek"
math: true
categories: 
  - Bilgi
tags: 
  - ansible
  - devops
  - ssh
  - otomasyon
  - altyapı
image: /img/ansible-ile-altyapi-76.png
---

Sunucu sayısı arttıkça “şu paketi hepsine kurar mısın?” cümlesi küçük bir ricadan operasyonel bir maratona dönüşür. Ansible, SSH tabanlı ajanssız mimarisiyle bu maratonu tekrarlanabilir playbook’lara çevirir. Tek bir kontrol makinesinden yüzlerce Linux sunucusuna bağlantı kurabilir, yapılandırma uygulayabilir, servisleri yönetebilir ve uygulama dağıtımları gerçekleştirebilirsiniz.


![ansible-ile-altyapi-76](/img/ansible-ile-altyapi-76.svg)

``

Ansible’ın temelinde **control node** ve **managed node** ayrımı vardır. Control node, komutların ve playbook’ların çalıştırıldığı yönetim makinesidir. Managed node ise yönetilen hedef sunucudur. Hedefte sürekli çalışan bir Ansible ajanı bulunmaz; Ansible, SSH ile bağlanır, gerektiğinde geçici Python modüllerini çalıştırır ve sonucu geri alır. Bu yaklaşım, yeni bir sunucunun yönetim kapsamına alınmasını çoğu durumda SSH erişimi ve Python ile mümkün kılar.

Ajanssızlık, yalnızca kurulum kolaylığı değildir; saldırı yüzeyini ve sürüm uyuşmazlığı riskini de azaltır. Ancak güvenliği SSH anahtarları, ayrı otomasyon kullanıcıları, `sudo` yetkileri ve envanter gruplarıyla dikkatlice tasarlamak gerekir. Basitçe, toplam operasyon maliyetini şöyle düşünebiliriz:

$$T = n \times t_{manuel} \quad \Rightarrow \quad T_{ansible} \approx t_{yazım} + t_{çalıştırma}$$

Burada $n$ sunucu sayısıdır. Playbook hazırlama süresi başlangıçta yatırım gibi görünse de $n$ büyüdükçe manuel işlemlere göre ciddi zaman kazancı sağlar.

| Yaklaşım | Çalışma modeli | Güçlü yanı | Dikkat edilmesi gereken |
|---|---|---|---|
| Manuel SSH | Sunucuya tek tek giriş | Hızlı başlangıç | Hata ve tutarsızlık riski |
| Ajan tabanlı araçlar | Her hedefte servis/ajan | Sürekli raporlama | Ajan yaşam döngüsü yönetimi |
| Ansible | SSH ile isteğe bağlı bağlantı | Basit kurulum, okunabilir YAML | SSH erişimi ve envanter disiplini |

Ansible’da hedefler **inventory** dosyasında tanımlanır. Gruplama; web, veritabanı, test veya üretim gibi mantıksal sınırlar kurar. Örneğin aşağıdaki envanter, web sunucularını tek bir hedef kümesi halinde toplar:

```ini
[web]
web-01 ansible_host=10.10.0.11
web-02 ansible_host=10.10.0.12
web-03 ansible_host=10.10.0.13

[web:vars]
ansible_user=deploy
ansible_ssh_private_key_file=~/.ssh/ansible_ed25519
```

Asıl sihir playbook’larda gerçekleşir. Playbook, istenen son durumu tarif eder; yani “Nginx kurulu ve çalışıyor olsun” dersiniz. Bu, komutların körlemesine tekrar edilmesinden daha güvenlidir. Ansible modüllerinin çoğu **idempotent** davranır: Aynı playbook tekrar çalıştırıldığında, hedef durum zaten sağlanmışsa gereksiz değişiklik yapılmaz.

```yaml
---
- name: Web katmanını hazırla
  hosts: web
  become: true
  serial: 25%
  tasks:
    - name: Nginx paketini kur
      ansible.builtin.apt:
        name: nginx
        state: present
        update_cache: true

    - name: Uygulama yapılandırmasını kopyala
      ansible.builtin.template:
        src: templates/site.conf.j2
        dest: /etc/nginx/sites-available/site.conf
        mode: "0644"
      notify: Nginx'i yeniden yükle

  handlers:
    - name: Nginx'i yeniden yükle
      ansible.builtin.service:
        name: nginx
        state: reloaded
```

Bu örnekte `serial: 25%`, yüzlerce sunucuda kontrollü dağıtım sağlar: tüm filoyu aynı anda riske atmak yerine hedeflerin dörtte biriyle ilerlenir. `template` görevi yalnızca dosya gerçekten değiştiğinde handler’ı tetikler; böylece gereksiz servis yeniden başlatmaları önlenir.

Ölçek büyüdüğünde envanteri statik dosyalar yerine bulut sağlayıcılarının dinamik envanter eklentilerinden üretmek mantıklıdır. Parolaları ise playbook içine yazmak yerine **Ansible Vault** ile şifrelemek gerekir. Son olarak önce `--check --diff` ile kuru çalışma yapın, ardından canary grup üzerinde deneyin. Ansible’ın gücü “aynı komutu çok yere göndermekten” değil, altyapıyı sürümlenebilir, denetlenebilir ve tekrar üretilebilir bir ürün gibi ele almaktan gelir.
