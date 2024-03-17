import streamlit as st

st.sidebar.title("Transportation Calculator Sidebar")
st.sidebar.subheader('Metode Yang di Inginkan')
# Membuat dropdown menu dengan beberapa pilihan
option = st.selectbox(
    'Pilih sebuah opsi',
    ('Metode North West Corner', 'Vogel Approximation Method (VAM)', 'Monalisha Approximation', 'Modification Distribution (MODI)')
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
elif option == 'Monalisha Approximation':
    st.markdown('# Monalisha Approximation Method')
    st.markdown('''
                Menurut Pattnaik (2015), metode Monalisha merupakan metode
yang biasanya memberikan pemecahan awal yang lebih baik dari
metode VAM. Pada kenyataannya, metode Monalisha umumnya
menghasilkan pemecahan awal yang mendekati hasil optimal (lebih
optimal daripada metode VAM). Langkah-langkah metode Monalisha
dapat diringkas sebagai berikut:
### Langkah-langkah Metode Monalisha

1. **Menentukan tabel biaya dan memeriksa keseimbangan permintaan:**
   - Jika total permintaan sama dengan total penawaran, lanjut ke langkah 2.
   - Jika tidak, tambahkan dummy dan lanjutkan ke langkah 2.

2. **Mengurangi setiap elemen dalam baris dengan nilai terkecil di baris tersebut:**
   - Dilakukan untuk setiap baris dalam matriks biaya.

3. **Mengurangi setiap elemen dalam kolom dengan nilai terkecil di kolom tersebut:**
   - Dilakukan untuk setiap kolom dalam matriks biaya.

4. **Menentukan dua biaya terkecil untuk setiap baris dan kolom:**
   - Selanjutnya, dicari selisihnya dan diletakkan dalam baris atau kolom penalty baru.

5. **Memilih baris penalty terkecil dan kolom penalty terbesar:**
   - Jika terdapat lebih dari satu sel yang memenuhi syarat, lanjut ke langkah 6.
   - Jika hanya terdapat satu sel yang memenuhi syarat, lanjut ke langkah 7.

6. **Identifikasi baris dan kolom dengan total biaya semula terkecil dan terbesar:**
   - Jika terdapat lebih dari satu sel yang memenuhi syarat, dipilih secara acak.

7. **Alokasikan jumlah maksimum yang layak pada sel terpilih:**
   - Menggunakan formula: $X_{i,j} = min(a_{i}, b_{j})$ pada sel $(i, j)$ .
   - Mengabaikan baris atau kolom yang sudah teralokasikan semua supply dan demand.

8. **Memeriksa apakah semua supply dan demand sudah teralokasikan:**
   - Jika tidak, kembali ke langkah 2.
   - Jika iya, lanjut ke langkah 9.

9. **Menambahkan nol pada sel kosong jika pengisian kurang dari $m + n - 1:$**
   - Tujuannya agar memenuhi syarat terisi sebanyak $m + n - 1$ sel.

''')

elif option =='Modification Distribution (MODI)':
    st.markdown('''
                Menurut Aminudin (2005), metode MODI adalah salah satu
solusi optimal dan lebih efisien daripada metode Stepping Stone.
Solusi optimal diperoleh setelah mengerjakan solusi awal. Menurut
Nasendi dan Anwar (1985), langkah-langkah metode MODI adalah
sebagai berikut:
### Langkah-langkah Metode MODI

1. **Seleksi biaya sel yang sudah teralokasi pada solusi awal:**
   - Mengabaikan biaya sel yang tidak terpilih pada solusi awal.
   - Menyimpan hasil akhir solusi awal dalam matriks A.

2. **Penentuan biaya $C_{i,j} = U_{i} + V_{j} (U_{i}$ = biaya baris, $V_{j}$ = biaya kolom):**
   - Dimulai dengan $U_{1} = 0$ .

3. **Melengkapi biaya sel yang diabaikan pada langkah 1:**
   - Menjumlahkan $C_{i,j} = U_{i} + V_{j}$ dan disimpan dalam matriks R.

4. **Pengurangan matriks A dengan matriks R:**
   - Memeriksa hasil operasi pengurangan apakah terdapat nilai negatif.
     - Jika ada, kembali ke langkah 5.
     - Jika tidak, lanjut ke langkah 6.

5. **Memindahkan biaya sel negatif ke sel lain yang kosong:**
   - Memastikan jumlah sel terisi sama dengan $m + n - 1$ .
     - Jika tidak, tambahkan nol pada sel kosong dan kembali ke langkah 2.

6. **Penentuan nilai Z dari matriks R terakhir:**
''')

else:
    st.markdown('# Vogel Approximation Method (VAM)')
    st.markdown('''
                Menurut Aminudin (2005), metode VAM merupakan metode
heuristik dan biasanya memberikan pemecahan awal yang lebih baik
dari metode NWC dan LC. Pada kenyataannya, metode VAM
umumnya menghasilkan pemecahan awal yang mendekati hasil
optimal. Langkah-langkah metode VAM dapat diringkas sebagai
berikut:
### Langkah-langkah Metode VAM

1. **Menentukan apakah termasuk transportasi seimbang:**
   - Jika tidak, akan ditambahkan dummy dan dilanjutkan ke langkah 2.
   - Jika iya, dilanjutkan ke langkah 2.

2. **Mencari selisih dari dua sel terkecil pada tiap baris dan kolom:**
   - Selisih tersebut dimasukkan pada baris atau kolom penalty.

3. **Menentukan baris atau kolom dengan penalty terbesar:**
   - Jika terdapat lebih dari satu, dipilih secara acak.
   - Jika hanya terdapat satu, otomatis terpilih.

4. **Mengisikan barang secara maksimum pada sel terpilih:**
   - Menggunakan formula: $X_{i,j} = min(a_{i}, b_{j})$ pada sel $(i, j)$ .
   - Mengabaikan baris atau kolom yang sudah teralokasikan semua supply dan demand.

5. **Memeriksa apakah semua supply dan demand sudah teralokasikan:**
   - Jika tidak, kembali ke langkah 2.
   - Jika iya, dilanjutkan ke langkah 6.

6. **Menambahkan nol pada sel kosong jika pengisian kurang dari $m + n - 1:$**
   - Tujuannya agar memenuhi syarat terisi sebanyak $m + n - 1$ sel.

7. **Menghitung nilai solusi awal Z dari metode VAM.**

''')
    