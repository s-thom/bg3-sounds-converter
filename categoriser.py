import shutil
import os
import glob
import subprocess

should_convert = True
should_decode_banks = True
should_group = True

# Make sure to escape backslahes! (i.e. replace `\` with `\\`)
wwizer_pyz = ""
folder_vgmstream = ""
folder_unpacked_data = ""
folder_audio_converted = ""


def convert_wem_folder(source, dest):
    cwd = os.getcwd()
    os.chdir(folder_vgmstream)

    wems = glob.glob(f"{source}\\*.wem")
    total = len(wems)
    i = 0
    print(f"\r  {i}/{total}", end="", flush=True)
    for wem in wems:
        _, filename = os.path.split(wem)
        subprocess.call(
            f"vgmstream-cli -o {dest}\\{filename}.wav {source}\\{filename}",
            shell=True,
            stdout=subprocess.DEVNULL,
        )
        i = i + 1
        print(f"\r  {i}/{total}", end="", flush=True)

    print(f"\r  {i}/{total}")
    os.chdir(cwd)


def decode_banks(source):
    banks = glob.glob(f"{source}\\*.bnk")
    total = len(banks)
    i = 0
    print(f"\r  {i}/{total}", end="", flush=True)
    for bank in banks:
        subprocess.call(
            f"python {wwizer_pyz} -d xsl {bank}",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        i = i + 1
        print(f"\r  {i}/{total}", end="", flush=True)
    print(f"\r  {i}/{total}")


def create_banks_folders(banks, sounds):
    banks_xmls = glob.glob(f"{banks}\\*.bnk.xml")
    total = len(banks_xmls)
    i = 0
    print(f"\r  {i}/{total}", end="", flush=True)
    for bank_filename in banks_xmls:
        bank_folder = os.path.basename(bank_filename).split(".")[0]
        if not os.path.exists(f"{sounds}\\{bank_folder}"):
            os.makedirs(f"{sounds}\\{bank_folder}")
        with open(bank_filename, "r") as bank_file_content:
            for line in bank_file_content:
                if 'name="sourceID"' in line:
                    ids = line.split('"')[-2]
                    filename = f"{ids}.wem.wav"
                    if filename in os.listdir(sounds):
                        shutil.move(
                            f"{sounds}\\{filename}",
                            f"{sounds}\\{bank_folder}\\{filename}",
                        )
        i = i + 1
        print(f"\r  {i}/{total}", end="", flush=True)
    print(f"\r  {i}/{total}")


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

