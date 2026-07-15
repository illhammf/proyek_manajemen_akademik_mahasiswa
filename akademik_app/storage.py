"""
storage.py
Class FileManager bertugas membaca dan menyimpan data ke file JSON.
Pemisahan ini membuat kode lebih rapi karena logic penyimpanan tidak bercampur dengan menu aplikasi.
"""

import json
from pathlib import Path
from typing import Dict, Any


class FileManager:
    def __init__(self, file_path: str):
        self.__file_path = Path(file_path)
        self.__file_path.parent.mkdir(parents=True, exist_ok=True)

    def get_file_path(self) -> Path:
        return self.__file_path

    def file_ada(self) -> bool:
        return self.__file_path.exists()

    def baca_json(self) -> Dict[str, Any]:
        if not self.file_ada():
            return {}
        with self.__file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def simpan_json(self, data: Dict[str, Any]) -> None:
        with self.__file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
