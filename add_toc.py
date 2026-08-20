import glob
import os

def check_and_add_toc():
    # _posts klasöründeki tüm markdown dosyalarını bul
    post_files = glob.glob(os.path.join('_posts', '*.md'))
    modified_files_count = 0

    for file_path in post_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if not lines:
            continue

        in_front_matter = False
        front_matter_end_idx = -1
        has_toc = False
        heading_count = 0
        in_code_block = False

        # Dosyayı satır satır analiz et
        for i, line in enumerate(lines):
            stripped_line = line.strip()

            # Front matter (---) sınırlarını belirle
            if stripped_line == '---':
                if i == 0:
                    in_front_matter = True
                elif in_front_matter:
                    in_front_matter = False
                    front_matter_end_idx = i
                continue

            if in_front_matter:
                # Zaten toc: ayarı var mı kontrol et
                if stripped_line.startswith('toc:'):
                    has_toc = True
            else:
                # Kod bloğu (```) kontrolü - içindeki # işaretlerini başlık saymamak için
                if stripped_line.startswith('```'):
                    in_code_block = not in_code_block
                    continue
                
                # Sadece normal metin kısmındaki h2 ve h3 başlıklarını say
                if not in_code_block:
                    if stripped_line.startswith('## ') or stripped_line.startswith('### '):
                        heading_count += 1

        # Şartlar sağlanıyorsa toc: true ekle
        if heading_count >= 2 and not has_toc and front_matter_end_idx != -1:
            # toc: true satırını front matter'ın en altına (ikinci --- işaretinden hemen önceye) ekle
            lines.insert(front_matter_end_idx, "toc: true\n")
            
            # Dosyayı yeni haliyle kaydet
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print(f"[Eklendi] {os.path.basename(file_path)} (Bulunan başlık: {heading_count})")
            modified_files_count += 1

    print(f"\nİşlem tamamlandı. Toplam {modified_files_count} dosyaya 'toc: true' eklendi.")

if __name__ == "__main__":
    check_and_add_toc()