import shutil
import os
import glob
import subprocess

should_convert = True
should_decode_banks = True
should_categorise = True

wwizer_pyz = ""
folder_vgmstream = ""
folder_banks = ""
folder_audio_raw = ""
folder_audio_converted = ""


if should_convert:
  cwd = os.getcwd()
  os.chdir(folder_vgmstream)

  wems = glob.glob(f"{folder_audio_raw}\\*.wem")
  for wem in wems:
    _, filename = os.path.split(wem)
    subprocess.call(f'vgmstream-cli -o {folder_audio_converted}\\{filename}.wav {folder_audio_raw}\\{filename}', shell=True)

  os.chdir(cwd)

if should_decode_banks:
  banks = glob.glob(f"{folder_banks}\\*.bnk")
  for bank in banks:
      r = subprocess.call(f'python {wwizer_pyz} -d xsl {bank}', shell=True)

if should_categorise:
  banks_xms = glob.glob(f"{folder_banks}\\*.bnk.xml")
  for bank in banks_xms:
      new_folder = os.path.basename(bank).split(".")[0]
      if not os.path.exists(f"{folder_audio_converted}\\{new_folder}"):
          os.makedirs(f"{folder_audio_converted}\\{new_folder}")
      with open(bank, 'r') as f:
          for line in f:
              if "name=\"sourceID\"" in line:
                  ids = line.split("\"")[-2]
                  filename = f"{ids}.wem.wav"
                  if filename in os.listdir(folder_audio_converted):
                      shutil.move(f"{folder_audio_converted}\\{filename}", f"{folder_audio_converted}\\{new_folder}\\{filename}")
