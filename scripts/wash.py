import re
import os
import subprocess

src_folder = "/home/qzh/Desktop/zh-google-styleguide-master/google-cpp-styleguide/convert"
dst_folder = os.path.join(src_folder, "output")

if not os.path.exists(dst_folder):
    os.mkdir(dst_folder)

processed_filepaths = []

for root, dirs, files in os.walk(src_folder):
    if root == src_folder:
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(dst_folder, file.replace(".rst", ".md"))
            subprocess.run(["pandoc", src, "-f", "rst", "-t", "markdown", "-o", dst])
            processed_filepaths.append(dst)

title_pattern = re.compile(r"^#+(.+)\{\#(\S+?)\}$", re.M)

id_file_dic = {}
id_title_dic = {}
for filepath in processed_filepaths:
    with open(filepath, "r") as file:
        text = file.read()
        filename = os.path.splitext(os.path.basename(filepath))[0]
        matches = title_pattern.findall(text)
        for match in matches:
            title_id = match[1].strip()
            if title_id in id_file_dic.keys():
                print(title_id)
                print(filename)
            else:
                id_file_dic[title_id] = filename
                match2 = re.match(r"^[0-9.\s]*(.+?)\s*$", match[0])
                if match2:
                    id_title_dic[title_id] = match2.groups()[0].replace("`", "")
                else:
                    raise Exception("o fuck")

print(id_title_dic)

def f(match):
    group = match.groups()
    if group[1] in id_file_dic.keys():
        if id_file_dic[group[1]] == filename:
            return "[" + group[0].strip() + "](#" + group[1] + ")"
        else:
            return "[" + group[0].strip() + "](" + id_file_dic[group[1]] + "#" + group[1] + ")"
    else:
        raise Exception("fuck")
    
def f2(match):
    group = match.groups()
    if group[0] in id_file_dic.keys():
        if id_file_dic[group[0]] == filename:
            return "[" + id_title_dic[group[0]] + "](#" + group[0] + ")"
        else:
            return "[" + id_title_dic[group[0]] + "](" + id_file_dic[group[0]] + "#" + group[0] + ")"
    else:
        raise Exception("fuck")
    
link_pattern1 = re.compile(r"\`(.+)\<(\S+)\>\`\{\.interpreted-text\s+role=\"ref\"\}")
link_pattern2 = re.compile(r"\`(\S+)\`\{\.interpreted-text\s+role=\"ref\"\}")

for filepath in processed_filepaths:
    filename = os.path.splitext(os.path.basename(filepath))[0]
    with open(filepath, "r") as file:
        output = link_pattern1.sub(f, file.read())
        output = link_pattern2.sub(f2, output)
    with open(filepath, "w") as file:
        file.write(output)
