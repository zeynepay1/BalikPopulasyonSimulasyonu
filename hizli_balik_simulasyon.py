import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import random
import threading
import time
from datetime import datetime
import json

class HizliBalikSimulasyonu:
    """Hızlı ve optimize edilmiş balık popülasyon simülasyonu"""
    
    def __init__(self, baslangic_populasyonu=1000, simulasyon_yili=200):
        self.baslangic_populasyonu = baslangic_populasyonu
        self.simulasyon_yili = simulasyon_yili
        
        # Genetik yapı - basit tutalım
        self.reset_populasyon()
        
        # Veri saklama
        self.yillar = []
        self.k_allel_frekanslari = []
        self.b_allel_frekanslari = []
        self.toplam_populasyonlar = []
        self.kk_frekanslari = []
        self.kb_frekanslari = []
        self.bb_frekanslari = []
        self.olaylar = []
        
    def reset_populasyon(self):
        """Popülasyonu Hardy-Weinberg dengesinde başlat"""
        p = 0.6  # K allel frekansı
        q = 0.4  # B allel frekansı
        
        # Basit hesaplama
        self.kk_sayisi = int(self.baslangic_populasyonu * p * p)
        self.kb_sayisi = int(self.baslangic_populasyonu * 2 * p * q)
        self.bb_sayisi = self.baslangic_populasyonu - self.kk_sayisi - self.kb_sayisi
        
    def tek_yil_simule_et(self, yil):
        """Bir yılı hızlıca simüle et"""
        toplam = self.kk_sayisi + self.kb_sayisi + self.bb_sayisi
        
        if toplam < 10:  # Kritik seviye
            return False
            
        # Basit mevsimsel etki
        mevsim_etkisi = 1.0 + 0.2 * np.sin(2 * np.pi * yil / 10)  # 10 yıllık döngü
        
        # Rastgele olaylar (düşük olasılık)
        olay = ""
        if random.random() < 0.05:  # %5 şans
            if random.random() < 0.5:
                # Hastalık
                kayip = random.uniform(0.1, 0.3)
                self.kk_sayisi = int(self.kk_sayisi * (1 - kayip))
                self.kb_sayisi = int(self.kb_sayisi * (1 - kayip))
                self.bb_sayisi = int(self.bb_sayisi * (1 - kayip))
                olay = f"Hastalık (%{kayip*100:.0f} kayıp)"
            else:
                # Yırtıcı saldırısı - renkli balıklar daha çok etkilenir
                kk_kayip = random.uniform(0.15, 0.25)
                kb_kayip = random.uniform(0.10, 0.20)
                bb_kayip = random.uniform(0.05, 0.15)
                
                self.kk_sayisi = int(self.kk_sayisi * (1 - kk_kayip))
                self.kb_sayisi = int(self.kb_sayisi * (1 - kb_kayip))
                self.bb_sayisi = int(self.bb_sayisi * (1 - bb_kayip))
                olay = "Yırtıcı Saldırısı"
        
        # Basit fitness ve üreme
        toplam = self.kk_sayisi + self.kb_sayisi + self.bb_sayisi
        
        if toplam > 0:
            # Allel frekanslarını hesapla
            k_freq = (2 * self.kk_sayisi + self.kb_sayisi) / (2 * toplam)
            b_freq = 1 - k_freq
            
            # Yeni nesil üret (Hardy-Weinberg + hafif seçilim)
            yeni_toplam = int(toplam * mevsim_etkisi)
            yeni_toplam = max(50, min(yeni_toplam, self.baslangic_populasyonu * 2))
            
            # Hafif heterozygot avantajı
            k_freq_yeni = k_freq + random.uniform(-0.01, 0.01)  # Küçük değişim
            k_freq_yeni = max(0.05, min(0.95, k_freq_yeni))
            b_freq_yeni = 1 - k_freq_yeni
            
            # Yeni genotip sayıları
            self.kk_sayisi = int(yeni_toplam * k_freq_yeni * k_freq_yeni)
            self.kb_sayisi = int(yeni_toplam * 2 * k_freq_yeni * b_freq_yeni)
            self.bb_sayisi = yeni_toplam - self.kk_sayisi - self.kb_sayisi
            
        # Veri kaydet
        toplam = self.kk_sayisi + self.kb_sayisi + self.bb_sayisi
        if toplam > 0:
            k_freq = (2 * self.kk_sayisi + self.kb_sayisi) / (2 * toplam)
            b_freq = 1 - k_freq
            kk_freq = self.kk_sayisi / toplam
            kb_freq = self.kb_sayisi / toplam
            bb_freq = self.bb_sayisi / toplam
        else:
            k_freq = b_freq = kk_freq = kb_freq = bb_freq = 0
            
        self.yillar.append(yil)
        self.k_allel_frekanslari.append(k_freq)
        self.b_allel_frekanslari.append(b_freq)
        self.toplam_populasyonlar.append(toplam)
        self.kk_frekanslari.append(kk_freq)
        self.kb_frekanslari.append(kb_freq)
        self.bb_frekanslari.append(bb_freq)
        self.olaylar.append(olay)
        
        return True
    
    def tam_simulasyon_calistir(self):
        """Tüm simülasyonu hızlıca çalıştır"""
        self.reset_populasyon()
        
        # İlk veri noktası
        toplam = self.kk_sayisi + self.kb_sayisi + self.bb_sayisi
        k_freq = (2 * self.kk_sayisi + self.kb_sayisi) / (2 * toplam)
        
        self.yillar = [0]
        self.k_allel_frekanslari = [k_freq]
        self.b_allel_frekanslari = [1 - k_freq]
        self.toplam_populasyonlar = [toplam]
        self.kk_frekanslari = [self.kk_sayisi / toplam]
        self.kb_frekanslari = [self.kb_sayisi / toplam]
        self.bb_frekanslari = [self.bb_sayisi / toplam]
        self.olaylar = [""]
        
        # Simülasyonu çalıştır
        for yil in range(1, self.simulasyon_yili + 1):
            if not self.tek_yil_simule_et(yil):
                print(f"Popülasyon {yil}. yılda yok oldu!")
                break
                
        return len(self.yillar)

class HizliArayuz:
    """Basit ve hızlı arayüz"""
    
    def __init__(self):
        self.simulasyon = None
        self.arayuz_olustur()
        
    def arayuz_olustur(self):
        """Basit arayüz oluştur"""
        self.root = tk.Tk()
        self.root.title("🐠 Hızlı Balık Popülasyon Genetiği")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f8ff')
        
        # Başlık
        baslik = tk.Label(self.root, 
                         text="🐠 Hızlı Balık Popülasyon Genetiği Simülasyonu 🐠",
                         font=("Arial", 16, "bold"), bg='#f0f8ff', fg='#2c3e50')
        baslik.pack(pady=10)
        
        # Kontrol paneli
        kontrol_frame = tk.Frame(self.root, bg='#ecf0f1')
        kontrol_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Parametreler
        tk.Label(kontrol_frame, text="Başlangıç Popülasyonu:", bg='#ecf0f1', font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.pop_var = tk.IntVar(value=1000)
        tk.Spinbox(kontrol_frame, from_=500, to=3000, textvariable=self.pop_var, width=8).pack(side=tk.LEFT, padx=5)
        
        tk.Label(kontrol_frame, text="Simülasyon Yılı:", bg='#ecf0f1', font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.yil_var = tk.IntVar(value=200)
        tk.Spinbox(kontrol_frame, from_=50, to=500, textvariable=self.yil_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # Butonlar
        tk.Button(kontrol_frame, text="🚀 Hızlı Simülasyon", command=self.hizli_simulasyon,
                 bg='#27ae60', fg='white', font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
        
        tk.Button(kontrol_frame, text="💾 Kaydet", command=self.veri_kaydet,
                 bg='#3498db', fg='white', font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Progress
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=10, pady=5)
        
        # Status
        self.status_label = tk.Label(self.root, text="Simülasyon bekleniyor...", 
                                   bg='#f0f8ff', font=("Arial", 10))
        self.status_label.pack()
        
        # Grafik alanı
        self.grafik_frame = tk.Frame(self.root, bg='white')
        self.grafik_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.grafikleri_olustur()
        
    def grafikleri_olustur(self):
        """2x2 grafik düzeni"""
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(14, 8))
        self.fig.patch.set_facecolor('#f8f9fa')
        
        self.canvas = FigureCanvasTkAgg(self.fig, self.grafik_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Başlangıç mesajları
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.text(0.5, 0.5, 'Simülasyon bekleniyor...', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)
            
        plt.tight_layout()
        self.canvas.draw()
        
    def hizli_simulasyon(self):
        """Hızlı simülasyon çalıştır"""
        def calistir():
            self.progress.start()
            self.status_label.config(text="Simülasyon çalışıyor...")
            
            # Simülasyon oluştur ve çalıştır
            self.simulasyon = HizliBalikSimulasyonu(
                self.pop_var.get(), 
                self.yil_var.get()
            )
            
            tamamlanan_yil = self.simulasyon.tam_simulasyon_calistir()
            
            # Ana thread'de grafikleri güncelle
            self.root.after(100, lambda: self.grafikleri_guncelle(tamamlanan_yil))
            
        # Threading ile çalıştır
        thread = threading.Thread(target=calistir)
        thread.daemon = True
        thread.start()
        
    def grafikleri_guncelle(self, tamamlanan_yil):
        """Grafikleri güncelle"""
        self.progress.stop()
        self.status_label.config(text=f"Simülasyon tamamlandı: {tamamlanan_yil} yıl")
        
        if not self.simulasyon or not self.simulasyon.yillar:
            return
            
        # Grafikleri temizle
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.clear()
            
        yillar = self.simulasyon.yillar
        
        # 1. Allel Frekansları (ANA GRAFİK)
        self.ax1.plot(yillar, self.simulasyon.k_allel_frekanslari, 
                     'r-', linewidth=3, label='K (Kırmızı) Alleli', alpha=0.8)
        self.ax1.plot(yillar, self.simulasyon.b_allel_frekanslari, 
                     'gray', linewidth=3, label='B (Beyaz) Alleli', alpha=0.8)
        self.ax1.set_title('🧬 Allel Frekans Değişimi', fontsize=14, fontweight='bold')
        self.ax1.set_xlabel('Yıl')
        self.ax1.set_ylabel('Allel Frekansı')
        self.ax1.legend()
        self.ax1.grid(True, alpha=0.3)
        self.ax1.set_ylim(0, 1)
        
        # 2. Genotip Dağılımı
        self.ax2.fill_between(yillar, 0, self.simulasyon.kk_frekanslari, 
                             color='darkred', alpha=0.7, label='KK (Kırmızı)')
        kk_kb = np.array(self.simulasyon.kk_frekanslari) + np.array(self.simulasyon.kb_frekanslari)
        self.ax2.fill_between(yillar, self.simulasyon.kk_frekanslari, kk_kb,
                             color='orange', alpha=0.7, label='KB (Karma)')
        self.ax2.fill_between(yillar, kk_kb, 1, 
                             color='lightgray', alpha=0.7, label='BB (Beyaz)')
        self.ax2.set_title('📊 Genotip Dağılımı', fontsize=14, fontweight='bold')
        self.ax2.set_xlabel('Yıl')
        self.ax2.set_ylabel('Genotip Frekansı')
        self.ax2.legend()
        self.ax2.grid(True, alpha=0.3)
        
        # 3. Popülasyon Boyutu
        self.ax3.plot(yillar, self.simulasyon.toplam_populasyonlar, 
                     'b-', linewidth=2, alpha=0.8)
        self.ax3.fill_between(yillar, 0, self.simulasyon.toplam_populasyonlar, 
                             alpha=0.3, color='lightblue')
        self.ax3.set_title('🐠 Toplam Popülasyon', fontsize=14, fontweight='bold')
        self.ax3.set_xlabel('Yıl')
        self.ax3.set_ylabel('Birey Sayısı')
        self.ax3.grid(True, alpha=0.3)
        
        # 4. Önemli Olaylar
        olay_yillari = []
        olay_tipleri = []
        for i, olay in enumerate(self.simulasyon.olaylar):
            if olay:
                olay_yillari.append(yillar[i])
                if "Hastalık" in olay:
                    olay_tipleri.append(1)
                elif "Yırtıcı" in olay:
                    olay_tipleri.append(2)
                else:
                    olay_tipleri.append(3)
        
        if olay_yillari:
            colors = ['red' if t == 1 else 'orange' if t == 2 else 'purple' for t in olay_tipleri]
            self.ax4.scatter(olay_yillari, olay_tipleri, c=colors, s=100, alpha=0.7)
            
        self.ax4.set_title('⚡ Catastrofik Olaylar', fontsize=14, fontweight='bold')
        self.ax4.set_xlabel('Yıl')
        self.ax4.set_ylabel('Olay Tipi')
        self.ax4.set_yticks([1, 2, 3])
        self.ax4.set_yticklabels(['Hastalık', 'Yırtıcı', 'Diğer'])
        self.ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        self.canvas.draw()
        
        # Özet göster
        self.ozet_goster()
        
    def ozet_goster(self):
        """Basit özet göster"""
        if not self.simulasyon:
            return
            
        baslangic_k = self.simulasyon.k_allel_frekanslari[0]
        son_k = self.simulasyon.k_allel_frekanslari[-1]
        baslangic_pop = self.simulasyon.toplam_populasyonlar[0]
        son_pop = self.simulasyon.toplam_populasyonlar[-1]
        olay_sayisi = len([o for o in self.simulasyon.olaylar if o])
        
        ozet = f"""
🔬 SİMÜLASYON ÖZETİ

📊 ALLEL DEĞİŞİMİ:
   K (Kırmızı): {baslangic_k:.3f} → {son_k:.3f}
   Değişim: {'↗️' if son_k > baslangic_k else '↘️'} {abs(son_k-baslangic_k):.3f}

🐠 POPÜLASYON:
   Başlangıç: {baslangic_pop:,} birey
   Son durum: {son_pop:,} birey
   Değişim: %{((son_pop-baslangic_pop)/baslangic_pop)*100:+.1f}

⚡ OLAYLAR:
   Toplam catastrofik olay: {olay_sayisi}
   
✅ Simülasyon başarıyla tamamlandı!
        """
        
        messagebox.showinfo("Simülasyon Tamamlandı", ozet)
        
    def veri_kaydet(self):
        """Veriyi kaydet"""
        if not self.simulasyon:
            messagebox.showwarning("Uyarı", "Önce simülasyon çalıştırın!")
            return
            
        dosya_adi = f"hizli_balik_sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        veri = {
            'parametreler': {
                'baslangic_populasyonu': self.pop_var.get(),
                'simulasyon_yili': self.yil_var.get()
            },
            'sonuclar': {
                'yillar': self.simulasyon.yillar,
                'k_allel_frekanslari': self.simulasyon.k_allel_frekanslari,
                'b_allel_frekanslari': self.simulasyon.b_allel_frekanslari,
                'toplam_populasyonlar': self.simulasyon.toplam_populasyonlar,
                'olaylar': self.simulasyon.olaylar
            }
        }
        
        try:
            with open(dosya_adi, 'w', encoding='utf-8') as f:
                json.dump(veri, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Başarılı", f"Veri {dosya_adi} dosyasına kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydetme hatası: {e}")
            
    def calistir(self):
        """Uygulamayı başlat"""
        self.root.mainloop()

def main():
    """Ana fonksiyon"""
    print("🐠 Hızlı Balık Popülasyon Genetiği Simülasyonu başlatılıyor...")
    uygulama = HizliArayuz()
    uygulama.calistir()

if __name__ == "__main__":
    main() 