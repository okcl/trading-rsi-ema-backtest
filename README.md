# RSI-EMA Trading Backtest Dashboard

Bu proje, Binance API'den alınan **BTCUSDT** verileri üzerinde RSI (Relative Strength Index) ve EMA (Exponential Moving Average) göstergelerine dayalı basit bir alım-satım stratejisinin geçmiş performansını test etmek için hazırlanmış bir Streamlit tabanlı dashboard uygulamasıdır.

---

## Özellikler

- Binance'den seçilen zaman aralığı (5m, 15m, 30m, 1h) ve gün sayısına göre veri çekme  
- RSI ve EMA göstergeleri kullanarak esnek sinyal üretimi (alış/satış noktaları)  
- Geçmiş performansın backtest ile hesaplanması  
- Toplam kar, işlem sayısı, başlangıç ve bitiş bakiyesi gibi temel metriklerin gösterimi  
- İşlem fiyatları ve al-sat noktalarının grafiklerle görselleştirilmesi  

---

## Kullanım

1. Projeyi klonlayın veya indirin.  
2. Gerekli paketleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
3. Streamlit uygulamasını başlatın:
    ```bash
    streamlit run app.py
    ```
4. Dashboard üzerinden zaman aralığı ve veri gün sayısını seçip "Veriyi İndir ve Backtest Yap" butonuna tıklayın.  
5. İşlem sonuçlarını ve grafiklerini inceleyin.

---

## Strateji Detayları

- RSI, fiyatın aşırı alım veya aşırı satım bölgesinde olup olmadığını gösterir.  
- EMA hızlı ve yavaş hareketli ortalamalar trend yönünü belirler.  
- Sinyal kuralları:  
  - **Alış (BUY):** RSI 55'in üzerinde, EMA hızlı EMA yavaş üzerinde ve önceki bar EMA hızlı EMA yavaş altında ise pozisyon açılır.  
  - **Satış (SELL):** RSI 45'in altında veya EMA hızlı EMA yavaş altına düştüğünde pozisyon kapatılır.  
- Bu sayede trend ve momentum bazlı esnek işlemler gerçekleştirilir.

---

## Dosya Yapısı

- `app.py` : Streamlit dashboard ana dosyası  
- `utils/fetch_binance_data.py` : Binance'den veri çekme fonksiyonları  
- `backtest/run_backtest.py` : Backtest işlemleri ve strateji yürütme  
- `data/` : İndirilen veri dosyalarının saklandığı klasör (isteğe bağlı)  
- `logs/` : İşlem kayıtları ve log dosyaları (isteğe bağlı)  

---

## Gereksinimler

Python 3.7+ ve aşağıdaki paketler:

- pandas  
- numpy  
- ta  
- requests  
- streamlit  
- plotly  

---

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.

---

Herhangi bir sorun ya da öneriniz için lütfen iletişime geçin.
