import os
import datetime
import subprocess

# Kita geser mulai dari minggu ke-8 ke belakang agar tulisan persis di tengah tahun
START_WEEK = 8 
COMMITS_PER_PIXEL = 10 

# Peta Piksel Presisi Tinggi (Grid 5x7 Klasik)
pixels = [
    # L (Lebar 4)
    (0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0),
    (6,1), (6,2), (6,3),

    # U (Lebar 5)
    (0,5), (1,5), (2,5), (3,5), (4,5), (5,5),
    (0,9), (1,9), (2,9), (3,9), (4,9), (5,9),
    (6,6), (6,7), (6,8),

    # K (Lebar 5)
    (0,11), (1,11), (2,11), (3,11), (4,11), (5,11), (6,11),
    (0,15), (1,14), (2,13), (3,12), (4,13), (5,14), (6,15),

    # A (Lebar 5)
    (0,19),
    (1,18), (1,20),
    (2,17), (2,21),
    (3,17), (3,18), (3,19), (3,20), (3,21),
    (4,17), (4,21),
    (5,17), (5,21),
    (6,17), (6,21),

    # Y (Lebar 5)
    (0,23), (0,27),
    (1,23), (1,27),
    (2,24), (2,26),
    (3,25), (4,25), (5,25), (6,25),

    # ? (Lebar 5)
    (0,32), (0,33), (0,34),
    (1,31), (1,35),
    (2,35),
    (3,34),
    (4,33),
    # Baris 5 kosong untuk jeda titik
    (6,33)
]

def make_commit(days_ago):
    date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")
    
    with open("riwayat.txt", "a") as f:
        f.write(f"Titik piksel pada {formatted_date}\n")
    
    subprocess.run(["git", "add", "riwayat.txt"], check=True)
    
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = formatted_date
    env["GIT_COMMITTER_DATE"] = formatted_date
    subprocess.run(["git", "commit", "-m", "menggambar huruf"], env=env, stdout=subprocess.DEVNULL, check=True)

def main():
    print("Mulai menimpa piksel agar simetris...")
    if not os.path.exists("riwayat.txt"):
        with open("riwayat.txt", "w") as f:
            f.write("Kanvas dimulai\n")
            
    total = len(pixels)
    current = 0
            
    for row, col_offset in pixels:
        current += 1
        print(f"Menggambar piksel {current}/{total}...")
        days_ago = (52 * 7) - ((START_WEEK + col_offset) * 7) + row
        for _ in range(COMMITS_PER_PIXEL):
            make_commit(days_ago)
            
    print("\nSelesai! Silakan jalankan: git push origin main")

if __name__ == "__main__":
    main()