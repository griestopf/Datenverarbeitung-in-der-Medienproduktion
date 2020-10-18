---
title: Übung 6 - Addon-Entwicklung und VS Code
---

Wenn Scripting-Projekte komplexer werden, wird es irgendwann sehr unübersichtlich im Blender-internen Texteditor an einem einzigen riesigen Script zu arbeiten. Zudem wollen wir anderen Nutzern ermöglichen unseren Code ausuführen, ohne jedesmal Scripte zu kopieren und auszuführen. Zu diesem Zweck werden wir in dieser Übung unseren Code in ein Addon bündeln und uns die Entwicklung mit der IDE Visual Studio Code erleichtern.



```python
bl_info = {
    "name": "New Object",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}
```
