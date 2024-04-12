import wx
from SYS_FİX_v3 import SystemMaintenance as sys_process

class SystemMaintenance_Gui(wx.Frame):

    def __init__(self, *args, **kw):
        """
        Sınıfın başlatıcı metodudur. 
        SystemMaintenance sınıfı ile bağlantı kurarak gerekli bilgileri çeker.
        """
        super(SystemMaintenance_Gui, self).__init__(*args, **kw)

        self.sys = sys_process()
        renk = self.sys.renk_kontrol()
        self.dil_paketi = self.sys.dil_kontrol()
        self.icon_path = self.sys.icon_path

        self.SetTitle("SYS-FİX-3")

        boyut = (405, 350)
        pozisyon = (560, 150)

        self.SetSize(boyut)
        self.SetSizeHints(*boyut)
        self.SetPosition(pozisyon)

        self.Center()
        self.SetBackgroundColour(renk)

        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)
        
        self.icon = wx.Icon(self.icon_path, wx.BITMAP_TYPE_PNG) 
        self.SetIcon(self.icon)

        self.menubar = wx.MenuBar()
        self.pencere_menü = wx.Menu()

        self.sistem_bilgi_item = self.pencere_menü.Append(-1, self.dil_paketi['Sistem'])
        self.Bind(wx.EVT_MENU, self.sistem_bilgi_gui, self.sistem_bilgi_item)

        self.hata_kayitlari_item = self.pencere_menü.Append(-1, self.dil_paketi['hata'])
        self.Bind(wx.EVT_MENU, self.Hata_erişim_Gui, self.hata_kayitlari_item)

        self.Tema = self.pencere_menü.Append(-1, self.dil_paketi['tema'])
        self.Bind(wx.EVT_MENU, self.Tema_ayarlama, self.Tema)

        self.language = self.pencere_menü.Append(-1, self.dil_paketi['dil'])
        self.Bind(wx.EVT_MENU, self.dil_degistir, self.language)


        self.kapat_item = self.pencere_menü.Append(wx.ID_EXIT, self.dil_paketi['kapat'])
        self.Bind(wx.EVT_MENU, self.sys.kapat, self.kapat_item)

        self.menubar.Append(self.pencere_menü, self.dil_paketi['menü'])
        self.SetMenuBar(self.menubar)

        self.Arayuz_oluştur()

    def Arayuz_oluştur(self):
        """
            Kullanıcı arayüzünü oluşturan fonksiyon.
        """
        panel = wx.Panel(self)

        self.baslik_etiket = wx.StaticText(panel, label=self.dil_paketi['sorun_cozucu_araclar'], pos=(100, 20), size=(200, -1))
        self.baslik_etiket.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        self.guncelleme_btn = wx.Button(panel, label=self.dil_paketi['guncelleme_denetleme'], pos=(50, 70), size=(300, -1))
        self.guncelleme_btn.Bind(wx.EVT_BUTTON, lambda event: self.sys.Arka_p(self.sys.guncelleme_yukle))
        self.guncelleme_btn.SetToolTip(self.dil_paketi["bilgisayar_guncelleme_mesaji"])

        self.internet_ayarı_btn = wx.Button(panel, label=self.dil_paketi['ping_sorunu_cozme'], pos=(50, 110), size=(300, -1))
        self.internet_ayarı_btn.Bind(wx.EVT_BUTTON, lambda event: self.sys.Arka_p(self.sys.internet_ayarı))
        self.internet_ayarı_btn.SetToolTip(self.dil_paketi["internet_baglanti_mesaji"])

        self.disk_temizleme_buton = wx.Button(panel, label=self.dil_paketi['disk_temizleme'], pos=(50, 150), size=(300, -1))
        self.disk_temizleme_buton.Bind(wx.EVT_BUTTON, lambda event: self.sys.Arka_p(self.sys.disk_temizleme))
        self.disk_temizleme_buton.SetToolTip(self.dil_paketi["disk_temizleme_mesaji"])

        self.disk_denetimi_buton = wx.Button(panel, label=self.dil_paketi['disk_denetimi'], pos=(50, 190), size=(300, -1))
        self.disk_denetimi_buton.Bind(wx.EVT_BUTTON, lambda event: self.sys.Arka_p(fonksiyon=self.sys.Dosya_Denetim))
        self.disk_denetimi_buton.SetToolTip(self.dil_paketi["disk_denetimi_mesaji"])

        self.Yüksek_tus = wx.Button(panel, label=self.dil_paketi["yuksek_guc"], pos=(50, 240), size=(75, -1))
        self.Yüksek_tus.Bind(wx.EVT_BUTTON, lambda event: self.sys.guc_planı("Yüksek"))
        self.Yüksek_tus.SetToolTip(self.dil_paketi['yuksek_guc_mesaj'])

        self.Normal_tus = wx.Button(panel, label=self.dil_paketi["normal_guc"], pos=(160, 240), size=(75, -1))
        self.Normal_tus.Bind(wx.EVT_BUTTON, lambda event: self.sys.guc_planı("normal"))
        self.Normal_tus.SetToolTip(self.dil_paketi['normal_guc_mesaji'])

        self.Düşük_tus = wx.Button(panel, label=self.dil_paketi["dusuk_guc"], pos=(270, 240), size=(75, -1))
        self.Düşük_tus.Bind(wx.EVT_BUTTON, lambda event: self.sys.guc_planı("Düşük"))
        self.Düşük_tus.SetToolTip(self.dil_paketi['dusuk_guc_mesaji'])

        panel.Layout()

    def Tema_ayarlama(self, event):
        """
            Tema değiştirmek için kullanılan fonksiyon.
        """
        renk = wx.ColourDialog(self)
        if renk.ShowModal() == wx.ID_OK:
            sa = renk.GetColourData().GetColour()
            json_veri ={
                            "renk": '#{:02x}{:02x}{:02x}'.format(*sa[:3])
                        }
            self.sys.jsona_yaz(json_veri, tur = "renk")
            self.SetBackgroundColour(sa)
            self.Refresh(True)

        renk.Destroy()

    def dil_degistir(self, event):
        """
            Dil değiştirmek için kullanılan fonksiyon.
        """
        dil_secenekleri = {'İngilizce': 'English', 'Türkçe': 'Turkish'}
        secilen_dil = wx.GetSingleChoice('Lütfen bir dil seçin/Pleas select', 'Dil Seçimi', list(dil_secenekleri.keys()))
        if secilen_dil:
            json_veri ={
                    "Dil": dil_secenekleri[secilen_dil]
                    }
            self.sys.jsona_yaz(json_veri, tur = "dil")
            wx.MessageBox('Dil değiştirme işlemi başarıyla gerçekleştirildi. Uygulamayı yeniden başlatmanız gerekebilir.',
                        'Bilgi', wx.OK | wx.ICON_INFORMATION)
            self.sys.kapat("")
            
    def sistem_bilgi_gui(self, event):
        """
            Sistem bilgilerini grafik arayüzde göstermek için kullanılan fonksiyon.
        """
        app = wx.App(False)
        frame = wx.Frame(None, title=self.dil_paketi['Sistem'], size=(405, 416))
        panel = wx.Panel(frame)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        icon = wx.Icon(self.icon_path, wx.BITMAP_TYPE_PNG) 
        frame.SetIcon(icon)

        text_widget = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(400, 400))
        text_widget.SetValue(self.sys.sistem_text)
        
        vbox.Add(text_widget, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        dışa_aktar_menu = file_menu.Append(wx.ID_ANY, self.dil_paketi['dışarı'], "Sistem bilgilerini dışa aktar")
        frame.Bind(wx.EVT_MENU, lambda event: self.sys.Sistem_bilgi_dısa_aktar(self.sys.sistem_text), dışa_aktar_menu)
        menu_bar.Append(file_menu, self.dil_paketi['menü'])
        frame.SetMenuBar(menu_bar)
        
        panel.SetSizer(vbox)
        frame.Show()
        app.MainLoop()

    def Hata_erişim_Gui(self, event):
        """
            Uygulama Hatalarını grafik arayüzde göstermek için kullanılan fonksiyon.
        """
        try:
            with open(self.sys.hata_path, "r+", encoding="utf-8") as hatalar:
                kayıtlar = hatalar.read()
                if not kayıtlar:
                    hatalar.write(" ")
                    hatalar.seek(0)
                    kayıtlar = hatalar.read()
                Toplam_hata = str((len(kayıtlar.split("\n")) / 2).__round__()) + "\n\n"

            hata_erisim_frame = wx.Frame(None, title=f"Toplam hata kaydı : {Toplam_hata}", size=(600, 400))
            panel = wx.Panel(hata_erisim_frame)
            sizer = wx.BoxSizer(wx.VERTICAL)

            text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
            text_ctrl.SetValue(kayıtlar)
            sizer.Add(text_ctrl, 1, wx.EXPAND | wx.ALL, 5)

            panel.SetSizer(sizer)
            hata_erisim_frame.Show()

        except Exception as e:
            self.sys.hata_kayit(f"Hata: {e}")
            return

if __name__ == '__main__':
    app = wx.App(False)
    frame = SystemMaintenance_Gui(None)
    frame.Show(True)
    app.MainLoop()