import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
import threading
import time
from dataclasses import dataclass
from typing import List, Dict
import json
from datetime import datetime

@dataclass
class BalikParametreleri:
    """Balık parametreleri - Sadeleştirilmiş"""
    populasyon_sayisi: int = 100
    kirmizi_balik_orani: float = 0.5  # Başlangıçta kırmızı balık oranı (0.0-1.0)
    
    # Temel evrim parametreleri
    genetik_suruklenme: float = 0.1  # Rastgele değişim oranı (0.0-1.0)
    mutasyon_orani: float = 0.01     # Mutasyon oranı (0.0-0.1)
    
    # Popülasyon dinamikleri
    dogum_orani: float = 0.3         # Doğum oranı (0.0-1.0)
    olum_orani: float = 0.2          # Ölüm oranı (0.0-1.0)

class BalikBireyi:
    """Balık bireyini temsil eden sınıf"""
    def __init__(self, genotip: str, cinsiyet: str):
        self.genotip = genotip  # "KK", "KB", "BB"
        self.cinsiyet = cinsiyet  # "erkek", "disi"
        self.yas = 0
        self.hayatta = True
        self.ureme_sayisi = 0
        
    @property
    def fenotip(self):
        """Görünür renk"""
        if self.genotip in ["KK", "KB"]:
            return "kirmizi"
        else:
            return "beyaz"
    
    def fitness_hesapla(self, parametreler: BalikParametreleri):
        """Fitness değerini hesapla"""
        if self.genotip == "KK":
            return 1.0
        elif self.genotip == "KB":
            return 1.0
        else:  # BB
            return 1.0

class EvrimSimulasyonu:
    """Ana evrim simülasyonu sınıfı"""
    
    def __init__(self):
        self.parametreler = BalikParametreleri()
        self.populasyon: List[BalikBireyi] = []
        self.nesil = 0
        self.calisir = False
        
        # Veri takibi
        self.nesil_verileri = []
        self.populasyon_verileri = []
        self.allel_frekanslari = []
        self.fitness_verileri = []
        
        self.arayuz_olustur()
        
    def arayuz_olustur(self):
        """Tkinter arayüzünü oluştur"""
        self.root = tk.Tk()
        self.root.title("🐠 Profesyonel Balık Evrim Simülasyonu")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Ana çerçeveler
        kontrol_ana_cerceve = tk.Frame(self.root, bg='#e8e8e8', width=350)
        kontrol_ana_cerceve.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        kontrol_ana_cerceve.pack_propagate(False)
        
        # Scroll bar ile kontrol paneli
        self.canvas_scroll = tk.Canvas(kontrol_ana_cerceve, bg='#e8e8e8', width=330)
        scrollbar = tk.Scrollbar(kontrol_ana_cerceve, orient="vertical", command=self.canvas_scroll.yview)
        self.kontrol_cercevesi = tk.Frame(self.canvas_scroll, bg='#e8e8e8')
        
        self.kontrol_cercevesi.bind(
            "<Configure>",
            lambda e: self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all"))
        )
        
        self.canvas_scroll.create_window((0, 0), window=self.kontrol_cercevesi, anchor="nw")
        self.canvas_scroll.configure(yscrollcommand=scrollbar.set)
        
        self.canvas_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scroll
        def _on_mousewheel(event):
            self.canvas_scroll.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas_scroll.bind("<MouseWheel>", _on_mousewheel)
        
        # Sağ taraf için ana çerçeve
        sag_ana_cerceve = tk.Frame(self.root, bg='white')
        sag_ana_cerceve.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Üst kısım: Canlı balık simülasyonu
        self.balik_cercevesi = tk.Frame(sag_ana_cerceve, bg='lightblue', height=200)
        self.balik_cercevesi.pack(fill=tk.X, pady=(0, 5))
        self.balik_cercevesi.pack_propagate(False)
        
        # Alt kısım: Grafikler
        self.grafik_cercevesi = tk.Frame(sag_ana_cerceve, bg='white')
        self.grafik_cercevesi.pack(fill=tk.BOTH, expand=True)
        
        self.kontrol_paneli_olustur()
        self.balik_paneli_olustur()
        self.grafik_paneli_olustur()
        self.baslangic_populasyonu_olustur()
        self.grafikleri_guncelle()
        
    def kontrol_paneli_olustur(self):
        """Kontrol panelini oluştur"""
        # Başlık
        baslik = tk.Label(self.kontrol_cercevesi, text="🧬 Deney Tasarımı", 
                         font=("Arial", 16, "bold"), bg='#e8e8e8')
        baslik.pack(pady=10)
        
        # Popülasyon Demografisi
        demo_frame = tk.LabelFrame(self.kontrol_cercevesi, text="Popülasyon Demografisi", 
                                  font=("Arial", 12, "bold"), bg='#e8e8e8')
        demo_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Başlangıç boyutu
        self.boyut_var = tk.IntVar(value=self.parametreler.populasyon_sayisi)
        self.slider_olustur(demo_frame, "Başlangıç Boyutu", self.boyut_var, 50, 500, 
                           lambda v: setattr(self.parametreler, 'populasyon_sayisi', int(v)))
        
        # Kırmızı balık oranı
        self.kirmizi_balik_orani_var = tk.DoubleVar(value=self.parametreler.kirmizi_balik_orani)
        self.slider_olustur(demo_frame, "Kırmızı Balık Oranı", self.kirmizi_balik_orani_var, 0.0, 1.0,
                           lambda v: setattr(self.parametreler, 'kirmizi_balik_orani', float(v)), scale=100)
        
        # Evrimsel Parametreler
        evrim_frame = tk.LabelFrame(self.kontrol_cercevesi, text="Evrimsel Parametreler", 
                                   font=("Arial", 12, "bold"), bg='#e8e8e8')
        evrim_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Genetik Suruklenme
        genetik_suruklenme_subframe = tk.Frame(evrim_frame, bg='#e8e8e8')
        genetik_suruklenme_subframe.pack(fill=tk.X, pady=2)
        tk.Label(genetik_suruklenme_subframe, text="Genetik Suruklenme", font=("Arial", 10, "bold"), bg='#e8e8e8').pack()
        
        self.genetik_suruklenme_var = tk.DoubleVar(value=self.parametreler.genetik_suruklenme)
        self.slider_olustur(genetik_suruklenme_subframe, "Genetik Suruklenme", self.genetik_suruklenme_var, 0.0, 1.0,
                           lambda v: setattr(self.parametreler, 'genetik_suruklenme', float(v)), scale=100)
        
        # Mutasyon Oranı
        mutasyon_subframe = tk.Frame(evrim_frame, bg='#e8e8e8')
        mutasyon_subframe.pack(fill=tk.X, pady=2)
        tk.Label(mutasyon_subframe, text="Mutasyon Oranı", font=("Arial", 10, "bold"), bg='#e8e8e8').pack()
        
        self.mutasyon_orani_var = tk.DoubleVar(value=self.parametreler.mutasyon_orani)
        self.slider_olustur(mutasyon_subframe, "Mutasyon Oranı", self.mutasyon_orani_var, 0.0, 0.1,
                           lambda v: setattr(self.parametreler, 'mutasyon_orani', float(v)), scale=100)
        
        # Popülasyon Dinamikleri
        pop_subframe = tk.Frame(evrim_frame, bg='#e8e8e8')
        pop_subframe.pack(fill=tk.X, pady=2)
        tk.Label(pop_subframe, text="Popülasyon Dinamikleri", font=("Arial", 10, "bold"), bg='#e8e8e8').pack()
        
        self.dogum_orani_var = tk.DoubleVar(value=self.parametreler.dogum_orani)
        self.slider_olustur(pop_subframe, "Doğum Oranı", self.dogum_orani_var, 0.0, 1.0,
                           lambda v: setattr(self.parametreler, 'dogum_orani', float(v)), scale=100)
        
        self.olum_orani_var = tk.DoubleVar(value=self.parametreler.olum_orani)
        self.slider_olustur(pop_subframe, "Ölüm Oranı", self.olum_orani_var, 0.0, 1.0,
                           lambda v: setattr(self.parametreler, 'olum_orani', float(v)), scale=100)
        
        # Kontrol Butonları
        buton_frame = tk.Frame(self.kontrol_cercevesi, bg='#e8e8e8')
        buton_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.baslat_btn = tk.Button(buton_frame, text="▶ Başlat", command=self.simulasyonu_baslat,
                                   bg='#4CAF50', fg='white', font=("Arial", 12, "bold"))
        self.baslat_btn.pack(side=tk.LEFT, padx=2)
        
        self.durdur_btn = tk.Button(buton_frame, text="⏸ Duraklat", command=self.simulasyonu_durdur,
                                   bg='#FF9800', fg='white', font=("Arial", 12, "bold"))
        self.durdur_btn.pack(side=tk.LEFT, padx=2)
        
        self.sifirla_btn = tk.Button(buton_frame, text="🔄 Sıfırla", command=self.simulasyonu_sifirla,
                                    bg='#f44336', fg='white', font=("Arial", 12, "bold"))
        self.sifirla_btn.pack(side=tk.LEFT, padx=2)
        
        # Hız kontrolü
        hiz_frame = tk.Frame(self.kontrol_cercevesi, bg='#e8e8e8')
        hiz_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(hiz_frame, text="Simülasyon Hızı:", bg='#e8e8e8', font=("Arial", 10)).pack()
        self.hiz_var = tk.DoubleVar(value=1.0)
        hiz_scale = tk.Scale(hiz_frame, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL,
                            variable=self.hiz_var, bg='#e8e8e8')
        hiz_scale.pack(fill=tk.X)
        
        # Veri kaydetme
        kaydet_btn = tk.Button(self.kontrol_cercevesi, text="💾 Veri Kaydet", command=self.veri_kaydet,
                              bg='#2196F3', fg='white', font=("Arial", 12, "bold"))
        kaydet_btn.pack(pady=10)
        
    def slider_olustur(self, parent, text, variable, min_val, max_val, callback, scale=1):
        """Slider oluşturma yardımcı fonksiyonu"""
        frame = tk.Frame(parent, bg='#e8e8e8')
        frame.pack(fill=tk.X, pady=2)
        
        # Label frame
        label_frame = tk.Frame(frame, bg='#e8e8e8')
        label_frame.pack(fill=tk.X)
        
        label = tk.Label(label_frame, text=text, bg='#e8e8e8', font=("Arial", 9))
        label.pack(side=tk.LEFT)
        
        # Değer ve buton frame
        control_frame = tk.Frame(frame, bg='#e8e8e8')
        control_frame.pack(fill=tk.X, pady=2)
        
        # Değer etiketi
        deger_label = tk.Label(control_frame, text=f"{variable.get():.3f}", bg='white', width=8, relief=tk.SUNKEN)
        deger_label.pack(side=tk.LEFT, padx=2)
        
        # Artırma/azaltma butonları
        btn_frame = tk.Frame(control_frame, bg='#e8e8e8')
        btn_frame.pack(side=tk.RIGHT)
        
        def artir():
            step = (max_val - min_val) / 100
            if isinstance(variable, tk.IntVar):
                step = max(1, int(step))
            yeni_deger = min(max_val, variable.get() + step)
            variable.set(yeni_deger)
            deger_label.config(text=f"{yeni_deger:.3f}")
            callback(yeni_deger)
            
        def azalt():
            step = (max_val - min_val) / 100
            if isinstance(variable, tk.IntVar):
                step = max(1, int(step))
            yeni_deger = max(min_val, variable.get() - step)
            variable.set(yeni_deger)
            deger_label.config(text=f"{yeni_deger:.3f}")
            callback(yeni_deger)
        
        artir_btn = tk.Button(btn_frame, text="▲", command=artir, width=3, height=1, 
                             bg='#4CAF50', fg='white', font=("Arial", 8, "bold"))
        artir_btn.pack(side=tk.TOP, pady=1)
        
        azalt_btn = tk.Button(btn_frame, text="▼", command=azalt, width=3, height=1,
                             bg='#f44336', fg='white', font=("Arial", 8, "bold"))
        azalt_btn.pack(side=tk.BOTTOM, pady=1)
        
        def guncelle(*args):
            deger_label.config(text=f"{variable.get():.3f}")
            callback(variable.get())
        
        variable.trace('w', guncelle)
    
    def balik_paneli_olustur(self):
        """Canlı balık simülasyon panelini oluştur"""
        # Başlık
        baslik_frame = tk.Frame(self.balik_cercevesi, bg='lightblue')
        baslik_frame.pack(fill=tk.X, pady=5)
        
        baslik = tk.Label(baslik_frame, text="🐠 Canlı Balık Akvaryumu 🐠", 
                         font=("Arial", 16, "bold"), bg='lightblue', fg='darkblue')
        baslik.pack()
        
        # Ana balık alanı
        self.balik_canvas = tk.Canvas(self.balik_cercevesi, bg='#87CEEB', height=150)
        self.balik_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Balık pozisyonları için liste
        self.balik_pozisyonlari = []
        
        # İstatistik paneli
        istatistik_frame = tk.Frame(self.balik_cercevesi, bg='lightblue')
        istatistik_frame.pack(fill=tk.X, pady=2)
        
        self.istatistik_label = tk.Label(istatistik_frame, 
                                        text="Nesil: 0 | Toplam: 0 | 🔴: 0 | ⚪: 0 | 🟠: 0",
                                        font=("Arial", 12, "bold"), bg='lightblue', fg='darkblue')
        self.istatistik_label.pack()
        
    def grafik_paneli_olustur(self):
        """Grafik panelini oluştur"""
        # Matplotlib figürü (daha küçük boyut)
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 6))
        self.fig.patch.set_facecolor('#f8f8f8')
        
        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.grafik_cercevesi)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Grafik başlıkları
        self.ax1.set_title('🐠 Zaman İçinde Popülasyon Boyutu', fontweight='bold', fontsize=12)
        self.ax2.set_title('🔴⚪ Allel Frekansları', fontweight='bold', fontsize=12)
        self.ax3.set_title('📊 Genotip Dağılımı', fontweight='bold', fontsize=12)
        self.ax4.set_title('🧬 Genetik Çeşitlilik', fontweight='bold', fontsize=12)
        
        # Eksen etiketleri
        self.ax1.set_xlabel('Nesil')
        self.ax1.set_ylabel('Popülasyon Boyutu')
        self.ax2.set_xlabel('Nesil')
        self.ax2.set_ylabel('Allel Frekansı')
        self.ax3.set_xlabel('Nesil')
        self.ax3.set_ylabel('Frekans')
        self.ax4.set_xlabel('Nesil')
        self.ax4.set_ylabel('Çeşitlilik İndeksi')
        
        plt.tight_layout()
        
    def baslangic_populasyonu_olustur(self):
        """Başlangıç popülasyonunu oluştur"""
        self.populasyon.clear()
        self.nesil = 0
        self.nesil_verileri.clear()
        self.populasyon_verileri.clear()
        self.allel_frekanslari.clear()
        self.fitness_verileri.clear()
        
        # Hardy-Weinberg dengesine göre genotip frekansları
        p = self.parametreler.kirmizi_balik_orani  # K allel frekansı
        q = 1 - p  # B allel frekansı
        
        kk_freq = p * p
        kb_freq = 2 * p * q
        bb_freq = q * q
        
        for i in range(self.parametreler.populasyon_sayisi):
            # Genotip belirleme
            rand = random.random()
            if rand < kk_freq:
                genotip = "KK"
            elif rand < kk_freq + kb_freq:
                genotip = "KB"
            else:
                genotip = "BB"
            
            birey = BalikBireyi(genotip, "disi" if random.random() < 0.5 else "erkek")
            self.populasyon.append(birey)
        
        self.verileri_kaydet()
        
    def simulasyonu_baslat(self):
        """Simülasyonu başlat"""
        if not self.calisir:
            self.calisir = True
            self.simulasyon_thread = threading.Thread(target=self.simulasyon_dongusu)
            self.simulasyon_thread.daemon = True
            self.simulasyon_thread.start()
            
    def simulasyonu_durdur(self):
        """Simülasyonu durdur"""
        self.calisir = False
        
    def simulasyonu_sifirla(self):
        """Simülasyonu sıfırla"""
        self.calisir = False
        time.sleep(0.1)  # Thread'in durması için bekle
        self.baslangic_populasyonu_olustur()
        self.grafikleri_guncelle()
        
    def simulasyon_dongusu(self):
        """Ana simülasyon döngüsü"""
        while self.calisir:
            self.nesil += 1
            
            # Popülasyon dinamikleri (doğum ve ölüm)
            self.populasyon_dinamikleri_uygula()
            
            # Genetik sürüklenme
            self.genetik_suruklenme_uygula()
            
            # Mutasyon
            self.mutasyon_uygula()
            
            # Üreme
            self.ureme_gerceklestir()
            
            # Veri kaydetme
            self.verileri_kaydet()
            
            # Grafik güncelleme
            self.root.after(0, self.grafikleri_guncelle)
            
            # Hız kontrolü
            time.sleep(1.0 / self.hiz_var.get())
            
            # Popülasyon sıfırsa dur
            if len(self.populasyon) == 0:
                self.calisir = False
                break
                
    def populasyon_dinamikleri_uygula(self):
        """Popülasyon artış ve azalış dinamikleri - Düzeltilmiş"""
        mevcut_populasyon = len(self.populasyon)
        
        if mevcut_populasyon == 0:
            return
        
        # Ölüm (rastgele bireyler ölür)
        olecek_sayi = int(mevcut_populasyon * self.parametreler.olum_orani)
        if olecek_sayi > 0 and olecek_sayi < mevcut_populasyon:
            # Güvenli şekilde rastgele bireyler seç ve çıkar
            olecek_indeksler = random.sample(range(mevcut_populasyon), olecek_sayi)
            olecek_indeksler.sort(reverse=True)  # Büyükten küçüğe sırala
            
            for indeks in olecek_indeksler:
                if indeks < len(self.populasyon):
                    self.populasyon.pop(indeks)
        
        # Doğum (yeni bireyler eklenir)
        if len(self.populasyon) >= 2:  # En az 2 birey olmalı
            dogacak_sayi = int(mevcut_populasyon * self.parametreler.dogum_orani)
            for _ in range(dogacak_sayi):
                # Mevcut popülasyondan rastgele iki ebeveyn seç
                ebeveyn1 = random.choice(self.populasyon)
                ebeveyn2 = random.choice(self.populasyon)
                
                yeni_genotip = self.genotip_olustur(ebeveyn1.genotip, ebeveyn2.genotip)
                yeni_cinsiyet = "disi" if random.random() < 0.5 else "erkek"
                
                yeni_birey = BalikBireyi(yeni_genotip, yeni_cinsiyet)
                self.populasyon.append(yeni_birey)
    
    def genetik_suruklenme_uygula(self):
        """Genetik sürüklenme - rastgele değişimler"""
        if self.parametreler.genetik_suruklenme <= 0:
            return
            
        # Popülasyonun bir kısmını rastgele değiştir
        degisecek_sayi = int(len(self.populasyon) * self.parametreler.genetik_suruklenme)
        
        for _ in range(degisecek_sayi):
            if self.populasyon:
                # Rastgele bir birey seç
                birey = random.choice(self.populasyon)
                
                # Rastgele yeni genotip ver
                rastgele_genotip = random.choice(["KK", "KB", "BB"])
                birey.genotip = rastgele_genotip
    
    def mutasyon_uygula(self):
        """Mutasyon işlemini uygula"""
        for birey in self.populasyon:
            if random.random() < self.parametreler.mutasyon_orani:
                # Mutasyon gerçekleşir
                yeni_genotip = ""
                
                for allel in birey.genotip:
                    if random.random() < 0.5:  # %50 şansla allel değişir
                        if allel == "K":
                            yeni_genotip += "B"
                        else:
                            yeni_genotip += "K"
                    else:
                        yeni_genotip += allel
                        
                birey.genotip = "".join(sorted(yeni_genotip, reverse=True))
        
    def ureme_gerceklestir(self):
        """Üreme işlemini gerçekleştir - Sadeleştirilmiş"""
        if len(self.populasyon) < 2:
            return
            
        # Popülasyonun %20'si kadar yeni yavru üret
        yavru_sayisi = max(1, int(len(self.populasyon) * 0.2))
        
        for _ in range(yavru_sayisi):
            # Rastgele iki ebeveyn seç
            ebeveyn1 = random.choice(self.populasyon)
            ebeveyn2 = random.choice(self.populasyon)
            
            # Yavru oluştur
            yavru_genotip = self.genotip_olustur(ebeveyn1.genotip, ebeveyn2.genotip)
            yavru_cinsiyet = "disi" if random.random() < 0.5 else "erkek"
            
            yavru = BalikBireyi(yavru_genotip, yavru_cinsiyet)
            self.populasyon.append(yavru)
        
    def genotip_olustur(self, anne_genotip: str, baba_genotip: str) -> str:
        """İki ebeveynden yavru genotipi oluştur"""
        # Anne'den allel
        if anne_genotip == "KK":
            anne_allel = "K"
        elif anne_genotip == "BB":
            anne_allel = "B"
        else:  # KB
            anne_allel = random.choice(["K", "B"])
            
        # Baba'dan allel
        if baba_genotip == "KK":
            baba_allel = "K"
        elif baba_genotip == "BB":
            baba_allel = "B"
        else:  # KB
            baba_allel = random.choice(["K", "B"])
        
        # Genotip oluştur
        alleller = sorted([anne_allel, baba_allel], reverse=True)
        return "".join(alleller)
        
    def verileri_kaydet(self):
        """Mevcut nesil verilerini kaydet - Düzeltilmiş"""
        if not self.populasyon:
            # Boş popülasyon durumu
            self.nesil_verileri.append(self.nesil)
            self.populasyon_verileri.append(0)
            self.allel_frekanslari.append({'K': 0, 'B': 0})
            self.fitness_verileri.append({
                'KK': 0, 'KB': 0, 'BB': 0, 'ortalama': 0,
                'genetik_cesitlilik': 0
            })
            return
            
        # Genotip sayıları hesapla
        kk_sayisi = 0
        kb_sayisi = 0  
        bb_sayisi = 0
        
        for birey in self.populasyon:
            if birey.genotip == "KK":
                kk_sayisi += 1
            elif birey.genotip == "KB" or birey.genotip == "BK":
                kb_sayisi += 1
            elif birey.genotip == "BB":
                bb_sayisi += 1
        
        toplam = len(self.populasyon)
        
        # Allel frekansları hesapla (doğru formül)
        if toplam > 0:
            # K alleli sayısı = (KK bireylerinde 2 adet) + (KB bireylerinde 1 adet)
            k_allel_sayisi = (kk_sayisi * 2) + (kb_sayisi * 1)
            toplam_allel_sayisi = toplam * 2  # Her bireyde 2 allel var
            
            k_frekansi = k_allel_sayisi / toplam_allel_sayisi
            b_frekansi = 1.0 - k_frekansi
            
            # Genotip frekansları
            kk_frekansi = kk_sayisi / toplam
            kb_frekansi = kb_sayisi / toplam
            bb_frekansi = bb_sayisi / toplam
            
            # Genetik çeşitlilik hesapla (Shannon Diversity Index)
            genetik_cesitlilik = 0
            if kk_frekansi > 0:
                genetik_cesitlilik -= kk_frekansi * np.log(kk_frekansi)
            if kb_frekansi > 0:
                genetik_cesitlilik -= kb_frekansi * np.log(kb_frekansi)
            if bb_frekansi > 0:
                genetik_cesitlilik -= bb_frekansi * np.log(bb_frekansi)
        else:
            k_frekansi = b_frekansi = 0
            kk_frekansi = kb_frekansi = bb_frekansi = 0
            genetik_cesitlilik = 0
        
        # Verileri kaydet
        self.nesil_verileri.append(self.nesil)
        self.populasyon_verileri.append(toplam)
        self.allel_frekanslari.append({
            'K': k_frekansi, 
            'B': b_frekansi
        })
        self.fitness_verileri.append({
            'KK': kk_frekansi,
            'KB': kb_frekansi, 
            'BB': bb_frekansi,
            'ortalama': 1.0,  # Tüm genotiplerin fitness'ı eşit
            'genetik_cesitlilik': genetik_cesitlilik
        })
        
        # Debug bilgisi (konsola yazdır)
        if self.nesil % 10 == 0:  # Her 10 nesilte bir yazdır
            print(f"Nesil {self.nesil}: Pop={toplam}, KK={kk_sayisi}, KB={kb_sayisi}, BB={bb_sayisi}")
            print(f"  K frekansı: {k_frekansi:.3f}, B frekansı: {b_frekansi:.3f}")
            print(f"  Genetik çeşitlilik: {genetik_cesitlilik:.3f}")
            print("---")
        
    def grafikleri_guncelle(self):
        """Grafikleri güncelle"""
        if not self.nesil_verileri:
            return
            
        # Grafikleri temizle
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.clear()
            
        # 1. Popülasyon boyutu
        self.ax1.plot(self.nesil_verileri, self.populasyon_verileri, 'b-', linewidth=2)
        self.ax1.set_title('🐠 Zaman İçinde Popülasyon Boyutu', fontweight='bold')
        self.ax1.set_xlabel('Nesil')
        self.ax1.set_ylabel('Popülasyon Boyutu')
        self.ax1.grid(True, alpha=0.3)
        
        # 2. Allel frekansları
        k_frekanslari = [af['K'] for af in self.allel_frekanslari]
        b_frekanslari = [af['B'] for af in self.allel_frekanslari]
        
        self.ax2.plot(self.nesil_verileri, k_frekanslari, 'r-', linewidth=2, label='K (Kırmızı)')
        self.ax2.plot(self.nesil_verileri, b_frekanslari, 'lightgray', linewidth=2, label='B (Beyaz)')
        self.ax2.set_title('🔴⚪ Allel Frekansları', fontweight='bold')
        self.ax2.set_xlabel('Nesil')
        self.ax2.set_ylabel('Allel Frekansı')
        self.ax2.legend()
        self.ax2.grid(True, alpha=0.3)
        self.ax2.set_ylim(0, 1)
        
        # 3. Genotip dağılımı
        kk_frekanslari = [gf['KK'] for gf in self.fitness_verileri]
        kb_frekanslari = [gf['KB'] for gf in self.fitness_verileri]
        bb_frekanslari = [gf['BB'] for gf in self.fitness_verileri]
        
        self.ax3.plot(self.nesil_verileri, kk_frekanslari, 'darkred', linewidth=2, label='KK')
        self.ax3.plot(self.nesil_verileri, kb_frekanslari, 'orange', linewidth=2, label='KB')
        self.ax3.plot(self.nesil_verileri, bb_frekanslari, 'lightgray', linewidth=2, label='BB')
        self.ax3.set_title('📊 Genotip Dağılımı', fontweight='bold')
        self.ax3.set_xlabel('Nesil')
        self.ax3.set_ylabel('Frekans')
        self.ax3.legend()
        self.ax3.grid(True, alpha=0.3)
        self.ax3.set_ylim(0, 1)
        
        # 4. Genetik çeşitlilik
        genetik_cesitlilik_verileri = [gf['genetik_cesitlilik'] for gf in self.fitness_verileri]
        self.ax4.plot(self.nesil_verileri, genetik_cesitlilik_verileri, 'green', linewidth=2)
        self.ax4.set_title('🧬 Genetik Çeşitlilik', fontweight='bold')
        self.ax4.set_xlabel('Nesil')
        self.ax4.set_ylabel('Çeşitlilik İndeksi')
        self.ax4.grid(True, alpha=0.3)
        
        # Çeşitlilik açıklaması ekle
        max_cesitlilik = np.log(3)  # 3 genotip için maksimum çeşitlilik
        self.ax4.axhline(y=max_cesitlilik, color='red', linestyle='--', alpha=0.5, label='Maksimum Çeşitlilik')
        self.ax4.legend()
        
        plt.tight_layout()
        self.canvas.draw()
        
        # Canlı balık panelini güncelle
        self.balik_panelini_guncelle()
        
    def balik_panelini_guncelle(self):
        """Canlı balık panelini güncelle"""
        if not hasattr(self, 'balik_canvas'):
            return
            
        # Canvas'ı temizle
        self.balik_canvas.delete("all")
        
        if not self.populasyon:
            return
            
        # Canvas boyutları
        canvas_width = self.balik_canvas.winfo_width()
        canvas_height = self.balik_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 800
            canvas_height = 150
        
        # Balık sayıları
        kk_sayisi = len([b for b in self.populasyon if b.genotip == "KK"])
        kb_sayisi = len([b for b in self.populasyon if b.genotip == "KB"])
        bb_sayisi = len([b for b in self.populasyon if b.genotip == "BB"])
        toplam = len(self.populasyon)
        
        # İstatistik güncelle
        istatistik_text = f"Nesil: {self.nesil} | Toplam: {toplam} | 🔴: {kk_sayisi} | 🟠: {kb_sayisi} | ⚪: {bb_sayisi}"
        self.istatistik_label.config(text=istatistik_text)
        
        # Balıkları çiz (maksimum 50 balık göster)
        gosterilecek_baliklar = min(50, toplam)
        if gosterilecek_baliklar == 0:
            return
            
        # Balık pozisyonlarını güncelle
        if len(self.balik_pozisyonlari) != gosterilecek_baliklar:
            self.balik_pozisyonlari = []
            for i in range(gosterilecek_baliklar):
                x = random.uniform(20, canvas_width - 20)
                y = random.uniform(20, canvas_height - 20)
                vx = random.uniform(-2, 2)
                vy = random.uniform(-1, 1)
                self.balik_pozisyonlari.append([x, y, vx, vy])
        
        # Balık pozisyonlarını güncelle (hareket)
        for pos in self.balik_pozisyonlari:
            pos[0] += pos[2]  # x += vx
            pos[1] += pos[3]  # y += vy
            
            # Sınır kontrolü
            if pos[0] <= 15 or pos[0] >= canvas_width - 15:
                pos[2] = -pos[2]  # vx tersine çevir
            if pos[1] <= 15 or pos[1] >= canvas_height - 15:
                pos[3] = -pos[3]  # vy tersine çevir
                
            pos[0] = max(15, min(canvas_width - 15, pos[0]))
            pos[1] = max(15, min(canvas_height - 15, pos[1]))
        
        # Balıkları çiz
        for i in range(gosterilecek_baliklar):
            if i < len(self.populasyon):
                balik = self.populasyon[i]
                pos = self.balik_pozisyonlari[i]
                
                # Renk belirleme
                if balik.genotip == "KK":
                    renk = "#FF3333"  # Kırmızı
                    outline = "#CC0000"
                elif balik.genotip == "KB":
                    renk = "#FF9933"  # Turuncu (karışık)
                    outline = "#CC6600"
                else:  # BB
                    renk = "#FFFFFF"  # Beyaz
                    outline = "#CCCCCC"
                
                # Balık şekli çiz
                x, y = pos[0], pos[1]
                
                # Gövde (oval)
                self.balik_canvas.create_oval(x-8, y-4, x+8, y+4, 
                                            fill=renk, outline=outline, width=2)
                
                # Kuyruk (üçgen)
                self.balik_canvas.create_polygon(x-8, y, x-15, y-3, x-15, y+3,
                                               fill=renk, outline=outline, width=1)
                
                # Göz
                self.balik_canvas.create_oval(x+2, y-1, x+4, y+1, 
                                            fill="black", outline="black")
                
                # Cinsiyet göstergesi
                if balik.cinsiyet == "disi":
                    self.balik_canvas.create_text(x, y-12, text="♀", 
                                                fill="pink", font=("Arial", 8, "bold"))
                else:
                    self.balik_canvas.create_text(x, y-12, text="♂", 
                                                fill="blue", font=("Arial", 8, "bold"))
        
        # Su kabarcıkları efekti
        for _ in range(5):
            bx = random.uniform(10, canvas_width - 10)
            by = random.uniform(10, canvas_height - 10)
            br = random.uniform(2, 5)
            self.balik_canvas.create_oval(bx-br, by-br, bx+br, by+br,
                                        fill="lightcyan", outline="cyan", width=1)
        
    def veri_kaydet(self):
        """Simülasyon verilerini JSON dosyasına kaydet"""
        zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
        dosya_adi = f"evrim_simulasyon_verileri_{zaman_damgasi}.json"
        
        veri = {
            'parametreler': {
                'populasyon_sayisi': self.parametreler.populasyon_sayisi,
                'kirmizi_balik_orani': self.parametreler.kirmizi_balik_orani,
                'genetik_suruklenme': self.parametreler.genetik_suruklenme,
                'mutasyon_orani': self.parametreler.mutasyon_orani,
                'dogum_orani': self.parametreler.dogum_orani,
                'olum_orani': self.parametreler.olum_orani
            },
            'nesil_verileri': self.nesil_verileri,
            'populasyon_verileri': self.populasyon_verileri,
            'allel_frekanslari': self.allel_frekanslari,
            'fitness_verileri': self.fitness_verileri,
            'son_nesil': self.nesil
        }
        
        try:
            with open(dosya_adi, 'w', encoding='utf-8') as f:
                json.dump(veri, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Başarılı", f"Veriler {dosya_adi} dosyasına kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Veri kaydetme hatası: {e}")
            
    def calistir(self):
        """Uygulamayı çalıştır"""
        self.root.mainloop()

def main():
    """Ana fonksiyon"""
    print("🐠 Profesyonel Balık Evrim Simülasyonu başlatılıyor...")
    simulasyon = EvrimSimulasyonu()
    simulasyon.calistir()

if __name__ == "__main__":
    main()