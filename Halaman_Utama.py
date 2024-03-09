import streamlit as st


# Membuat dropdown menu dengan beberapa pilihan
option = st.selectbox(
    'Pilih sebuah opsi',
    ('Metode North West Corner', 'Vogel Approximation Method (VAM)')
)

# Menampilkan hasil berdasarkan pilihan yang dipilih
st.write('Anda memilih:', option)

if option=='Metode North West Corner':
    st.markdown('# Metode North West Corner')
    st.markdown("""  
            **Metode North West Corner** (NWC) adalah salah satu metode yang digunakan dalam pemecahan masalah transportasi pada ilmu manajemen operasi. Metode ini digunakan untuk menemukan solusi awal dari masalah transportasi dengan memperhatikan sudut barat laut (northwest corner) dari tabel kebutuhan dan kapasitas.

Berikut adalah langkah-langkah lengkap dalam penerapan Metode North West Corner:

1. **Pemahaman Masalah:**
   - Masalah transportasi melibatkan alokasi sumber daya dari beberapa asal ke beberapa tujuan dengan biaya atau keuntungan yang telah ditentukan.
   - Dalam konteks NWC, kita akan mempertimbangkan masalah transportasi dengan asumsi bahwa setiap asal memiliki ketersediaan tertentu dan setiap tujuan memiliki permintaan tertentu.

2. **Membuat Tabel Transportasi:**
   - Membuat tabel yang menunjukkan asal (supply) dan tujuan (demand) beserta biaya (cost) atau keuntungan pada setiap sel.
   - Tabel ini akan memiliki baris untuk setiap asal dan kolom untuk setiap tujuan.

3. **Menentukan Titik Awal (Northwest Corner):**
   - Pilih sel di sudut barat laut (northwest corner) dari tabel. Sel ini akan menjadi titik awal untuk alokasi.
   - Biasanya, kita mulai dengan sel yang memiliki biaya atau keuntungan terendah di sudut barat laut.

4. **Alokasi Kapasitas (Supply dan Demand):**
   - Mulai dari titik awal yang telah ditentukan, alokasikan kapasitas maksimum yang tersedia (supply) ke tujuan yang membutuhkan (demand) hingga kapasitas atau permintaan terpenuhi.
   - Jika kapasitas atau permintaan untuk suatu asal atau tujuan telah terpenuhi, geser ke sel berikutnya ke arah timur (kanan) atau selatan (bawah) sesuai dengan kebijakan prioritas pengalokasian.

5. **Memperbarui Ketersediaan (Supply) dan Permintaan (Demand):**
   - Setelah alokasi dilakukan, perbarui ketersediaan (supply) dan permintaan (demand) yang tersisa.
   - Jika kapasitas suatu asal atau tujuan telah terpenuhi, hilangkan baris atau kolom tersebut dari tabel.

6. **Menyimpulkan Alokasi:**
   - Ulangi langkah-langkah 3 hingga 5 hingga semua ketersediaan (supply) dan permintaan (demand) telah terpenuhi.
   - Akhirnya, hasil akhir akan berupa alokasi sumber daya yang optimal dari setiap asal ke setiap tujuan dengan biaya atau keuntungan minimum atau maksimum, sesuai dengan kasus yang diberikan.

7. **Menganalisis dan Evaluasi Solusi:**
   - Setelah mendapatkan alokasi awal menggunakan Metode North West Corner, solusi tersebut dapat dievaluasi lebih lanjut untuk memastikan konsistensi dengan tujuan bisnis dan memperhitungkan faktor-faktor lain seperti batasan waktu, kapasitas, atau aturan bisnis lainnya.

Metode North West Corner sering digunakan sebagai langkah awal dalam pemecahan masalah transportasi, dan seringkali diikuti oleh metode penyelesaian lain seperti Metode Minimum Cost atau Metode Vogel untuk memperbaiki solusi awal yang diperoleh.

            
            
            
            """)
else:
    st.markdown('# Vogel Approximation Method (VAM)')
    st.markdown('''
Metode Vogel's Approximation Method (VAM) adalah salah satu metode yang digunakan dalam pemecahan masalah transportasi pada ilmu manajemen operasi. Metode ini dirancang untuk memberikan solusi awal yang lebih baik daripada Metode North West Corner dengan mempertimbangkan perbedaan biaya atau keuntungan antara sel-sel dalam tabel transportasi.

Berikut adalah langkah-langkah lengkap dalam penerapan Metode Vogel's Approximation Method (VAM):

1. **Pemahaman Masalah:**
   - Seperti yang telah dijelaskan sebelumnya, masalah transportasi melibatkan alokasi sumber daya dari beberapa asal ke beberapa tujuan dengan biaya atau keuntungan yang telah ditentukan.

2. **Membuat Tabel Transportasi:**
   - Membuat tabel yang menunjukkan asal (supply) dan tujuan (demand) beserta biaya (cost) atau keuntungan pada setiap sel.

3. **Menghitung Biaya Diferensial (Penalti):**
   - Menghitung biaya diferensial (penalti) untuk setiap baris dan kolom dalam tabel. Biaya diferensial adalah perbedaan biaya terbesar dan biaya terkecil di setiap baris atau kolom.
   - Hitung selisih antara biaya terbesar dan biaya terkecil untuk setiap baris dan kolom.

4. **Menentukan Sel dengan Biaya Diferensial Terbesar:**
   - Tentukan baris dan kolom dengan biaya diferensial terbesar.
   - Pilih sel yang memiliki biaya diferensial terbesar. Jika terdapat lebih dari satu sel dengan biaya diferensial terbesar, pilih salah satunya secara arbitrer.

5. **Alokasi Kapasitas (Supply dan Demand):**
   - Alokasikan kapasitas maksimum yang tersedia (supply) ke tujuan yang membutuhkan (demand) hingga kapasitas atau permintaan terpenuhi.
   - Jika kapasitas atau permintaan untuk suatu asal atau tujuan telah terpenuhi, geser ke sel berikutnya ke arah timur (kanan) atau selatan (bawah) sesuai dengan kebijakan prioritas pengalokasian.

6. **Memperbarui Ketersediaan (Supply) dan Permintaan (Demand):**
   - Setelah alokasi dilakukan, perbarui ketersediaan (supply) dan permintaan (demand) yang tersisa.
   - Jika kapasitas suatu asal atau tujuan telah terpenuhi, hilangkan baris atau kolom tersebut dari tabel.

7. **Menyimpulkan Alokasi:**
   - Ulangi langkah-langkah 3 hingga 6 hingga semua ketersediaan (supply) dan permintaan (demand) telah terpenuhi.
   - Akhirnya, hasil akhir akan berupa alokasi sumber daya yang optimal dari setiap asal ke setiap tujuan dengan biaya atau keuntungan minimum atau maksimum, sesuai dengan kasus yang diberikan.

Metode Vogel's Approximation Method (VAM) mempertimbangkan biaya diferensial antara baris dan kolom dalam tabel transportasi untuk memperbaiki solusi awal yang diperoleh dari Metode North West Corner. Ini membantu dalam mendapatkan solusi awal yang lebih baik dan meminimalkan biaya atau maksimalkan keuntungan dalam pemecahan masalah transportasi.
''')