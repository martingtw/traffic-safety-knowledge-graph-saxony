#!/usr/bin/env bash
# fuseki.sh
# Starte einen Apache Fuseki Container ohne Authentifizierung (ohne Admin-Passwort)
# Erfordert: podman

set -euo pipefail

# Konfigurierbare Variablen
IMAGE="${IMAGE:-docker.io/stain/jena-fuseki:latest}"
NAME="${NAME:-fuseki}"
HOST_PORT="${HOST_PORT:-3030}"

# Stelle sicher, dass podman installiert ist
if ! command -v podman &>/dev/null; then
  echo "Fehler: podman ist nicht installiert. Bitte installiere podman."
  exit 1
fi

usage() {
  cat <<EOF
Verwendung: $0 [OPTION]

Starte, sichere oder entferne einen Apache Fuseki Container per podman.

Optionen:
  -h, --help      Diese Hilfe anzeigen und beenden.

  -b              Backup: Kopiert das Verzeichnis /fuseki/backups aus dem
                  laufenden Container '$NAME' nach ./fuseki/backups
                  (auf dem Host). Der Container bleibt dabei unangetastet
                  und läuft weiter.

  -rm             Backup & Entfernen: Kopiert das Verzeichnis /fuseki/backups 
                  aus dem laufenden Container '$NAME' nach ./fuseki/backups 
                  (auf dem Host). Anschließend wird der Container gestoppt
                  und gelöscht.

Ohne Option wird ein neuer Fuseki-Container gestartet (sofern nicht vorhanden).
Es wird automatisch eine shiro.ini erzeugt, die alle Authentifizierung deaktiviert.
Der Container ist dann auf Port $HOST_PORT erreichbar.

Sicherheitshinweis:
  Die Standardeinstellung deaktiviert ALLE Zugriffsbeschränkungen. 
  Setze das Skript nur in geschützten/isolierten Netzen ein!

EOF
}

if [[ "${1:-}" == "-h" ]] || [[ "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi


if [[ "${1:-}" == "-b" ]]; then
    # Sichere /fuseki/backups aus dem Container in das aktuelle ./fuseki Verzeichnis auf dem Host
    mkdir -p ./fuseki
    podman cp "$NAME:/fuseki/backups" ./fuseki
    echo "Backupdateien befinden sich nun in ./fuseki/backups"
    exit 0
fi

if [[ "${1:-}" == "-rm" ]]; then
    echo "Backup wird synchronisiert..."
    mkdir -p ./fuseki
    podman cp "$NAME:/fuseki/backups" ./fuseki
    echo "Backup wurde nach ./fuseki/backups synchronisiert."
    echo "Stoppe und entferne den Container $NAME ..."
    podman stop "$NAME" || true
    podman rm "$NAME" || true
    echo "Fertig."
    exit 0
fi


# Existiert das Image? Falls nicht: Pull
if ! podman image exists "$IMAGE"; then
  echo "Hole Image $IMAGE ..."
  podman pull "$IMAGE"
fi

# Gibt es den Container bereits?
if podman ps -a --format '{{.Names}}' | grep -qw "$NAME"; then
  STATUS=$(podman inspect "$NAME" --format '{{.State.Status}}')
  if [ "$STATUS" = "running" ]; then
    echo "Container $NAME läuft bereits. Bitte stoppe ihn manuell, bevor du das Skript erneut ausführst."
    ./fuseki.sh -b
    exit 0
  else
    echo "Container $NAME ist vorhanden, aber gestoppt. Starte ihn..."
    podman start "$NAME"
    echo "Container $NAME wurde gestartet."
    echo "Keine Änderungen vorgenommen. Wenn du die Konfiguration erneuern willst, lösche oder stoppe den Container vorher."
    ./fuseki.sh -b
    exit 0
  fi
fi

# Container starten (wenn noch nicht vorhanden)
podman run -d --name "$NAME" \
  -p "127.0.0.1:$HOST_PORT:3030" \
  "$IMAGE"

  
# Kurze Pause für initialen Start
sleep 5

podman exec -i -u root "$NAME" sh -c 'cat > /fuseki/shiro.ini' <<'EOF'
[main]
[users]
[roles]
[urls]
/$/** = anon
/** = anon
EOF


# Container neu starten, damit Fuseki die neue shiro.ini einliest
podman restart "$NAME"

echo "Fuseki läuft jetzt ohne Authentifizierung auf http://localhost:$HOST_PORT"

