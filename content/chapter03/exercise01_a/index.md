---
title: Übung 3 - Operatoren & Addons
---

![Würfeldimension](img/wuerfeldimension.png)

<!--
**Addon mit UI erstellen um Würfeldimension zu generieren:**

- Set an Türmchenassets generieren
- Mit Voronoi Diagram (Kollisionsfrei - oder doch Partikelsystem wenn zu kompliziert) auf Fläche verteilen
- Würfel bis zum Horizont - hübsch rendern (bei Bedarf vorgegebene Szene)
-->

Bisher sind alle Funktionalitäten, die wir mit unseren Scripten erstellt haben auch nur als solche ausführbar - als Script im Texteditor. In dieser Übung wollen wir das ändern und Blender selbst um eine Benutzeroberfläche für die Generierung unseres Turms erweitern

## Operatoren {{<doclink "https://docs.blender.org/api/current/bpy.types.Operator.html">}}

Wir haben bereits die `ops` Kategorie des `bpy` Moduls kennengelernt. Nun wollen wir unseren eigenen Operator schreiben, der dann auch über die API aufgerufen und mit der `F3`-Suche gefunden werden kann.


{{<todo>}}
- öffne im Text Editor das *"Operator Simple"* Template.
![Simple Operator Template](img/template.png)
{{</todo>}}

Sehen wir uns hier nun ersteinmal die Klasse `SimpleOperator an`
```python
class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}
```

- Mit der Deklaration **`class SimpleOperator(bpy.types.Operator)`** geben wir an, dass unsere Klasse ein Operator ist - also von `bpy.types.Operator` erbt.
- Darunter können wir mit **`"""Mein Tooltipp"""`** eine Beschreibung angeben, die dem Nutzer beim überfahren des Operators mit dem Cursor angezeigt wird.
- **`bl_idname`** ist der API-Pfad unter dem der Operator aufrufbar sein wird `"object.simple_operator"` lässt sich dann mit `bpy.ops.object.simple_operator()` aufrufen.
- **`bl_label`** ist der Name, unter dem der Operator auftaucht, wenn er in das Blender-UI, z. B. in ein Menü, eingefügt wird.
<!--Warum ist poll classmethod und execute nicht?-->
- Die **`poll`** Methode ist optional. Sie ist eine statische Methode (daher `@classmethod`) und benötigt daher keine Instanz der Klasse, um aufgerufen zu werden. `cls` ist hier die Referenz auf die sie beinhaltende Klasse selbst (während `self` immer eine Instanz referenziert). Poll empfängt zudem den aktuellen Kontext.

- Die **`execute`** Methode ist der tatsächlich ausgeführte Code beim aufrufen des Operators. Ihr wird hier `self` übergeben (in Python wird über `self.meine_variable` auf Membervariablen der aktuellen Klasseninstanz zugegriffen) und wiederum der aktuelle Kontext.

Der ausgeführte Code wurde hier in die `main` Methode ausgelagert. Diese könnte auch anders heißen und andere Parameter haben. In diesem Beispiel wird über jedes Objekt in der aktuellen Szene `context.scene.objects` iteriert und dieses in der Konsole ausgegeben. `for` lässt dich in Python nutzen wie `foreach` in anderen Sprachen.

Schließlich fallen noch die drei Methoden `menu_func`, `register` und `unregister` auf.
- **`menu_func`** wird vom Blender-UI aufgerufen und "rendert" den Operator, z. B. als Menüeintrag, in die Umgebung, unter der der Operator ins UI eingefügt wurde.
- **`register`** dient zur Registrierung des Add-ons und wird u. a. aufgerufen, wenn unter Edit -> Preferences -> Add-ons das Add-on durch Klick auf die Check-Box aktiviert wird. Die Methode registriert das Add-on als Befehl und fügt einen Eintrag ins Object-Menü (`VIEW3D_MT_object`) des 3D-Views ein.
- **`unregister`** ist die zu `register` symmetrische Methode zur Deregistrierung. Sie wird u. a. aufgerufen, wenn unter Edit -> Preferences -> Add-ons das Add-on durch Klick auf die Check-Box deaktiviert wird. Dann wird der Eintrag im Object-Menü gelöscht und die Klasse als Operator deregestiert

<!--
{{<info>}}
Wenn viele Klassen zu registrieren sind, lässt sich auch die `register_classes_factory` nutzen, der ein Tuple an Klassen übergeben wird.

```python
register, unregister = bpy.utils.register_classes_factory(
    (MeineKlasse1,
    MeineKlasse2,
    MeineKlasse3,)
)
```
{{</info>}}
-->

- Zu guter Letzt folgen die etwas kryptischen Zeilen
```python
if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()
```

Ein "fertiges" Add-on wird üblicherweise als Python-Datei (.py) oder als ZIP-Datei, die mehrere Python-Dateien enthalten kann, über Preferences -> Add-ons -> Install installiert. In diesem Fall wird beim Aktivieren/Deaktivieren die hinterlegte `register` und `unregister`-Methode aufgerufen. Falls das Skript nicht installiert wird, sondern mit dem "Play"-Button aus dem Text-Editor aufgerufen, ist die Bedingung in `if __name__ == "__main__"` positiv. Dann wird auch - ohne Installationsprozess - die `register`-Methode aufgerufen, so dass das Add-on getestet werden kann. Das Starten eines Add-on-Skriptes direkt aus dem Texteditor findet üblicherweise nur während der Entwicklung des Add-on statt.

{{<info>}}
Beim Registrieren wird das Beispiel-Add-on (der Simple Object Operator ) im Object-Menü des 3D-View hinzugefügt. Jedes mal, wenn das Skript aus dem Text-Editor gestartet wird, wird somit ein neuer Menüeintrag erzeugt. Da niemals `unregister`aufgerufen wird, kommen so immer mehr Menüeinträge hinzu.

Um die Menüeinträge wieder zu löschen, kann im Blender-Icon-Menü der Befehl System -> Reload Scripts ausgeführt werden. 

Alternativ dazu kann auch während des Entwickelns das Aktivieren/Deaktivieren aus dem Preferences -> Add-ons Menü simuliert werden. Dazu muss/darf das Skript nicht per "Play"-Button aus dem Text-Editor gestartet werden. Stattdessen kann folgendes über die interaktive Python-Konsole eingegeben werden:

Zunächst muss dem Skript ein "Namespace gegeben werden". Dabei muss der Skript-Name (hier `operator_simple.py`) dem im Text-Editor angezeigten Namen entsprechen.

```python
>>> mein_addon = bpy.data.texts['operator_simple.py'].as_module()
```

Dann kann es über diesen Namespace registriert werden:

```python
>>> mein_addon.register()
```

und später auch wieder deregistriert werden:

```python
>>> mein_addon.unregister()
```

Um vielfache Menüeinträge zu umgehen, könnte auch die Registrierung des Menüeintrags während der Entwicklungszeit einfach weggelassen werden. Dann ist der Operator nur über seinen 
Python-Namen (`bl_idname`, hier "object.simple_operator") im F3-Menü auffindbar. Allerdings dies auch ***nur***, wenn unter Edit -> Preferences -> Interface die Developer Extras 
aktiviert sind.

Um die Python-Namen anderer Blender-Menüs (außer `VIEW3D_MT_object`) zu erfahren, hilft der jeweilige Python-Tooltip (muss in Edit -> Preferences -> Interface aktiviert sein) beim Hovern über dem Menü-Namen.
{{</info>}}


{{<todo>}}
- Lösche den "test call" aus der letzten Zeile des Add-ons
- Stelle sicher, dass **Preferences → Interface → Developer Extras** aktiviert ist (nur dann lassen sich so erstellte Operatoren mit F3 suchen)
- Führe das Skript *Operator Simple* im Texteditor aus
- Öffne die Systemkonsole mit **Window → Toggle System Console**
- Suche im mit F3 nach *Simple Object Operator*

*Alternativ*
- Lösche den "test call" aus der letzten Zeile des Add-ons
- Führe den Operator über seinen Menüeintrag im Object-Menü des 3D-View aus

In der Systemkonsole wird nun eine Liste der Objekte in der Szene ausgegeben.

{{<console 700px>}}
found bundled python: C:\Blender\daily\blender-2.91.0-7ff6bfd1e0af-windows64\2.91\python
&lt;bpy_struct, Object("Cube") at 0x000001D2821FC088&gt;
&lt;bpy_struct, Object("Light") at 0x000001D2821FC608&gt;
&lt;bpy_struct, Object("Camera") at 0x000001D2821FBB08&gt;>}}
{{</console>}}
{{</todo>}}

## Properties {{<doclink "https://docs.blender.org/api/current/bpy.props.html">}}

Die wenigsten Operatoren sind einfach so ohne weitere Angaben ausführbar. Fast alle Operatoren lassen sich in ihrer Funktionalität durch Parameter beeinflussen. In Blender heißen solche Parameter von Operatoren _Properties_.

Properties lassen sich ganz einfach als Eigenschaften der Klasse, die den Operator definiert implementieren (also die Klasse, die von `bpy.types.Operator` erbt und die eine `execute`-Methode definiert). Hierzu können innerhalb des Klassenrumpfes Eigenschaften definiert werden, denen ein Aufruf einer der folgenden Funktionen zugewiesen wird.

```python
 bpy.props.IntProperty
 bpy.props.BoolProperty
 bpy.props.FloatProperty
 bpy.props.FloatVectorProperty
```

Diesem Funktionsaufruf werden dann `name` (Label des Operators in der GUI), sowie optional eine `description` und ein `default` - Wert zugewiesen.

```python
my_float: bpy.props.FloatProperty(
        name="My Float",
        description="does stuff with the thing.",
        default = 1)
```
{{<info>}}
Es handelt sich hierbei nicht um klassische Variablendeklaration. Wir weisen keinen Wert einer Python-Variablen hinzu, wir sagen Blender nur: "Erstelle in deiner internen Datenstruktur eine Float-Variable mit diesem Namen etc."
{{</info>}}


<pre><code class="language-python">
import bpy

def main(context, loc):
    for ob in context.scene.objects:
        ob.location = loc
</code></pre>

{{<todo>}}


{{<twoculumn>}}
{{<left 50>}}

Passt das **Operator Simple** Template folgendermaßen an:

- Zunächst legen wir in der Operatorklasse eine `FloatVectorProperty` an und weisen ihr Name, Beschreibung und Defaultwert zu.

- Nun können wir unsere Property anwenden. Diese sind innerhalb der Klasse über das Schlüsselwort `self` (ähnlich wie `this` in anderen Sprachen) aufrufbar. In diesem Beispiel Fügen wir unserer `main` Methode einen Parameter `value` hinzu und übergeben bei deren Aufruf in der `execute` Methode `self.my_vector`. 
- Damit beim Ausführen des Operators auch etwas passiert, ändern wir in `main` die Position jedes Objekts zu diesem Wert.

Sind die Properties so der Operatorklasse hinzugefügt, sind sie bei Aufruf des Operators über die Python Konsole bereits einstellbar.

- Führe das Script aus und teste den Operator mit der Python-Konsole:

```
>>> bpy.ops.object.simple_operator(my_vec=(2,2,2))
```

Alle Objekte in der Szene sollten nun an die Position (2, 2, 2) verschoben werden.

![location](img/location.png)



{{</left>}}
{{<right 50>}}
```python
import bpy

def main(context, loc):
    
    for ob in context.scene.objects:
        ob.location = loc

class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context, self.my_vec)
        return {'FINISHED'}

    my_vec: bpy.props.FloatVectorProperty(
        name='My Vector',
        description='does stuff with the thing.',
        default = (1, 1, 1))


def register():
    bpy.utils.register_class(SimpleOperator)

def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()
```
{{</right>}}
{{</twoculumn>}}

- Damit Properties nun auch in einem Menü beim Aufruf des Operators eingestellt werden können, müssen wir das Blender in der Operatorklasse mit einer weiteren bl_... Zeile: `bl_options = {"REGISTER", "UNDO"}` sagen.
- Testet den Operator mit dem `F3` Suchmenü im Viewport

<video autoplay loop src="img/operator.mp4"></video>
{{</todo>}}


{{<todo>}}
Wandelt das [Turmgenerator-Skript](../../course-python-scripts/#vl2-turmgenerator) vom letzten mal in einen Operator um und macht dessen Parameter zu Operator-Properties.
{{</todo>}}

## Addons {{<doclink "https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html">}}
{{<twoculumn>}}
{{<left 50>}}

Nun wollen wir unser Skript als Addon abspeichern, damit es jeder einfach installieren und benutzen kann. Dazu benötigt Blender lediglich ein paar Informationen zum Addon. Diese werden in einem `bl_info` Dictionary (rechts) angegeben, dass wir ganz oben in unser Skript einfügen. Verpflichtend anzugeben sind dabei nur Name, Author und Kategorie. Die vollständige Liste der möglichen Angaben sind im Blender Wiki {{<doclink "https://wiki.blender.org/wiki/Process/Addons/Guidelines/metainfo">}} dokumentiert. 

{{</left>}}
{{<right 50>}}

```python
bl_info = {
    "name": "Operator Simple",
    "author": "Ich <ich@webmail.hs-furtwangen.de>",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "View3D > Object > Operator Simple",
    "description": "Just to show how to hack a blender operator",
    "category": "Object",
    "support": "TESTING",
}
```

{{</right>}}
{{</twoculumn>}}


<!--Dunkle Markdown-CSS Magie
<p class="tabletitle"><b>Nicht selbsterklärende Parameter von bl_info</b></p>

|||
|---|---|
| `version` | gibt die (frei wählbare) Versionsnummer des Addons an.|
| `blender` | ist die Blender Version, mit der das Addon getestet wurde (was nicht heißt, dass es nicht auch in anderen Versionen funktionieren kann)|
| `location` | zeigt den Weg zur UI des Addons (nur als Anleitung für den Nutzer)|
| `doc_url` | Link zur Dokumentation, falls diese existiert (was meist wünschenswert ist)|
| `category` | Gibt die Kategorie unter der das Addon in den Einstellungen angezeigt wird  |
-->


{{<todo>}}

Folgende Folge von Operationen führt einen Schritt eines "Matrix-Extrude" aus, mit dem z. B. aus einer Fläche eines Meshes ein Tentakel extrudiert werden kann

```python
    bpy.ops.mesh.extrude_faces_move( TRANSFORM_OT_shrink_fatten={"value":1.5} )
    bpy.ops.transform.rotate(value = 0.1)
    bpy.ops.transform.resize(value = (0.9, 0.9, 0.9))
```

Erzeugt auf Basis dieser Befehlsfolge ein Matrix-Extrude-Add-on, das die aktuell selektierten Flächen (im Edit-Mode) mehrfach extrudiert. Dabei sollen währende der Ausführung folgende Float-Properties einstellbar sein:

- Anzahl der Wiederholungen (der Schleifendurchläufe, in denen o. a. drei Befehlszeilen durchlaufen werden)
- Extrudierungsabstand pro Wiederholung (in o. a. Code 1.5)
- Rotationswinkel pro Wiederholung in Grad (in o. a. Code 0.1 (Radiant))
- Skalierung der Fläche pro Wiederholung (in o. a. Code (0.0, 0.9, 0.9)). Die Skalierung soll durch einen skalaren Parameter einstellbar sein

Lest die Dokumentation zu bpy.props.FloatProperty {{<doclink "https://docs.blender.org/api/current/bpy.props.html#bpy.props.FloatProperty">}} und wählt aus der Liste der möglichen Parameter geeignete aus, um das Add-on für Benutzer gut bedienbar zu machen.


Als Fingerübung: Wandelt das Turmgenerator-Skript nun in ein Addon um und installiert es. Auch die Deinstallation sollte reibungslos klappen.
{{</todo>}}

## Ressourcen & Tutorials zum Thema

| Art/Länge | Titel | Beschreibung | Quelle |
|---|---|---|---|
|<img src="/general/icons/video.png" class="resicon">  22min | [Your Own Operator - Scripting for Artists [8]](https://youtu.be/xscQ9tcN4GI?list=PLa1F2ddGya_8acrgoQr1fTeIuQtkSd6BW) | Operators | [Blender Cloud](https://cloud.blender.org/welcome) - [Dr. Sybren A. Stüvel](https://stuvel.eu/)|
|<img src="/general/icons/video.png" class="resicon">  10min | [From Script to Add-on - Scripting for Artists [9]](https://youtu.be/nKt6CtMH0no?list=PLa1F2ddGya_8acrgoQr1fTeIuQtkSd6BW) | Operators | [Blender Cloud](https://cloud.blender.org/welcome) - [Dr. Sybren A. Stüvel](https://stuvel.eu/)|
