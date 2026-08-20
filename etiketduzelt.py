import glob
import re

def tr_lower(text):
    # Türkçe I/İ harflerini küçük harfe düzgün çevir
    return text.replace('I', 'ı').replace('İ', 'i').lower()

def tr_title_word(word):
    # Kelimenin ilk harfini büyük, kalanını küçük yap (Türkçe uyumlu)
    if not word: return word
    first = word[0]
    rest = word[1:]
    
    if first == 'i': first = 'İ'
    elif first == 'ı': first = 'I'
    else: first = first.upper()
    
    rest = tr_lower(rest)
    return first + rest

for file_path in glob.glob("_posts/*.md"):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    in_front_matter = False
    current_block = None
    changed = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Front matter sınırlarını belirle
        if stripped == '---':
            in_front_matter = not in_front_matter
            current_block = None
            continue
            
        if in_front_matter:
            # Hangi bloğun (tags/categories) içinde olduğumuzu tespit et
            if ':' in line and not line.startswith(' ') and not line.startswith('-'):
                if line.startswith('tags:'):
                    current_block = 'tags'
                elif line.startswith('categories:'):
                    current_block = 'categories'
                else:
                    current_block = None
                    
            if current_block == 'tags':
                # Sadece değer kısmını küçük harf yap
                if line.startswith('tags:'):
                    prefix = line[:line.index(':')+1]
                    content = line[line.index(':')+1:]
                    new_line = prefix + tr_lower(content)
                else:
                    new_line = tr_lower(line)
                    
                if new_line != line:
                    lines[i] = new_line
                    changed = True
                    
            elif current_block == 'categories':
                # Değer kısmındaki kelimelerin ilk harflerini büyük yap
                def process_categories(text):
                    # Regex ile sadece harfleri yakalayıp Title Case yapıyoruz
                    return re.sub(r'([A-Za-zÇĞİÖŞÜçğıöşü]+)', lambda m: tr_title_word(m.group(1)), text)
                    
                if line.startswith('categories:'):
                    prefix = line[:line.index(':')+1]
                    content = line[line.index(':')+1:]
                    new_line = prefix + process_categories(content)
                else:
                    new_line = process_categories(line)
                    
                if new_line != line:
                    lines[i] = new_line
                    changed = True
                    
    # Değişiklik varsa kaydet
    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

print("Etiketler küçük harfe, kategorilerin ilk harfleri büyük harfe dönüştürüldü!")