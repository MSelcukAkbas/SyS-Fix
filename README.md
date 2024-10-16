
# System Maintenance Tool

## Overview
`SystemMaintenance` sınıfı, Windows işletim sistemlerinde sistem bilgilerini toplamak ve bakımlarını yapmak için kullanılan bir Python uygulamasıdır. Uygulama, CPU, RAM, disk bilgileri gibi sistem bilgilerini alır ve gerektiğinde hata kaydı tutar. Ayrıca, kullanıcı dostu bir arayüz ile bu bilgileri dışa aktarma imkanı sunar.

## Features
- **Sistem Bilgisi Alma**: İşlemci, RAM, grafik kartı ve depolama bilgilerini toplar.
- **Hata Kaydı Tutma**: Uygulama sırasında meydana gelen hataları kaydeder.
- **Dışa Aktarma**: Toplanan sistem bilgilerini bir dosyaya dışa aktarma imkanı sağlar.
- **Güncelleme**: `winget` kullanarak sistemdeki uygulamaları günceller.
- **Kullanıcı Dostu Arayüz**: Bilgilerin gösterimi ve kullanıcı etkileşimi için kolay bir arayüz sunar.

## Requirements
- Python 3.x
- `psutil` kütüphanesi: Sistem bilgilerini almak için kullanılır. (Kurulum için: `pip install psutil`)
- `wmi` kütüphanesi: Windows Management Instrumentation ile etkileşim için kullanılır. (Kurulum için: `pip install WMI`)

## Usage
1. Projeyi klonlayın veya indirin.

2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install psutil WMI
   ```
3. Uygulamayı çalıştırın:
   ```bash
   python SYS_FİX_v3.py
   ```

## Notes
- Bu uygulama sadece Windows platformunda çalışmaktadır.
- Kullanıcı izinleri gerektirebilir, bu nedenle yönetici olarak çalıştırılması önerilir.

## Katkıda Bulunma

Herhangi bir öneri veya katkıda bulunmak isterseniz, lütfen aşağıdan iletişime geçin.

- E-posta: [akbasselcuk32@gmail.com](mailto:akbasselcuk32@gmail.com)
- LinkedIn: [Mustafa Selçuk Akbaş](https://linkedin.com/in/mustafa-selcuk-akbas)
