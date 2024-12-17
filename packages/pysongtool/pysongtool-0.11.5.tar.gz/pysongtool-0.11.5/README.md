# PySongTool

### 🎵 **Music Theory with Python**
**Version**: beta 0.10

PySongTool is a Python library designed to help provide information involving music theory

This project follows **SOLID** principles and uses the **Facade** design pattern to organize and simplify the management of classes and functions.

---

## 📚 **Requirements**

- Python >= 3.7

---

## 🔧 **Installation**

You can install PySongTool directly from PyPI (when available) or locally:

```bash
pip install pysongtool
```

Or clone the repository and install it manually:

```
git clone https://github.com/your-username/pysongtool.git
cd pysongtool
pip install .
```

---

## 🗂 **Features**

- Generate chords from a root note and chord name.
- Get all available scales or chords.
- Explore musical intervals based on a root note.
- Retrieve detailed scale information, including notes and associated chords.

---

## 🚀 **How to Use**

### Creating an Instance
```python
from pysongtool import PySongTool

tool = PySongTool()
```
### Generating a Chord
```python
result = tool.chord('C', 'major')
print(result)
# {'chord': 'Cmaj', 'notes': ['C', 'E', 'G']}
```

### Listing All Chords
```python
all_chords = tool.all_chords('C')
print(all_chords)
# [{'maj': {'chord': 'Cmaj', 'notes': ['C', 'E', 'G']}}, ...]
```

### Generating a Scale
```python
scale = tool.scale('C', 'major')
print(scale)
# {'notes': ['C', 'D', 'E', 'F', 'G', 'A', 'B'], 'chords': ['Cmaj', 'Dmin', ...]}
```

### Getting Intervals
```python
intervals = tool.intervals('C')
print(intervals)
# [{'name': 'Unison', 'semitones': 0, 'note': 'C'}, ...]
```

### Calculating Intervals Between Notes
```python
intervals = tool.get_interval('C', 'E', 'G')
print(intervals)
# [{'note': 'E', 'interval': {'name': 'Major Third', 'semitones': 4}}, ...]
```

## 🛠 **Contributing**

Contributions are welcome!

---

## 📝 **License**
This project is licensed under the [MIT License](LICENSE).  

---