"""
A language-neutral description of a problem's signature.

This is the piece that makes "add a language" a small job. LeetCode does not
hand-write starter code for twenty languages per problem; it describes the
signature once in a neutral type system and renders it per language. Same idea
here.

Types are inferred from two sources, in this order of trust:

1. **The test data.** Every portable problem already has forty-odd concrete
   `(args, expected)` pairs, so the shapes are observable facts rather than
   guesses. A parameter that is always a list of ints *is* `list[int]`.
2. **The Python annotation**, when the exercise file has one, to settle what the
   data cannot: an empty list in every case says `list[?]`, and the annotation
   says `List[int]`.

Inference beats a hand-written table because it cannot drift: change a
generator, and the rendered signature follows. Where the two disagree the data
wins -- the data is what the solution will actually be handed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence

# ------------------------------------------------------------ the type model

#: Neutral type names. Deliberately small -- these are DSA problems, so the
#: universe is scalars, sequences of scalars, matrices, and the occasional map.
#: A language is added by mapping these names, not by handling arbitrary types.
SCALARS = ("int", "float", "bool", "string", "any")


@dataclass(frozen=True)
class Type:
    """`kind` is a scalar name, "list", "dict", "tuple" or "void"."""
    kind: str
    of: Optional["Type"] = None                 # element type for list/tuple
    value: Optional["Type"] = None              # value type for dict

    def __str__(self) -> str:
        if self.kind == "list":
            return f"list[{self.of or ANY}]"
        if self.kind == "tuple":
            return f"tuple[{self.of or ANY}]"
        if self.kind == "dict":
            return f"dict[{self.of or ANY},{self.value or ANY}]"
        return self.kind


ANY = Type("any")
VOID = Type("void")
INT = Type("int")
FLOAT = Type("float")
BOOL = Type("bool")
STRING = Type("string")


def list_of(inner: Type) -> Type:
    return Type("list", of=inner)


@dataclass
class Param:
    name: str
    type: Type


@dataclass
class Signature:
    name: str
    params: List[Param] = field(default_factory=list)
    returns: Type = ANY
    #: True when the problem mutates its first argument and returns nothing.
    inplace: bool = False
    doc: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "params": [{"name": p.name, "type": str(p.type)} for p in self.params],
            "returns": str(self.returns),
            "inplace": self.inplace,
            "doc": self.doc,
        }


# --------------------------------------------------------- inference: values

def _unify(a: Optional[Type], b: Optional[Type]) -> Type:
    """
    The most specific type that describes both.

    `int` widening to `float` matters: a generator that mostly yields whole
    numbers but sometimes a fraction must render as a float parameter, or the
    signature lies about what will arrive.
    """
    if a is None:
        return b or ANY
    if b is None:
        return a
    if a == b:
        return a
    if {a.kind, b.kind} == {"int", "float"}:
        return FLOAT
    if a.kind == "any":
        return b
    if b.kind == "any":
        return a
    if a.kind == b.kind in ("list", "tuple"):
        return Type(a.kind, of=_unify(a.of, b.of))
    if a.kind == b.kind == "dict":
        return Type("dict", of=_unify(a.of, b.of), value=_unify(a.value, b.value))
    # bool and int are distinct on purpose: a problem returning True/False must
    # not render as returning a number.
    return ANY


def type_of_value(value: Any) -> Type:
    if value is None:
        return ANY
    if isinstance(value, bool):
        return BOOL
    if isinstance(value, int):
        return INT
    if isinstance(value, float):
        return FLOAT
    if isinstance(value, str):
        return STRING
    if isinstance(value, (list, tuple)):
        kind = "list"          # JSON has one sequence type; see fixtures.py
        inner: Optional[Type] = None
        for item in value:
            inner = _unify(inner, type_of_value(item))
        return Type(kind, of=inner or ANY)
    if isinstance(value, dict):
        key: Optional[Type] = None
        val: Optional[Type] = None
        for k, v in value.items():
            key = _unify(key, type_of_value(k))
            val = _unify(val, type_of_value(v))
        return Type("dict", of=key or ANY, value=val or ANY)
    return ANY


def infer_from_cases(cases: Sequence[Dict[str, Any]]) -> tuple:
    """(param_types, return_type) observed across every case."""
    widths = max((len(c["args"]) for c in cases), default=0)
    params: List[Optional[Type]] = [None] * widths
    returns: Optional[Type] = None
    for case in cases:
        for i, arg in enumerate(case["args"]):
            params[i] = _unify(params[i], type_of_value(arg))
        returns = _unify(returns, type_of_value(case.get("expected")))
    return [p or ANY for p in params], (returns or ANY)


# ---------------------------------------------------- inference: annotations

_PY_SCALARS = {
    "int": INT, "float": FLOAT, "bool": BOOL, "str": STRING,
    "Any": ANY, "None": VOID, "object": ANY,
}


def type_from_annotation(text: str) -> Optional[Type]:
    """
    Parse a Python annotation into the neutral model. None when unrecognised.

    Only the shapes that actually appear in these exercise files are handled --
    a general PEP 484 parser would be a lot of code for no extra coverage.
    """
    if not text:
        return None
    t = text.strip().strip("'\"")
    t = re.sub(r"^typing\.", "", t)

    if t in _PY_SCALARS:
        return _PY_SCALARS[t]

    opt = re.fullmatch(r"Optional\[(.+)\]", t)
    if opt:
        return type_from_annotation(opt.group(1))

    for name in ("List", "list", "Sequence", "Iterable", "Tuple", "tuple", "Set", "set"):
        m = re.fullmatch(rf"{name}\[(.+)\]", t)
        if m:
            inner = m.group(1)
            # Tuple[int, int] and the like: unify the members.
            if "," in inner and not inner.startswith(("List", "list", "Dict", "dict")):
                parts = [p.strip() for p in inner.split(",") if p.strip() != "..."]
                unified: Optional[Type] = None
                for p in parts:
                    unified = _unify(unified, type_from_annotation(p) or ANY)
                return list_of(unified or ANY)
            return list_of(type_from_annotation(inner) or ANY)
        if t == name:
            return list_of(ANY)

    m = re.fullmatch(r"(?:Dict|dict)\[(.+?),\s*(.+)\]", t)
    if m:
        return Type("dict", of=type_from_annotation(m.group(1)) or ANY,
                    value=type_from_annotation(m.group(2)) or ANY)
    if t in ("Dict", "dict"):
        return Type("dict", of=ANY, value=ANY)

    return None


_DEF_RE = re.compile(
    r"^(?:async\s+)?def\s+(?P<name>\w+)\s*\((?P<params>[^)]*)\)"
    r"(?:\s*->\s*(?P<ret>[^:]+))?\s*:", re.M | re.S)


def parse_python_def(source: str, name: str) -> Optional[Dict[str, Any]]:
    """Pull parameter names and any annotations out of the exercise file."""
    for match in _DEF_RE.finditer(source):
        if match.group("name") != name:
            continue
        raw_params = match.group("params") or ""
        params: List[Dict[str, Optional[str]]] = []
        depth = 0
        current = ""
        # Split on top-level commas so `Dict[str, int]` stays one parameter.
        for ch in raw_params + ",":
            if ch in "[({":
                depth += 1
            elif ch in "])}":
                depth -= 1
            if ch == "," and depth == 0:
                if current.strip():
                    params.append(_split_param(current))
                current = ""
            else:
                current += ch
        return {"params": [p for p in params if p["name"] not in ("self", "cls")],
                "returns": (match.group("ret") or "").strip() or None}
    return None


def _split_param(text: str) -> Dict[str, Optional[str]]:
    body = text.split("=")[0].strip()
    if ":" in body:
        pname, _, annot = body.partition(":")
        return {"name": pname.strip(), "annotation": annot.strip()}
    return {"name": body.strip(), "annotation": None}


# ------------------------------------------------------------------- combine

def build(name: str, cases: Sequence[Dict[str, Any]],
          python_source: str = "", inplace: bool = False,
          doc: str = "") -> Signature:
    """
    A signature from the test data, refined by the Python annotations.

    The data decides the shape; annotations only fill gaps the data leaves --
    typically the element type of a list that happens to be empty in every case.
    """
    data_params, data_return = infer_from_cases(cases)
    parsed = parse_python_def(python_source, name) if python_source else None

    params: List[Param] = []
    for i, observed in enumerate(data_params):
        pname = f"arg{i + 1}"
        annotated: Optional[Type] = None
        if parsed and i < len(parsed["params"]):
            pname = parsed["params"][i]["name"] or pname
            annotated = type_from_annotation(parsed["params"][i]["annotation"] or "")
        params.append(Param(pname, _refine(observed, annotated)))

    returns = data_return
    if parsed and parsed["returns"]:
        returns = _refine(returns, type_from_annotation(parsed["returns"]))
    if inplace:
        returns = VOID

    return Signature(name=name, params=params, returns=returns,
                     inplace=inplace, doc=doc)


def _refine(observed: Type, annotated: Optional[Type]) -> Type:
    """
    Observed data wins; the annotation only sharpens an unknown.

    An annotation saying `List[int]` cannot override data showing strings -- the
    data is what the solution will be handed, and a signature that contradicts
    it would send the learner down the wrong path.
    """
    if annotated is None:
        return observed
    if observed.kind == "any":
        return annotated
    if observed.kind in ("list", "tuple") and annotated.kind in ("list", "tuple"):
        if (observed.of or ANY).kind == "any":
            return Type(observed.kind, of=annotated.of or ANY)
    return observed
