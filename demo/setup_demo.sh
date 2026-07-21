#!/usr/bin/env bash
# Resets the demo project to a pristine, un-initialized state.
# Safe to re-run as many times as you want while rehearsing.
set -e

DEMO_DIR="$HOME/mini-git-demo-project"

rm -rf "$DEMO_DIR"
mkdir -p "$DEMO_DIR/src"
cd "$DEMO_DIR"

cat > index.html <<'EOF'
<!DOCTYPE html>
<html>
<head><title>My Blog</title></head>
<body>
  <h1>Welcome to my blog</h1>
</body>
</html>
EOF

cat > style.css <<'EOF'
body {
    font-family: sans-serif;
    margin: 0;
}
EOF

cat > src/app.py <<'EOF'
def main():
    print("Starting blog server...")


if __name__ == "__main__":
    main()
EOF

echo "Demo project reset at: $DEMO_DIR"
echo "cd into it and follow demo/DEMO_SCRIPT.md"
