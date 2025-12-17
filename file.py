"""Program manajemen nilai dan presensi mahasiswa. Program ini kami buat 
sebagai tugas akhir pemrograman Python dengan konsep class, loop, dan file
handling. Data mahasiswa disimpan dalam file csv agar tidak hilang saat program
ditutup."""

import csv
import os

DATA_FILE = "students.csv"  # file CSV yang menyimpan semua data mahasiswa

class Student:
        def __init__(self, nim, nama, nilai_tugas=0, nilai_uts=0, nilai_uas=0,):
            self.nim = nim
            self.nama = nama
            self.tugas = 0
            self.uts = 0
            self.uas = 0
            self.presensi = []
            
        def hitung_nilai_akhir(self):
         nilai_akhir = (0.3 * self.tugas) + \
                      (0.35 * self.uts) + \
                      (0.35 * self.uas)
         return nilai_akhir

        def hitung_persentase_hadir(self):
         if not self.presensi:
            return 0.0
         return (self.presensi.count("H") / len(self.presensi)) * 100

        def to_csv_row(self):
         return [
           self.nim,
           self.nama,
           self.tugas,
           self.uts,
           self.uas,
           "|".join(self.presensi)
         ]

        @staticmethod
        def from_csv_row(row):
          mhs = Student(row[0], row[1])
          mhs.tugas = float(row[2]) if row[2] else 0
          mhs.uts   = float(row[3]) if row[3] else 0
          mhs.uas   = float(row[4]) if row[4] else 0

          mhs.presensi = row[5].split("|") if len(row) > 5 and row[5] else []

          return mhs

       
# ---- Utility / Data store ----
students = []  # Variabel students digunakan untuk menyimpan data semua mahasiswa

def load_data():            # variabel untuk membaca data mahasiswa
    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header

        for row in reader:
            mhs = Student(row[0], row[1])
            mhs.tugas = float(row[2]) if row[2] else 0
            mhs.uts = float(row[3]) if row[3] else 0
            mhs.uas = float(row[4]) if row[4] else 0
            mhs.presensi = row[5].split("|") if row[5] else []
            students.append(mhs)
 

def save_data():                          # variabel untuk menyimpan data mahasiswa
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["NIM", "Nama", "Tugas", "UTS", "UAS", "Presensi"])
        for s in students:
            writer.writerow(s.to_csv_row())

    print("Data mahasiswa berhasil disimpan ke file.")

def find_student_by_nim(nim):
    for mhs in students:
        if isinstance(mhs, Student):
            if mhs.nim == nim:
                return mhs
    return None

# ---- Menu features ----
def tambah_mahasiswa():
    nim = input("Input NIM mahasiswa: ").strip()
    nama = input("Input nama mahasiswa: ").strip()

    mhs = Student(nim, nama)

    if students:
        total_pertemuan = len(students[0].presensi)
        mhs.presensi = ["A"] * total_pertemuan

    students.append(mhs)
    print("Data mahasiswa berhasil disimpan.")


def tampilkan_data_mahasiswa():
    if not students:
        print("Belum ada data mahasiswa.")
        return

    print("\n=== DAFTAR MAHASISWA ===")
    for mhs in students:
        if not isinstance(mhs, Student):
            continue

        print("NIM  :", mhs.nim)
        print("Nama :", mhs.nama)
        print("Tugas:", mhs.tugas)
        print("UTS  :", mhs.uts)
        print("UAS  :", mhs.uas)
        print("-" * 30)

def hapus_mahasiswa ():
    nim = input("Masukkan NIM yang akan dihapus: ").strip()
    mahasiswa = find_student_by_nim(nim)

    if mahasiswa is None:
        print("Data tidak ditemukan")
        return
    
    students.remove(mahasiswa)
    print("Data mahasiswa berhasil dihapus.")


def input_nilai_akademik():
    nim = input("Masukkan NIM: ").strip()
    s = find_student_by_nim(nim)

    if s is None:
        print("Mahasiswa tidak ditemukan.")
        return

    try:
        s.tugas = float(input("Nilai Tugas: "))
        s.uts = float(input("Nilai UTS: "))
        s.uas = float(input("Nilai UAS: "))
        print("Nilai berhasil disimpan.")
    except ValueError:
        print("Input nilai harus angka.")


def input_score(prompt, current_value):
    while True:
        val = input(prompt).strip()

        # jika ENTER ditekan, nilai lama dipakai
        if val == "":
            return current_value

        try:
            f = float(val)
            if 0 <= f <= 100:
                return f
            else:
                print("Nilai harus di antara 0 dan 100.")
        except ValueError:
            print("Masukkan angka yang valid.")


# Lambda function untuk konversi grade  = konversi_grade(nilai)
def konversi_grade(nilai):
    if nilai >= 85:
        return "A"
    elif nilai >= 70:
        return "B"
    elif nilai >= 55:
        return "C"
    elif nilai >= 40:
        return "D"
    else:
        return "E"
    

def input_presensi():
    if not students:
        print("Belum ada data mahasiswa.")
        return

    for s in students:
        pertemuan_ke = len(s.presensi) + 1

        # Menentukan sesi berdasarkan pertemuan (logika modulus)
        if pertemuan_ke % 2 == 1:
            sesi = "Teori"
        else:
            sesi = "Praktikum"

        while True:
            status = input(
                f"Pertemuan {pertemuan_ke} | "
                f"Sesi {sesi} | "
                f"NIM {s.nim} Nama {s.nama} (H/A/I): "
            ).strip().upper()

            if status in ("H", "A", "I"):
                s.presensi.append(status)
                break
            else:
                print("Masukkan H, A, atau I.")

def tampilkan_laporan():
    if not students:
        print("Belum ada data mahasiswa.")
        return

    print("\nNIM    | Nama     | Akhir | Grade | Hadir")
    print("-" * 50)

    for s in sorted(students, key=lambda x: x.nim):
        nilai = s.hitung_nilai_akhir()
        grade = konversi_grade(nilai)

        hadir = s.presensi.count('H')
        total = len(s.presensi)

        persen = (hadir / total * 100) if total > 0 else 0

        print(f"{s.nim:<6} | {s.nama:<8} | {nilai:5.1f} | {grade:^5} | {persen:5.1f}%")



def save_and_exit():
    save_data()
    print("Data disimpan ke", DATA_FILE)
    print("Keluar program. Sampai jumpa!")
    exit(0)

def main_menu():
    load_data()
    menu_actions = {
        "1": tambah_mahasiswa,
        "2": tampilkan_data_mahasiswa,
        "3": hapus_mahasiswa,
        "4": input_nilai_akademik,
        "5": input_presensi,
        "6": tampilkan_laporan,
        "7": save_data,
        "8": save_and_exit
    }

    while True:
        print("\n=== MENU UTAMA SISTEM MAHASISWA ===")
        print("1. Tambah data Mahasiswa")
        print("2. Tampilkan Data Mahasiswa")
        print("3. Hapus data Mahasiswa")
        print("4. Input Nilai Akademik (Tugas/UTS/UAS)")
        print("5. Input Presensi (pertemuan)")
        print("6. Tampilkan Laporan / Data")
        print("7. Simpan Data")
        print("8. Keluar (Simpan otomatis)")

        pilihan = input("pilih menu: ")

        if pilihan == "1":
            tambah_mahasiswa()
        elif pilihan == "2":
            tampilkan_data_mahasiswa()
        elif pilihan == "3":
            hapus_mahasiswa()
        elif pilihan == "4":
            input_nilai_akademik()
        elif pilihan == "5":
            input_presensi()
        elif pilihan == "6":
            tampilkan_laporan()
        elif pilihan == "7":
            save_data()
        elif pilihan == "8":
            print("Program selesai.")
            break
        else:
            print("Menu tidak valid.")
        
        input ("\nTekan Enter untuk kembali ke menu...")
            

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt diterima. Menyimpan data sebelum keluar...")
        save_data()
        print("Selesai.")