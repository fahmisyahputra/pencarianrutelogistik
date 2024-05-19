Cara Run app.py dan Install dependecy/modul non global dengan venv


*Direkomendasikan agar menyamakan versi python 3.12.3. Cek versi python :

```
python --version
```

1. Bikin venv

```
python -m venv venv
```

2. Aktifkan venv

```
# Cari file activate di venv, secara umum kyk gini :
./venv/Scripts/activate
```

3. Install modul

```
pip install -r requirements.txt
```

4. Run app.py
```
python app.py
```
