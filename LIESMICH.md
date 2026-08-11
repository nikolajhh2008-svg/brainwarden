# Brainwarden auf Deutsch – Kurzanleitung

Brainwarden richtet dir in ~20 Minuten ein „Second Brain" in Obsidian
ein – Claude Code baut und pflegt es für dich. Alles Weitere passiert
im Gespräch mit Claude, **auf Deutsch** (die technischen Anleitungen im
Kit sind englisch, die liest nur Claude).

## Du brauchst
- [Obsidian](https://obsidian.md) (kostenlos, installiert)
- Ein Claude-Abo mit [Claude Code](https://claude.com/claude-code)
- ~20 Minuten Ruhe

## Los geht's
Terminal öffnen (cmd+Leertaste → „Terminal"), `claude` eintippen und
diesen einen Satz sagen oder einfügen:

> Richte mir das Second Brain aus diesem GitHub-Repo ein:
> https://github.com/nikolajhh2008-svg/brainwarden – klone es und
> folge SETUP-FOR-CLAUDE.md Schritt für Schritt. Sprich Deutsch mit mir.

## Die erste Frage: für wen ist das Brain?
Claude fragt das ganz am Anfang, noch vor allem anderen. Deine Antwort
entscheidet, welche Ordner entstehen und womit das Brain startet.

| Deine Antwort | Was du bekommst |
|---|---|
| **für mich** | dein Leben: Projekte, Bereiche, Wissen, Entscheidungen, Personen |
| **für die Arbeit** | dasselbe ohne den privaten Teil, dazu `50-processes/` für wiederkehrende Abläufe |
| **beides, getrennt** | zwei Vaults, zwei Startbefehle (`claude` und `workbrain`), nichts vermischt sich |
| **für eine Firma** | geteiltes Firmenwissen: Abläufe, Rollen, Einarbeitung, Partner. Keine Projekte und Bereiche, und Rollen statt Dossiers über Kolleginnen und Kollegen |

Danach kommen vier kurze Fragen (deine Situation, womit das Brain
zuerst helfen soll, die Sprache deiner Notizen, dein nächster wichtiger
Termin). Daraus baut Claude sofort die ersten echten Notizen. Im
Firmenmodus sind es ein paar Fragen mehr, und der erste Gewinn ist ein
aufgeschriebener Ablauf statt eines Projekts. Das ausführliche
Interview kommt erst danach, und nur wenn du willst.

## Die fünf Worte für den Alltag
- **„capture: …"** – Gedanken sofort festhalten (landet in der Inbox)
- **„ingest"** – ein PDF/Artikel/Transkript ins Brain einarbeiten
- **„was weiß mein Brain über …?"** – Antworten mit deinen Notizen als Beleg
- **„brain review"** – der Wochen-Check (Inbox leeren, aufräumen)
- **„research mein Brain"** – Lücken mit belegten Fakten füllen

## Zwei Dinge, die dir beim Lesen auffallen
- In jedem Ordner liegt eine `index.md`: was dort hingehört, was nicht,
  und die zwei bis drei Notizen, mit denen man anfängt. Die ist vor
  allem für die KI da, damit sie sich in deinem Vault zurechtfindet.
  Du kannst sie beim Lesen ignorieren.
- Notizen tragen zwei getrennte Angaben: `maturity:` sagt, wie
  ausgearbeitet eine Notiz ist (`seed`, `growing`, `evergreen`),
  `status:` sagt, ob sie noch gilt (`draft`, `stable`, `deprecated`).
  Dazu `verified:` (ein Mensch hat es bestätigt) und `generated:`
  (eine KI hat es geschrieben). `verified:` setzt Claude nie selbst.

## Suche
Die Suche im Vault versteht zusammengesetzte Wörter: „Vertrag" findet
auch „Rahmenvertrag", „Kosten" auch „Mehrkostenforderungen". Umlaute
und ß spielen keine Rolle.

Etwas kaputt? Sag es einfach Claude – das Brain hat eine eingebaute
Sicherung (Git), fast alles lässt sich zurückholen.
