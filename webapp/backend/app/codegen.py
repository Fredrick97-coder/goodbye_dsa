"""
Render starter code for any language from a neutral signature.

One renderer, driven by the language table. This is what makes 342 problems
appear in a new language the moment its row exists -- nobody writes stubs by
hand, and a stub can never contradict what the tests will actually pass in,
because both come from the same inferred signature.

Python is the exception and keeps its hand-written stub: the exercise files are
the source of truth there, complete with the author's own hints and parameter
names, and a generated approximation would be a downgrade. Generation is for
the languages that have no authored file.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from .languages import Language
from .settings import settings

if str(settings.python_root) not in sys.path:
    sys.path.insert(0, str(settings.python_root))

from _harness import signature as sig          # noqa: E402


def render_type(t: str, lang: Language) -> str:
    """
    Neutral type string -> this language's spelling.

    Parses the compact form `list[list[int]]` rather than taking the dataclass,
    so the plan can travel as JSON without the type model on both sides.
    """
    t = (t or "any").strip()

    if t.startswith("list[") and t.endswith("]"):
        return lang.list_form.format(render_type(t[5:-1], lang))
    if t.startswith("tuple[") and t.endswith("]"):
        return lang.list_form.format(render_type(t[6:-1], lang))
    if t.startswith("dict[") and t.endswith("]"):
        inner = t[5:-1]
        depth = 0
        for i, ch in enumerate(inner):
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
            elif ch == "," and depth == 0:
                return lang.dict_form.format(render_type(inner[:i], lang),
                                             render_type(inner[i + 1:], lang))
        return lang.dict_form.format(render_type(inner, lang),
                                     render_type("any", lang))

    return lang.types.get(t, lang.types.get("any", "unknown"))


def placeholder_for(t: str, lang: Language) -> str:
    """What an untouched stub returns, so the file compiles as handed over."""
    t = (t or "any").strip()
    if t.startswith(("list[", "tuple[")):
        return lang.placeholders.get("list", "[]")
    if t.startswith("dict["):
        return lang.placeholders.get("dict", "{}")
    return lang.placeholders.get(t, lang.placeholders.get("any", "null"))


def _params(signature: Dict[str, Any], lang: Language) -> str:
    out: List[str] = []
    for param in signature["params"]:
        rendered = render_type(param["type"], lang)
        text = lang.param_form.format(name=param["name"], type=rendered)
        # JavaScript has no annotations, so `param_form` is just the name and
        # the separator would leave a dangling colon.
        out.append(text.rstrip(": ").strip() if not rendered else text)
    return ", ".join(out)


def _return_clause(signature: Dict[str, Any], lang: Language) -> str:
    """Positioned and punctuated by the language's own `return_form`."""
    rendered = render_type(signature["returns"], lang)
    if not rendered or not lang.return_form:
        return ""
    return lang.return_form.format(rendered)


def stub_for(signature: Dict[str, Any], lang: Language, note: str = "") -> str:
    """One function stub, with a TODO and a compiling placeholder return."""
    body_lines = [f"{lang.comment} TODO: your solution here"]
    if note:
        body_lines += [f"{lang.comment} {line}" for line in _wrap(note, 68)]

    returns = signature["returns"]
    if signature.get("inplace"):
        body_lines.append(f"{lang.comment} mutate the first argument in place; "
                          f"return nothing")
    placeholder = placeholder_for(returns, lang)
    if placeholder and not signature.get("inplace") and returns != "void":
        body_lines.append(f"return {placeholder};" if lang.comment == "//"
                          else f"return {placeholder}")

    indent = "  " if lang.comment == "//" else "    "
    body = "\n".join(indent + line for line in body_lines)

    return lang.function_form.format(
        name=signature["name"], params=_params(signature, lang),
        ret=_return_clause(signature, lang), body=body)


def _wrap(text: str, width: int) -> List[str]:
    words, lines, current = text.split(), [], ""
    for word in words:
        if len(current) + len(word) + 1 > width:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        lines.append(current)
    return lines


HEADERS = {
    "typescript": (
        "// Export a function for each name below. The exact name from the\n"
        "// problem statement works, and so does its camelCase form.\n"
        "//\n"
        "// Node runs this by STRIPPING types, not checking them -- a type error\n"
        "// will not fail the build, so treat the annotations as documentation.\n"
    ),
    "javascript": (
        "// Export a function for each name below. The exact name from the\n"
        "// problem statement works, and so does its camelCase form.\n"
    ),
}


def starter(signatures: List[Dict[str, Any]], lang: Language,
            notes: Optional[Dict[str, str]] = None) -> str:
    """The whole file: header plus one stub per target."""
    notes = notes or {}
    blocks = [stub_for(s, lang, notes.get(s["name"], "")) for s in signatures]
    header = HEADERS.get(lang.id, "")
    return (header + "\n" + "\n\n".join(blocks) + "\n") if header \
        else "\n\n".join(blocks) + "\n"


def signatures_for_plan(plan: Dict[str, Any], python_source: str = "",
                        ) -> List[Dict[str, Any]]:
    """Infer a signature per target from the plan's own test data."""
    out: List[Dict[str, Any]] = []
    for target in plan.get("targets", []):
        built = sig.build(
            name=target["name"],
            cases=target["cases"],
            python_source=python_source,
            inplace=bool(target.get("inplace")),
        )
        out.append(built.as_dict())
    return out
