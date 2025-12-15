import shutil
import os
import glob
import re
import subprocess

should_convert = True
should_decode_banks = True
should_group = True
# Only set this if the additional steps in the README have been completed
should_rename = False

# Make sure to escape backslahes! (i.e. replace `\` with `\\`)
wwiser_pyz = ""
folder_vgmstream = ""
folder_unpacked_data = ""
folder_audio_converted = ""
# Only required if should_rename is True
folder_bg3sids_wiki = ""


def convert_wem_folder(source_dir: str, dest_dir: str):
    cwd = os.getcwd()
    os.chdir(folder_vgmstream)

    wems = glob.glob(f"{source_dir}\\*.wem")
    total = len(wems)
    wem_index = 0
    print(f"\r  {wem_index}/{total}", end="", flush=True)
    for wem in wems:
        _, filename = os.path.split(wem)
        subprocess.call(
            [ "vgmstream-cli",
                "-o",
                os.path.join(dest_dir, f"{filename}.wav"),
                os.path.join(source_dir, filename),
            ],
            stdout=subprocess.DEVNULL,
        )
        wem_index = wem_index + 1
        print(f"\r  {wem_index}/{total}", end="", flush=True)

    print(f"\r  {wem_index}/{total}")
    os.chdir(cwd)


def decode_banks(source_dir: str):
    banks = glob.glob(f"{source_dir}\\*.bnk")
    total = len(banks)
    bank_index = 0
    print(f"\r  {bank_index}/{total}", end="", flush=True)
    for bank in banks:
        subprocess.call(
            [ "python", wwiser_pyz, "-d", "xsl", bank ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        bank_index = bank_index + 1
        print(f"\r  {bank_index}/{total}", end="", flush=True)
    print(f"\r  {bank_index}/{total}")


def create_banks_folders(banks_dir: str, sounds_dir: str):
    banks_xmls = glob.glob(f"{banks_dir}\\*.bnk.xml")
    total = len(banks_xmls)
    bank_folder_index = 0
    print(f"\r  {bank_folder_index}/{total}", end="", flush=True)
    for bank_filename in banks_xmls:
        bank_folder = os.path.basename(bank_filename).split(".")[0]
        if not os.path.exists(f"{sounds_dir}\\{bank_folder}"):
            os.makedirs(f"{sounds_dir}\\{bank_folder}")
        with open(bank_filename, "r") as bank_file_content:
            for line in bank_file_content:
                if 'name="sourceID"' in line:
                    ids = line.split('"')[-2]
                    filename = f"{ids}.wem.wav"
                    if filename in os.listdir(sounds_dir):
                        shutil.move(
                            f"{sounds_dir}\\{filename}",
                            f"{sounds_dir}\\{bank_folder}\\{filename}",
                        )
        bank_folder_index = bank_folder_index + 1
        print(f"\r  {bank_folder_index}/{total}", end="", flush=True)
    print(f"\r  {bank_folder_index}/{total}")


def rename_files(source: str):
    folders = glob.glob(f"{source}/*/")
    total = len(folders)
    rename_folder_index = 0
    print(f"\r  {rename_folder_index}/{total}", end="", flush=True)

    markdown_files = glob.glob(f"{folder_bg3sids_wiki}\\*.bnk.md")

    for folder_path in folders:
        folder_name = os.path.basename(os.path.normpath(folder_path))

        markdown_file = None
        for file_name in markdown_files:
            if f"{folder_name}-" in file_name or f"{folder_name}.bnk.md" in file_name:
                markdown_file = file_name
                break

        if markdown_file is None:
            print(f"\r  No mappings found for {folder_name}")
            continue

        # The bank in the Ambience pack has nicer names than Amb, so use that.
        # I don't know of any other duplicated IDs, but they may exist.
        if "Amb_[PAK]_Amb_Ps_Specific-_-AMB_PS_SPECIFIC.bnk.md" in markdown_file:
            markdown_file = f"{folder_bg3sids_wiki}\\Ambience_[PAK]_Amb_Ps_Specific-_-AMB_PS_SPECIFIC.bnk.md"

        id_dict = {}
        with open(markdown_file, "r") as markdown_file_content:
            for line in markdown_file_content:
                line_match = re.match(r"^\| \d+ \| (\w+) \| (.*) \|$", line)
                if line_match is not None:
                    base_name = line_match.group(1)
                    ids = line_match.group(2).split(", ")
                    for sound_match_index in range(len(ids)):
                        id = ids[sound_match_index]
                        id_dict[id] = f"{base_name}_{sound_match_index}"

        # For files in dir, rename by looking up id
        # if no id, do nothing
        sounds = glob.glob(f"{folder_path}\\*.wem.wav")
        for sound in sounds:
            sound_id = os.path.basename(sound).split(".")[0]
            if sound_id in id_dict:
                os.rename(sound, os.path.join(folder_path, f"{id_dict[sound_id]}.wav"))

        rename_folder_index = rename_folder_index + 1
        print(
            f"\r  {rename_folder_index}/{total}",
            end="",
            flush=True,
        )
    print(f"\r  {rename_folder_index}/{total}")


src_sound = os.path.join(
    folder_unpacked_data, "SharedSounds\\Public\\Shared\\Assets\\Sound"
)
src_sound_dev = os.path.join(
    folder_unpacked_data, "SharedSounds\\Public\\SharedDev\\Assets\\Sound"
)
src_banks = os.path.join(
    folder_unpacked_data, "SharedSoundBanks\\Public\\Shared\\Assets\\Sound"
)
src_banks_dev = os.path.join(
    folder_unpacked_data, "SharedSoundBanks\\Public\\SharedDev\\Assets\\Sound"
)

dest_sound = os.path.join(folder_audio_converted, "Shared")
dest_sound_dev = os.path.join(folder_audio_converted, "SharedDev")


os.makedirs(src_sound, exist_ok=True)
os.makedirs(src_sound_dev, exist_ok=True)
os.makedirs(src_banks, exist_ok=True)
os.makedirs(src_banks_dev, exist_ok=True)
os.makedirs(dest_sound, exist_ok=True)
os.makedirs(dest_sound_dev, exist_ok=True)

if should_convert:
    print("Converting sound files")
    print("  Shared")
    convert_wem_folder(src_sound, dest_sound)
    print("  SharedDev")
    convert_wem_folder(src_sound_dev, dest_sound_dev)

if should_decode_banks:
    print("Decoding sound banks")
    print("  Shared")
    decode_banks(src_banks)
    print("  SharedDev")
    decode_banks(src_banks_dev)

if should_group:
    print("Grouping files by bank")
    print("  Shared")
    create_banks_folders(src_banks, dest_sound)
    print("  SharedDev")
    create_banks_folders(src_banks_dev, dest_sound_dev)

if should_rename:
    print("Renaming files")
    print("  Shared")
    rename_files(dest_sound)
    print("  SharedDev")
    rename_files(dest_sound_dev)

print("Done")
