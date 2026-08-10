export type Difficulty = "Easy" | "Medium" | "Hard" | "Challenge";

export type Verdict =
  | "accepted" | "failed" | "stub" | "error"
  | "missing" | "untested" | "ran";

export interface Language {
  id: string;
  label: string;
  monaco: string;
  ext: string;
  available: boolean;
}

export interface Topic {
  topic: number;
  name: string;
  slug: string;
  problemCount: number;
  testedCount: number;
  level: string;
}

export interface Stats {
  problems: number;
  topics: number;
  tested: number;
  specCount: number;
  byDifficulty: Record<string, number>;
}

export interface Meta {
  languages: Language[];
  topics: Topic[];
  stats: Stats;
  difficulties: Difficulty[];
}

export interface ProblemSummary {
  id: string;
  topic: number;
  topicName: string;
  num: number;
  title: string;
  rawTitle: string;
  difficulty: Difficulty;
  targets: string[];
  tested: boolean;
  testCount: number;
  drillable: boolean;
}

export interface ProblemDetail extends ProblemSummary {
  inputDesc: string;
  outputDesc: string;
  example: string;
  notes: string[];
  conventions: string[];
  starterCode: Record<string, string>;
}

export interface CaseResult {
  name: string;
  passed: boolean;
  input: string;
  expected: string;
  got: string;
  error: string;
}

export interface TargetResult {
  target: string;
  status: "PASS" | "FAIL" | "STUB" | "ERROR" | "MISSING" | "RAN";
  note: string;
  cases: CaseResult[];
  passed: number;
  total: number;
}

export interface SubmitReport {
  ok: boolean;
  problemId: string;
  compileError: {
    type: string;
    message: string;
    line: number | null;
    offset: number | null;
    text: string;
    traceback?: string;
  } | null;
  stdout: string;
  targets: TargetResult[];
  elapsedMs: number;
  untested?: boolean;
  summary: {
    verdict: Verdict;
    passed: number;
    total: number;
    targetCount: number;
  };
}
