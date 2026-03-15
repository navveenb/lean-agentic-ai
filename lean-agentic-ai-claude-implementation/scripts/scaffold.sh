#!/usr/bin/env bash
# scaffold.sh — Create new skills, agents, or commands from templates
# Usage:
#   ./scripts/scaffold.sh skill  my-skill-name
#   ./scripts/scaffold.sh agent  my-agent-name
#   ./scripts/scaffold.sh command my-command-name

set -e

TYPE="$1"
NAME="$2"

if [ -z "$TYPE" ] || [ -z "$NAME" ]; then
    echo "Usage: ./scripts/scaffold.sh <type> <name>"
    echo ""
    echo "Types:"
    echo "  skill    → Creates .claude/skills/<name>/SKILL.md"
    echo "  agent    → Creates .claude/agents/<name>.md"
    echo "  command  → Creates .claude/commands/<name>.md"
    echo ""
    echo "Examples:"
    echo "  ./scripts/scaffold.sh skill  prompt-compressor"
    echo "  ./scripts/scaffold.sh agent  qa-reviewer"
    echo "  ./scripts/scaffold.sh command run-audit"
    exit 1
fi

case "$TYPE" in
    skill)
        TARGET=".claude/skills/$NAME/SKILL.md"
        SOURCE=".claude/skills/_template/SKILL.md"
        if [ -f "$TARGET" ]; then
            echo "Error: $TARGET already exists"
            exit 1
        fi
        mkdir -p ".claude/skills/$NAME"
        cp "$SOURCE" "$TARGET"
        # Replace placeholder name
        sed -i.bak "s/your-skill-name/$NAME/g" "$TARGET" && rm -f "$TARGET.bak"
        echo "Created: $TARGET"
        echo "Next: Edit $TARGET and fill in your content"
        ;;
    agent)
        TARGET=".claude/agents/$NAME.md"
        SOURCE="contrib/agents/TEMPLATE.md"
        if [ -f "$TARGET" ]; then
            echo "Error: $TARGET already exists"
            exit 1
        fi
        cp "$SOURCE" "$TARGET"
        sed -i.bak "s/your-agent-name/$NAME/g" "$TARGET" && rm -f "$TARGET.bak"
        echo "Created: $TARGET"
        echo "Next: Edit $TARGET and fill in your content"
        ;;
    command)
        TARGET=".claude/commands/$NAME.md"
        SOURCE="contrib/commands/TEMPLATE.md"
        if [ -f "$TARGET" ]; then
            echo "Error: $TARGET already exists"
            exit 1
        fi
        cp "$SOURCE" "$TARGET"
        echo "Created: $TARGET"
        echo "Next: Edit $TARGET and fill in your content"
        ;;
    *)
        echo "Unknown type: $TYPE"
        echo "Use: skill, agent, or command"
        exit 1
        ;;
esac

echo ""
echo "Test it:"
echo "  cd $(pwd)"
echo "  claude"
echo "  > what new skills/agents do you see?"
