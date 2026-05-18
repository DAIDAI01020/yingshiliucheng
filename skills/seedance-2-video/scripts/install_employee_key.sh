#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_SCRIPT="$SCRIPT_DIR/seedance_task.py"

KEY_FILE=""
FORCE=0
FROM_STDIN=0
RUN_DOCTOR=1
DOCTOR_ARGS=()

usage() {
  cat <<'EOF'
Usage: install_employee_key.sh [options]

Installs an Ark API key into the employee's local private config for
$seedance-2-video. The key is not written into the shareable skill folder.

Options:
  --key-file PATH       Override local key file path
  --force               Overwrite an existing key file
  --from-stdin          Read the key from stdin instead of hidden prompt
  --no-doctor           Skip post-install doctor check
  --image-url URL       Pass an image URL to doctor for reachability check
  -h, --help            Show this help

Examples:
  ./install_employee_key.sh
  ./install_employee_key.sh --force
  pass show ark/key | ./install_employee_key.sh --from-stdin --force
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --key-file)
      KEY_FILE="${2:-}"
      if [[ -z "$KEY_FILE" ]]; then
        echo "ERROR: --key-file requires a path" >&2
        exit 2
      fi
      shift 2
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --from-stdin)
      FROM_STDIN=1
      shift
      ;;
    --no-doctor)
      RUN_DOCTOR=0
      shift
      ;;
    --image-url)
      if [[ -z "${2:-}" ]]; then
        echo "ERROR: --image-url requires a URL" >&2
        exit 2
      fi
      DOCTOR_ARGS+=(--image-url "$2")
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ ! -f "$TASK_SCRIPT" ]]; then
  echo "ERROR: seedance_task.py not found next to installer: $TASK_SCRIPT" >&2
  exit 1
fi

setup_args=(setup-key)
doctor_args=(doctor)
if [[ -n "$KEY_FILE" ]]; then
  setup_args+=(--key-file "$KEY_FILE")
  doctor_args+=(--key-file "$KEY_FILE")
fi
if [[ "$FORCE" -eq 1 ]]; then
  setup_args+=(--force)
fi

if [[ "$FROM_STDIN" -eq 1 ]]; then
  setup_args+=(--from-stdin)
  python3 "$TASK_SCRIPT" "${setup_args[@]}"
else
  python3 "$TASK_SCRIPT" "${setup_args[@]}"
fi

if [[ "$RUN_DOCTOR" -eq 1 ]]; then
  if [[ ${#DOCTOR_ARGS[@]} -gt 0 ]]; then
    python3 "$TASK_SCRIPT" "${doctor_args[@]}" "${DOCTOR_ARGS[@]}"
  else
    python3 "$TASK_SCRIPT" "${doctor_args[@]}"
  fi
fi

echo "Seedance employee key install complete."
