from wx import LogError ,OK ,ICON_INFORMATION ,MessageBox ,ID_OK ,DirDialog
from subprocess import run, check_output, PIPE, CalledProcessError, TimeoutExpired, Popen
from threading import Thread
from os import makedirs
from os.path import join, expanduser ,exists ,dirname ,abspath
from platform import release, system ,version
from sys import exit
from psutil import virtual_memory, disk_partitions, disk_usage ,cpu_freq ,cpu_count # pip install psutil
from wmi import WMI 
import json

class SystemMaintenance():
    def __init__(self):
        """
            Sınıfın başlatıcı metodudur. 
            Hata Path:
                Hata durumunda Kayıt edilecek argümanların , kayıt komununu belirtir.
                varsayılan hali programın çalıştığı dizindir.
            
            Doğrulama :
                Programın çalıştığı platform windows olması gereklidir.
        """
        if system() != 'Windows':
            LogError("Bu Program Sadece Windows Platformunda Çalışmaktadır")
            LogError("Diğer platformlarla uyumlu değildir ve çalıştırılamaz.")
            LogError("Farklı bir işletim sistemi kullanıyorsanız, bu uygulamanın çalıştırılması mümkün değildir.")
            exit()

        exe_dizini = dirname(abspath(__file__))
        ikon_adi = "icon.png"
        self.icon_path = join(exe_dizini, ikon_adi)

        appdata = join(expanduser('~'), 'AppData', 'Local', 'SyS-FiX')
        makedirs(appdata, exist_ok=True)
        self.renk_path = join(appdata, 'Renk_data.json')
        self.language_path = join(appdata, 'language_data.json')
        self.hata_path = join(appdata, 'hata-kayitlari.txt')
        self.sistem_kayıt_path = join(appdata, 'sistem_bilgileri.txt')

        self.Arka_p(self.sistem_bilgi_thread)

    def hata_kayit(self, hata_mesaji):
        try:
            with open(self.hata_path, "a", encoding="utf-8") as dosya:
                dosya.write("\n" + hata_mesaji + "\n")
                LogError(hata_mesaji)
        except Exception as e:
            LogError(f"Hata kayıt sırasında bir hata oluştu: {e}")

    def kapat(self, event):
        """
            Uygulama kapatma işlemini gerçekleştirir.
        """
        try:
            exit()
        except Exception as e:
            self.hata_kayit(f"Kapatma sırasında bir hata oluştu: {e}")

    def Arka_p(self, fonksiyon, *args):
        thread = Thread(target=fonksiyon, args=args)
        thread.daemon = True
        thread.start()

    def sistem_bilgi_thread(self):
        """
            Sistem bilgisini almak için ek iş parçacığı kullanılan fonksiyon.
            Eğer sistem bilgisi dosyası mevcut değilse, sistem bilgisi dosyası oluşturulur.
            Eğer daha önceden sistem bilgisi dosyası oluşturulmuşsa, sistem bilgisi dosyası okunur.
        """
        if exists(self.sistem_kayıt_path):
            with open(self.sistem_kayıt_path, "r", encoding="utf-8") as dosya:
                self.sistem_text = dosya.read()
        else: 
            self.sistem_text = self.Sistem_Bilgi()
            if self.sistem_text:
                self.sistem_bilgi_yaz_txt(self.sistem_text)

    def Sistem_Bilgi(self):
        """
        Sistem bilgisini almak için kullanılan fonksiyon.
        İşlemci modeli, maksimum hız, fiziksel bellek miktarı ve boş bellek miktarı döndürülür.
        """
        komutlar = {
        "cpu_model" : "wmic cpu get name",
        "cpu_mimari" : "wmic cpu get caption",
        "cpu_max_speed" : "wmic cpu get maxclockspeed",
        "grafik_kartı_bilgi":"wmic path win32_videocontroller get caption" ,
        "Bellektop": ['powershell', '-Command', 'systeminfo | findstr /C:"Total Physical Memory"'],
        "bellekBoş": ['powershell', '-Command', 'wmic OS get FreePhysicalMemory'],
        "Depolama" : ['powershell', '-Command', 'wmic logicaldisk get DeviceID,VolumeName,Size,FreeSpace,FileSystem']}
        try:
            def Check_komut(Komut=None):
                try :
                    bilgi = str(check_output(Komut, shell=True).decode('utf-8'))
                    return bilgi
                except Exception as exc:
                    hata_mesaji =f"Beklenmeyen bir hata oluştu : {exc}"
                    self.hata_kayit(hata_mesaji=hata_mesaji) 
                    return "Bilgi alınmadı" 
                
            def isletim_sistem():
                try:
                    pc = WMI()
                    isletim_sistem = pc.Win32_OperatingSystem()[0]
                    isletim_sistem = isletim_sistem.Caption
                    return isletim_sistem
                except:
                    try:
                        isletim_sistem =system()+" " +release() +" "+version()
                        return isletim_sistem
                    except Exception as e:
                        isletim_sistem = "Bilgi alınamadı: " + str(e)
                
            def cpu_gpu_bilgisi_al():
                try:
                    ıslemci_çekirdek=str(cpu_count()) + " Çekirdek"
                except Exception as e:
                    ıslemci_çekirdek = "Bilgi alınamadı: " + str(e)
                try:
                    pc =WMI()
                    cpu_model = pc.Win32_Processor()[0].Name
                except :
                    try :
                        cpu_model = Check_komut(Komut=komutlar["cpu_model"]).strip().split('\n')[1].strip()
                    except Exception as e:
                        cpu_model = "Bilgi alınamadı: " + str(e)
                try:
                    cpu_mimari =  Check_komut(Komut=komutlar["cpu_mimari"])[42:].strip()
                except Exception as e:
                    cpu_mimari = "Bilgi alınamadı: " + str(e)
                try:
                    cpu_max_speed = cpu_freq().max + " GHz"
                except :
                    try:
                        cpu_max_speed = str(int(Check_komut(Komut=komutlar["cpu_max_speed"]).strip().split('\n')[1]) / 1000) + " GHz".strip()
                    except Exception as e:
                        cpu_max_speed = "Bilgi alınamadı: " + str(e)
                try:
                    grafik_kartı_bilgi = Check_komut(Komut=komutlar["grafik_kartı_bilgi"])[30:].strip()
                    grafik_kartı_bilgi ="\n".join([f" - {gpu_name.strip()}" for gpu_name in grafik_kartı_bilgi.split('\n')]) 
                except:
                    try:
                        pc =WMI()
                        grafik_kartı_bilgi = "-"+ str(pc.Win32_VideoController()[0].Name)
                    except Exception as e:
                        grafik_kartı_bilgi = "Bilgi alınamadı: " + str(e)

                return cpu_model,ıslemci_çekirdek ,cpu_mimari, cpu_max_speed, grafik_kartı_bilgi
            
            def ram_bilgisi_al():
                try:
                    ram = virtual_memory()
                    toplam = str(ram.total // (1024 ** 2))+ " MB"
                    kullanılabilir = str(ram.available // (1024 ** 2))
                except :
                    try:
                        toplam= Check_komut(komutlar["Bellektop"])[26:] 
                        kullanılabilir =str((float(Check_komut(komutlar["bellekBoş"])[22:]) / 1000).__round__() )
                        return toplam, kullanılabilir
                    except Exception as e:
                        toplam= "Bilgi alınamadı: " + str(e)
                        kullanılabilir = "Bilgi alınamadı: " + str(e)
                        return toplam, kullanılabilir
                return toplam, kullanılabilir
            
            def depolama_bilgisi_al():
                try:
                    depolama_bilgileri = {}
                    for bölüm in disk_partitions():
                        bölüm_kullanımı = disk_usage(bölüm.mountpoint)
                        toplam_alan = bölüm_kullanımı.total // (1024 ** 3)
                        boş_alan = bölüm_kullanımı.free // (1024 ** 3)
                        depolama_bilgileri[bölüm.device.strip()] = toplam_alan, boş_alan
                        parçalı = "\n".join([f"- Cihaz: {cihaz}\n   Toplam Alan: {toplam_alanlar} GB\n   Boş Alan: {Bos_alanlar} GB" for cihaz, (toplam_alanlar, Bos_alanlar) in depolama_bilgileri.items()]) 
                    return parçalı
                except :
                    try:
                        depolama = Check_komut(komutlar["Depolama"]).strip()
                        depolama_bilgi = depolama.strip()[70:120].split()
                        depolama_biçim = depolama_bilgi[0]
                        depolama_bos_alan = str((float(depolama_bilgi[1]) / 1024000).__round__()) + " MB"
                        depolama_toplam_alan = str((float(depolama_bilgi[2]) / 1024000).__round__()) +" MB"
                        depolama= ("-Cihaz: C:\\"
                                f"\n--Depolama Biçimi: {depolama_biçim} "
                                f"\n--Depolama Toplam Alan: {depolama_toplam_alan}"
                                f"\n--Depolama Boş Alan: {depolama_bos_alan}  ")
                        return depolama
                    except:
                        pass
                    
            isletim_sistemi = isletim_sistem()
            cpu_model,ıslemci_çekirdek, cpu_mimari, cpu_max_speed, grafik_kartı_bilgi = cpu_gpu_bilgisi_al()
            toplam_ram, kullanılabilir_ram = ram_bilgisi_al()
            depolama_bilgileri = depolama_bilgisi_al()

            if cpu_mimari != "" or cpu_model is not None :
                Sistem_text = ("Sistem Bilgileri:\n\n" +
                        f"İşletim sistemi : {isletim_sistemi}\n\n"+
                        f"İşlemci Mimarı: {cpu_mimari}\n" +
                        f"İşlemci Modeli: {cpu_model}\n" +
                        f"İşlemci Hızı: {cpu_max_speed}\n" +
                        f"İşlemci Çekirdek Sayısı: {ıslemci_çekirdek}\n\n" +
                        "Grafik Kartları:\n" +
                        f"{grafik_kartı_bilgi}  \n\n"+
                        f"Toplam RAM: {toplam_ram} \n" +
                        f"Boş RAM: {kullanılabilir_ram} MB\n\n" +
                        "Depolama Bilgisi:\n" +
                        depolama_bilgileri)
            return Sistem_text

        except CalledProcessError as e:
            self.hata_kayit(f"Hata: Bir işlem başlatılırken hata oluştu: {e}" )
            return None
        
        except Exception as e:
            self.hata_kayit(f"Beklenmeyen bir hata oluştu: {e}")  
            return None
        
    def sistem_bilgi_yaz_txt(self ,sistem_text):
        try:
            if sistem_text is not None:
                with open(self.sistem_kayıt_path, "w", encoding="utf-8") as dosya:
                    dosya.writelines(sistem_text)
        except Exception as e:
            self.hata_kayit(f"Sistem bilgileri dosyaya yazılırken bir hata oluştu: {e}")

    def Sistem_bilgi_dısa_aktar(self, event):
        try:
            Expo = DirDialog(None, "Klasör seç")
            if Expo.ShowModal() == ID_OK:
                klasor_yolu = Expo.GetPath()
                if klasor_yolu:
                    dosya_yolu = join(klasor_yolu, "sistem_bilgileri.txt")
                    with open(dosya_yolu, "w", encoding="utf-8") as dosya:
                        dosya.write(self.sistem_text)
                    MessageBox("Sistem bilgileri başarıyla dışa aktarıldı.", "Bilgi", OK | ICON_INFORMATION)
                else:
                    LogError("Klasör seçilmedi. Dışa aktarma işlemi iptal edildi.")
            Expo.Destroy()
        except Exception as e:
            self.hata_kayit(hata_mesaji=f"Dışa aktarma işlemi sırasında bir hata oluştu:\n{e}")
            
    def komut_runner(self , komut ,method_ismi=None,başarı_mesajı = None ,wifi_Adi= None ):
        """
        Verilen komutu çalıştırır ve başarı durumunda belirtilen mesajı gösterir.

        komut:
            komut (list veya str): Çalıştırılacak komut veya komutlar. 
            Birden fazla komut için liste kullanılmalıdır.

        Hatalar:
            PermissionError: Komutun çalıştırma izni yoksa.
            CalledProcessError: Komut hatalı çalışırsa.
            TimeoutExpired: Beklenenden uzun sürerse.

        Başarı Mesajı :
            Başarı mesajşarı gönderilen argümana göre 
            kullanıcıya gösterilebilir yada None dönebilir.

        """
        try:
            if method_ismi == "internet_ayarı":
                komutlar_list = komut
                SSID_name = 'NETSH WLAN SHOW INTERFACE | findstr /r "^....SSID"'
                p = Popen(SSID_name,shell=True,stderr=PIPE,stdout=PIPE)
                (out,err) = p.communicate()
                if p.returncode != 0 : self.hata_kayit( "Wifi İsmi alınamadı")
                else:
                    wifi_Adi = str(out)[31:-5] if out else None 
                for x, command in enumerate(komutlar_list, start=2):
                    run(command, capture_output=True)
                MessageBox(f"WİFİ Optimize Edildi\nWifi adı: {wifi_Adi}","Bilgi", OK | ICON_INFORMATION)

            elif method_ismi =="guc_planı" :
                p = Popen(komut,  text=True)

            elif (method_ismi != "guc_planı" and method_ismi != "internet_ayarı"):
                p = Popen(komut, stdout=PIPE, stderr=PIPE, shell=True)

            if method_ismi != "internet_ayarı"  and başarı_mesajı is not None :
                p.communicate() 
                if p.returncode == 0 :
                    MessageBox( başarı_mesajı,"Bilgi", OK | ICON_INFORMATION)

        except PermissionError as ex:
            self.hata_kayit(f"(Komut_runner)Belirtilen komutun çalıştırma izni yok: {ex}")  # parantez içi kod geliştirme aşaması için
        except CalledProcessError as cep:
            self.hata_kayit( f"(Komut_runner)İşlem Gerçekleşirken Beklenmeyen Bir Durum Oluştu: {cep}") # parantez içi kod geliştirme aşaması için
        except TimeoutExpired as ti:
            self.hata_kayit( f"(Komut_runner)İşlem Gereğinden fazla sürdü: {ti}")  # parantez içi kod geliştirme aşaması için
        except Exception as on:
            self.hata_kayit(f"(Komut_runner)Program çalışırken bir hata ile karşılaştı: {on}")  # parantez içi kod geliştirme aşaması için
    
    def guncelleme_yukle(self ,event = None):
        """
            Güncelleme işlemini başlatan fonksiyon.
        """
        komutlar = {
        "winget" : ['powershell', '-Command', 'Start-Process winget -ArgumentList \'upgrade\', \'--all\' -Verb RunAs -WindowStyle Hidden'] } #Güncelleme
                
        self.komut_runner(komut=komutlar["winget"],method_ismi="winget" ,başarı_mesajı= "Güncelleme İşlemi Başlatıldı")

    def guc_planı(self, plan_ayarları):
        """
            Güç Planı Değiştirme işlemini başlatan fonksiyon.
        """

        if plan_ayarları == "Yüksek" : 
            komut  = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"  
        elif plan_ayarları == "normal":
            komut  = "381b4222-f694-41f0-9685-ff5bb260df2e" 
        else :
            komut ="a1841308-3541-4fab-bc81-f71556f20b4a"
    
        self.komut_runner(komut=f'powercfg -setactive {komut}',method_ismi="guc_planı" ,başarı_mesajı=f"Güç Planı Değiştirildi: {plan_ayarları} Güç Modu")

    def internet_ayarı(self,event = None):
        """
            İnternet ayarlarını sıfırlama işlemini gerçekleştiren fonksiyon.
        """
        komutlar = {
        "ipconfig": [['cmd', '/c', "start /b", 'ipconfig', '/flushdns'],
                    ['cmd', '/c', "start /b", 'ipconfig', '/release'], # Wİfi optimizasyon
                    ['cmd', '/c', "start /b", 'ipconfig', '/renew']]}
                
        self.komut_runner(komut=komutlar["ipconfig"] ,method_ismi="internet_ayarı")

    def Dosya_Denetim(self,event = None):
        """
            Windows dosya denetimi için 'sfc /scannow' ve 'dism /online /cleanup-image /startcomponentcleanup' 
            komutlarını yönetici yetkileriyle başlatır ve dosya denetim işlemlerini gerçekleştirir.
        """
        komutlar = {
        "sfc" : ['powershell', '-Command', 'Start-Process cmd -ArgumentList \'/c\', \'sfc /scannow\' -Verb RunAs -WindowStyle Hidden'],  # Disk denetimi
        "dism_cleanup" : ['powershell', '-Command', 'Start-Process dism -ArgumentList \'/online /cleanup-image /startcomponentcleanup\' -Verb RunAs -WindowStyle Hidden' ] }  # Disk  Temizle
                
        self.komut_runner(komut=komutlar["sfc"] ,method_ismi="sfc")
        self.komut_runner(komut=komutlar["dism_cleanup"] ,method_ismi="dism_cleanup", başarı_mesajı="Dosya denetleme Başarı ile Başlatıldı.")

    def disk_temizleme(self,event = None):
        """
            Windowsta disk temizleme işlemleri için 'cleanmgr' ve 'dism /online /cleanup-image /restorehealth' komutlarını
            kullanır bu komutları yönetici yetkileriyle başlatır ve disk temizleme işlemlerini gerçekleştirir.
        """
        komutlar = {
        "dism_cleanup" : ['powershell', '-Command', 'Start-Process dism -ArgumentList \'/online /cleanup-image /startcomponentcleanup\' -Verb RunAs -WindowStyle Hidden'], # Disk  Temizle
        "cleanmgr" : ['powershell', '-Command', 'Start-Process cleanmgr -ArgumentList \'/sagerun:1\' -Verb RunAs -WindowStyle Hidden'] }# Disk  Temizle
                
        self.komut_runner(komut=komutlar["cleanmgr"] ,method_ismi="cleanmgr")
        self.komut_runner(komut=komutlar["dism_cleanup"] ,method_ismi="dism_cleanup", başarı_mesajı="Disk Temizleme Başarı ile Başlatıldı.")

    def jsona_yaz(self, veri ,tur):
        """
        Belirtilen dosyaya JSON formatında verilen veriyi yazan fonksiyon.
        """
        if tur == "renk" :
                
            with open(self.renk_path, 'w' ,encoding="utf-8") as json_dosyasi:
                json.dump(veri, json_dosyasi, indent=4)
        if tur == "dil" :
            with open(self.language_path, 'w' ,encoding="utf-8") as json_dosyasi:
                json.dump(veri, json_dosyasi, indent=4)
                
    def renk_kontrol(self):
        """
        Belirtilen JSON formatındaki veriyi okuyup Renk ayarlarını günceller
        """
        if exists(self.renk_path):
            with open(self.renk_path, "r" ,encoding="utf-8") as dosya:
                json_icerik = json.load(dosya)
                renk_degeri = json_icerik["renk"]
            return renk_degeri 
        else: 
            return "#f0f8ff"
            
    def dil_kontrol(self):
        """
        Belirtilen JSON formatındaki veriyi okuyup Dil ayarlarını günceller
        """
        tr = {
            "aç" : "Aç" ,
            "systepsi" :"SYS-FİX Arka Planda Çalışıyor",
            "dışarı" : "Dışarı Aktar",
            "menü": "menü",
            "tema": "Temayı Değiştir",
            "dil": "Dili Değiştir",
            "kapat": "kapat",
            "hata": "Hata Kayıtları", 
            "Sistem" : "Sistem Bilgisi",

            "sorun_cozucu_araclar":"Sorun Çözücü Araçlar",
            "guncelleme_denetleme": "Güncelleme Denetleme",
            "ping_sorunu_cozme": "Ping Sorununu Çözme",
            "disk_temizleme": "Disk Temizleme",
            "disk_denetimi": "Disk denetimi",
            "yuksek_guc": "Yüksek güç",
            "normal_guc": "Normal güç",
            "dusuk_guc": "Düşük güç",

            "bilgisayar_guncelleme_mesaji": "Bilgisayarınızdaki güncellemeleri denetlemek için tıklayın.",
            "internet_baglanti_mesaji": "İnternet bağlantısı sorunlarını gidermek için tıklayın.",
            "disk_temizleme_mesaji": "Bilgisayarınızın diskini temizlemek için tıklayın.",
            "disk_denetimi_mesaji": "Bilgisayarınızın diskini denetlemek için tıklayın.",
            "yuksek_guc_mesaj": "Yüksek performans güç planını etkinleştirmek için tıklayın.",
            "normal_guc_mesaji": "Normal performans güç planını etkinleştirmek için tıklayın.",
            "dusuk_guc_mesaji": "Düşük güç tüketim modunu etkinleştirmek için tıklayın."
        }
        en ={
            "aç" :"Open",
            "systepsi" :"SYS-FIX is running in the background" ,
            "dışarı" : "export" ,
            "menü" : "menu" ,
            "tema" : "Change theme" ,
            "dil"  : "language" ,
            "kapat" : "close" ,
            "hata" : "Error Logs",
            "Sistem" :  "System Information",

            "sorun_cozucu_araclar": "Problem Solver Tools",
            "guncelleme_denetleme": "Check for Updates",
            "ping_sorunu_cozme": "Resolve Ping Issues",
            "disk_temizleme": "Disk Cleanup",
            "disk_denetimi": "Disk Check",
            "yuksek_guc": "High Power",
            "normal_guc": "Normal Power",
            "dusuk_guc": "Low Power",
            
            "bilgisayar_guncelleme_mesaji": "Click to check for updates on your computer.",
            "internet_baglanti_mesaji": "Click to resolve internet connection issues.",
            "disk_temizleme_mesaji": "Click to clean your computer's disk.",
            "disk_denetimi_mesaji": "Click to check your computer's disk.",
            "yuksek_guc_mesaj": "Click to enable high-performance power plan.",
            "normal_guc_mesaji": "Click to enable normal performance power plan.",
            "dusuk_guc_mesaji": "Click to enable low power consumption mode."
        }
        
        if exists(self.language_path):
            with open(self.language_path, "r" ,encoding="utf-8") as dosya:
                veri = json.load(dosya)
                dil = veri["Dil"]
                if dil == "English":
                    return en
                else :
                    return tr
        else: 
            return tr

if __name__ == '__main__':
    frame = SystemMaintenance()