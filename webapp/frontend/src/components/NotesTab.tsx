import { useEffect, useRef, useState } from "react";
import { api } from "../lib/api";
import { timeAgo } from "../lib/format";
import { Icon, Spinner } from "./ui";

/**
 * Per-problem scratch notes, saved server-side.
 *
 * The pattern you spotted matters more than the solution you typed, and it is
 * the thing you want back when the same shape shows up two weeks later.
 */
export function NotesTab({ problemId, onSavedChange }: {
  problemId: string; onSavedChange: (hasNote: boolean) => void;
}) {
  const [body, setBody] = useState<string | null>(null);
  const [savedAt, setSavedAt] = useState<number | null>(null);
  const [saving, setSaving] = useState(false);
  const timer = useRef<number | undefined>(undefined);
  const dirty = useRef(false);

  useEffect(() => {
    setBody(null);
    dirty.current = false;
    void (async () => {
      try {
        const note = await api.note(problemId);
        setBody(note.body);
        setSavedAt(note.updatedAt);
      } catch { setBody(""); }
    })();
  }, [problemId]);

  // Debounced autosave. A note is not worth a Save button.
  useEffect(() => {
    if (body === null || !dirty.current) return;
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(async () => {
      setSaving(true);
      try {
        const note = await api.saveNote(problemId, body);
        setSavedAt(note.updatedAt);
        onSavedChange(Boolean(note.body));
      } finally { setSaving(false); }
    }, 700);
    return () => window.clearTimeout(timer.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [body, problemId]);

  if (body === null)
    return <div className="grid h-full place-items-center"><Spinner className="h-5 w-5 text-volt-400" /></div>;

  return (
    <div className="flex h-full flex-col">
      <div className="flex h-9 shrink-0 items-center gap-2 border-b border-white/[.06] px-4">
        <Icon name="note" className="h-3.5 w-3.5 text-mist-400" />
        <span className="text-[11px] font-semibold text-mist-300">Your notes</span>
        <span className="ml-auto flex items-center gap-1.5 text-[10.5px] text-mist-400">
          {saving ? <><Spinner className="h-3 w-3" /> saving…</>
           : savedAt ? `saved ${timeAgo(savedAt)}` : "not saved yet"}
        </span>
      </div>
      <textarea
        value={body}
        onChange={(e) => { dirty.current = true; setBody(e.target.value); }}
        placeholder={"What was the trick here?\n\n- pattern:\n- complexity:\n- what I got wrong first:"}
        spellCheck={false}
        className="scroll-thin min-h-0 flex-1 resize-none bg-transparent px-5 py-4 font-mono
                   text-[12.5px] leading-relaxed text-mist-200 placeholder:text-ink-500
                   focus:outline-none"
      />
    </div>
  );
}
