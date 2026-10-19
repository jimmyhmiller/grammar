"""Gate for the grammar agent: rejects reports that cannot be applied."""
import json
import sys

run = json.load(sys.stdin)
problems = []
for report in run["reports"]:
    args = report["arguments"]
    n = report["number"]
    if args["original"] not in args["context"]:
        problems.append(f"#{n}: original {args['original']!r} is not inside context {args['context']!r}.")
    elif len(args["context"]) <= len(args["original"]):
        problems.append(f"#{n}: context {args['context']!r} must include words around original, not just original.")
    if args["suggestion"] == args["original"]:
        problems.append(f"#{n}: suggestion is identical to original; retract it or give the correction.")

if problems:
    print("Fix these reports (retract and report again):")
    print("\n".join(problems))
    sys.exit(1)
