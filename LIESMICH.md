# Brainwarden auf Deutsch – Kurzanleitung

Brainwarden richtet dir ein Gedächtnis auf deinem Rechner ein: einen Ordner
voller Notizen, den Claude für dich baut und pflegt – Projekte, Termine,
Personen, Entscheidungen. Alles Weitere passiert im Gespräch, **auf
Deutsch** (die technischen Anleitungen im Kit sind englisch, die liest nur
Claude).

## Du brauchst

- [Obsidian](https://obsidian.md) – kostenlos, zeigt dir deine Notizen
- Ein bezahltes Claude-Abo mit [Claude Code](https://claude.com/claude-code)
- Etwa eine halbe Stunde. Davon gehen 10–20 Minuten für die Installationen
  drauf, der Rest ist Gespräch.

## Los geht's – ohne Terminal

**Claude Code gibt es als normales Programm für Mac und Windows.** Kein
schwarzer Bildschirm, kein Terminal: Du installierst es wie jede andere App,
machst es auf und schreibst hinein. Das ist der empfohlene Weg.

Dort diesen einen Satz einfügen:

> Richte mir das Second Brain aus diesem GitHub-Repo ein:
> https://github.com/nikolajhh2008-svg/brainwarden – klone es und
> folge SETUP-FOR-CLAUDE.md Schritt für Schritt. Sprich Deutsch mit mir.

**Falls du das Terminal magst:** genauso gut. Terminal öffnen
(cmd+Leertaste → „Terminal"), `claude` eintippen, denselben Satz.

## Was während der Einrichtung passiert – damit du nicht erschrickst

Claude arbeitet nicht heimlich. Für **jeden** Schritt, der etwas auf deinem
Rechner anlegt, ändert oder löscht, fragt es dich vorher. Das sind ungefähr
zwanzig Nachfragen – das ist normal und kein Zeichen, dass etwas schiefgeht.

Zwei Stellen lohnt es sich zu kennen:

- **`assemble.py`** legt deinen Ordner an: Es kopiert die Vorlage, nimmt
  nur die Teile, die zu deiner Antwort auf die erste Frage passen, und
  lässt Gerüstmaterial aus dem Bausatz weg. Es überschreibt **nie** etwas,
  was schon da ist – zeigt dir am Ende sogar, was es stehen gelassen hat.
- **Ein kurzer Regelblock in `~/.claude/CLAUDE.md`** ist das, woran jede
  spätere Claude-Sitzung dein Brain erkennt: die Zeile mit dem Pfad zu
  deinem Ordner, dazu ein paar Zeilen, wann Claude hineinschauen und wann
  es etwas festhalten soll. Claude fragt vorher.

Du kannst bei den Nachfragen „für diese Sitzung erlauben" wählen, dann ist
Ruhe. Und wenn dir etwas nicht geheuer ist: frag einfach nach, bevor du
zustimmst. Claude erklärt jeden Befehl.

Vielleicht sagt Claude einmal, du sollst es kurz neu starten. Auch das ist
normal – neue Bausteine werden dabei geladen, es ist nichts kaputt.

## Die erste Frage: für wen ist das Brain?

Claude fragt das ganz am Anfang, noch vor allem anderen. Deine Antwort
entscheidet, welche Ordner entstehen und womit das Brain startet.

| Deine Antwort | Was du bekommst |
|---|---|
| **für mich** | dein Leben: Projekte, Bereiche, Wissen, Entscheidungen, Personen |
| **für die Arbeit** | dasselbe ohne den privaten Teil, dazu eigene Abläufe, ein Protokoll dessen, was du geschafft hast, und ein Feld auf jeder Notiz: gehört das dir oder dem Arbeitgeber |
| **beides, getrennt** | zwei Ordner, zwei Startbefehle (`claude` und `workbrain`), nichts vermischt sich |
| **für eine Firma** | geteiltes Firmenwissen: Abläufe, Rollen, Einarbeitung, Partner. Keine Projekte und Bereiche, und Rollen statt Dossiers über Kolleginnen und Kollegen |

Danach kommen vier kurze Fragen (deine Situation, womit das Brain zuerst
helfen soll, die Sprache deiner Notizen, dein nächster wichtiger Termin).
Daraus baut Claude sofort die ersten echten Notizen. Im Firmenmodus sind es
ein paar Fragen mehr, und der erste Gewinn ist ein aufgeschriebener Ablauf
statt eines Projekts. Das ausführliche Interview kommt erst danach, und nur
wenn du willst.

**Warum das eine Feld beim Arbeits-Brain:** Wer kündigt, muss in Österreich
und Deutschland herausgeben, was er aus dem Arbeitsverhältnis hat – Gerichte
zählen selbst geschriebene Notizen über Kundengespräche und Projektarbeit
dazu, Kopien inklusive. Nur echte private Aufzeichnungen sind ausgenommen.
Wer beim Schreiben eine Zeile setzt, ist in Minuten fertig. Wer es am letzten
Tag sortieren will, kann es nicht mehr. Dasselbe Feld entscheidet, was die KI
an ein externes Modell schicken darf.

## Die fünf Worte für den Alltag

- **merken** – „capture: …" hält einen Gedanken sofort fest (landet im
  Eingang, sortiert wird später)
- **einarbeiten** – „ingest" holt ein PDF, einen Artikel oder ein
  Transkript ins Brain
- **nachfragen** – „was weiß mein Brain über …?" antwortet nur aus deinen
  eigenen Notizen, mit Beleg
- **aufräumen** – „brain review" ist der Wochen-Check: Eingang leeren,
  Termine nachziehen, Zustand prüfen
- **recherchieren** – „research mein Brain" füllt offene Fragen mit
  belegten Fakten

Diese fünf englischen Wörter sind Befehle und bleiben englisch – alles
andere sprichst du auf Deutsch.

## Zwei Dinge, die dir beim Lesen auffallen

- **In jedem Ordner liegt eine `index.md`.** Darin steht, was dort
  hingehört, was nicht, und die zwei bis drei Notizen, mit denen man
  anfängt. Die ist vor allem für die KI da, damit sie sich in deinem Ordner
  zurechtfindet. Du kannst sie beim Lesen überspringen.
- **Oben in jeder Notiz stehen ein paar Zeilen Verwaltungskram** zwischen
  zwei Strichen (`---`) – Datum, Art, Schlagwörter. Der eigentliche Text
  fängt darunter an. In Obsidian siehst du diesen Block gar nicht erst.
  Zwei Angaben davon lohnen sich zu kennen: `maturity:` sagt, wie
  ausgearbeitet eine Notiz ist, `status:` sagt, ob sie noch gilt. Und
  `verified:` heißt „ein Mensch hat das bestätigt" – das setzt Claude nie
  selbst.

## Suche

Die Suche versteht zusammengesetzte Wörter: „Vertrag" findet auch
„Rahmenvertrag", „Kosten" auch „Mehrkostenforderungen". Umlaute und ß
spielen keine Rolle.

## Wenn du länger weg warst

Nichts kaputt. Öffne Claude in deinem Brain-Ordner und schreib einfach
**„brain review"** – der Wochen-Check arbeitet auch drei Wochen Rückstand
in einem Rutsch ab und macht dir deswegen keine Vorwürfe. Ausgefallene
Wochen sind eingeplant, nicht ein Versagen.

Weißt du nicht mehr, wie das Ding hieß? Frag Claude: *„was ist mein Brain,
und wie benutze ich es?"* – die Antwort steht in deinem Ordner.

## Wenn etwas klemmt

Sag es einfach Claude – dein Brain hat eine eingebaute Sicherung, fast alles
lässt sich zurückholen.

Ausführlicher:
- [TUTORIAL.md](TUTORIAL.md) – der Weg von null, mit Kontrollpunkt nach
  jeder Etappe (englisch, aber Claude übersetzt dir jede Stelle)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) – was tun, wenn etwas hakt;
  darin auch, wie du unterwegs vom Handy aus etwas festhältst
- [COWORK.md](COWORK.md) – ein fertiges Brain in Claude Cowork lesen, ganz
  ohne Terminal. Der richtige Weg, wenn du ein Firmen-Brain bekommen hast
  und nur nachschlagen willst
- [PHILOSOPHY.md](PHILOSOPHY.md) – warum es so gebaut ist, und warum nicht
  einfach Word-Dateien auf dem Server
