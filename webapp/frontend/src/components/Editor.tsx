import Monaco, { type OnMount } from "@monaco-editor/react";
import { useRef } from "react";
import type { Language } from "../lib/types";
import { Spinner } from "./ui";

/** Editor theme matched to the app palette rather than a stock Monaco theme. */
function defineTheme(monaco: Parameters<OnMount>[1]) {
  monaco.editor.defineTheme("forge", {
    base: "vs-dark",
    inherit: true,
    rules: [
      { token: "comment", foreground: "5c6b8a", fontStyle: "italic" },
      { token: "keyword", foreground: "a894ff" },
      { token: "string", foreground: "2ed3a0" },
      { token: "number", foreground: "ffbe4d" },
      { token: "type", foreground: "54b3f5" },
      { token: "function", foreground: "c3ccdd" },
      { token: "variable", foreground: "c3ccdd" },
      { token: "delimiter", foreground: "7d8ba8" },
    ],
    colors: {
      "editor.background": "#0b0f1a",
      "editor.foreground": "#c3ccdd",
      "editorLineNumber.foreground": "#2e3950",
      "editorLineNumber.activeForeground": "#7d8ba8",
      "editor.selectionBackground": "#6d4aff40",
      "editor.inactiveSelectionBackground": "#6d4aff20",
      "editor.lineHighlightBackground": "#141a2880",
      "editorCursor.foreground": "#8a6dff",
      "editorIndentGuide.background1": "#1a2131",
      "editorIndentGuide.activeBackground1": "#2e3950",
      "editorWidget.background": "#0f1420",
      "editorWidget.border": "#222b3d",
      "editorSuggestWidget.background": "#0f1420",
      "editorSuggestWidget.selectedBackground": "#222b3d",
      "editorBracketMatch.background": "#6d4aff25",
      "editorBracketMatch.border": "#6d4aff60",
      "scrollbarSlider.background": "#2e395080",
      "scrollbarSlider.hoverBackground": "#414f6b80",
    },
  });
}

export function Editor({
  value, language, onChange, onSubmit,
}: {
  value: string;
  language: Language;
  onChange: (next: string) => void;
  onSubmit: () => void;
}) {
  const submitRef = useRef(onSubmit);
  submitRef.current = onSubmit;

  const handleMount: OnMount = (editor, monaco) => {
    defineTheme(monaco);
    monaco.editor.setTheme("forge");
    // Cmd/Ctrl+Enter submits, matching every judge people already use.
    editor.addCommand(
      monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter,
      () => submitRef.current(),
    );
  };

  return (
    <Monaco
      language={language.monaco}
      value={value}
      onChange={(v) => onChange(v ?? "")}
      onMount={handleMount}
      loading={<div className="grid h-full place-items-center"><Spinner className="h-5 w-5 text-volt-400" /></div>}
      options={{
        fontSize: 13.5,
        fontFamily: "'JetBrains Mono', 'SF Mono', Menlo, monospace",
        fontLigatures: true,
        lineHeight: 1.7,
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        padding: { top: 16, bottom: 16 },
        renderLineHighlight: "line",
        smoothScrolling: true,
        cursorBlinking: "smooth",
        cursorSmoothCaretAnimation: "on",
        tabSize: 4,
        insertSpaces: true,
        bracketPairColorization: { enabled: true },
        guides: { indentation: true, bracketPairs: false },
        scrollbar: { verticalScrollbarSize: 10, horizontalScrollbarSize: 10 },
        overviewRulerLanes: 0,
        automaticLayout: true,
        stickyScroll: { enabled: false },
      }}
    />
  );
}
