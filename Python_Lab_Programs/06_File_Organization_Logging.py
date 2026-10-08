import os
import logging
from shutil import move

folderPath = 'TestFile'

logging.basicConfig(
    filename=os.path.join(folderPath, 'log.txt'),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

folder = {
    '.pdf': "PDF",
    '.png': "Images",
    '.jpg': "Images",
    ".docx": "Documents",
    ".txt": "Documents",
    ".py": "Python Files",
    ".csv": "Data Files",
}

files = os.listdir(folderPath)

for file in files:
    name, extension = os.path.splitext(file)
    if extension in folder:
        folderName = folder[extension]
        destination = os.path.join(folderPath, folderName)

        if not os.path.exists(destination):
            os.makedirs(destination)

        move(
            os.path.join(folderPath, file),
            os.path.join(destination, file)
        )

        logging.info(f"Moved {file} to {folderName}")

print("File organization complete. Check log.txt for details.")
