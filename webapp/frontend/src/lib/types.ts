export interface User {
  id: string;
  email: string;
  name: string;
  createdAt: number;
}

export type Difficulty = "Easy" | "Medium" | "Hard" | "Challenge";

export type Verdict =
  | "accepted" | "failed" | "stub" | "error"
  | "missing" | "untested" | "ran";

/** Where the learner stands on a problem, as the server sees it. */
export type ProblemState = "solved" | "attempted" | "todo";

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
  status: ProblemState;
  attempts: number;
  bookmarked: boolean;
  hasNote: boolean;
}

export interface ProblemDetail extends ProblemSummary {
  inputDesc: string;
  outputDesc: string;
  example: string;
  notes: string[];
  conventions: string[];
  starterCode: Record<string, string>;
  prevId: string | null;
  nextId: string | null;
  submissionCount: number;
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
  submissionId: number | null;
  summary: {
    verdict: Verdict;
    passed: number;
    total: number;
    targetCount: number;
  };
}

export interface Submission {
  id: number;
  problemId: string;
  language: string;
  verdict: Verdict;
  passed: number;
  total: number;
  elapsedMs: number;
  createdAt: number;      // unix seconds
  /** Present only on /api/submissions/{id}, which returns the code too. */
  source?: string;
  /** Joined in by /api/progress for the recent-activity feed. */
  title?: string;
  difficulty?: Difficulty;
  topic?: number;
  topicName?: string;
}

export interface Note {
  problemId: string;
  body: string;
  updatedAt: number | null;
}

export interface ActivityDay {
  date: string;           // YYYY-MM-DD, server-local
  submissions: number;
  solved: number;
}

export interface Activity {
  days: ActivityDay[];
  streak: number;
  longestStreak: number;
  activeDays: number;
  totalSubmissions: number;
}

export interface DifficultyProgress {
  difficulty: Difficulty;
  total: number;
  solved: number;
  attempted: number;
}

export interface TopicProgress {
  topic: number;
  name: string;
  total: number;
  solved: number;
  attempted: number;
  tested: number;
  level: string;
}

export interface Overview {
  totals: { problems: number; solved: number; attempted: number; tested: number };
  byDifficulty: DifficultyProgress[];
  byTopic: TopicProgress[];
  activity: Activity;
  recent: Submission[];
  resume: {
    id: string; title: string; difficulty: Difficulty;
    topic: number; topicName: string; verdict: Verdict; at: number;
  } | null;
  nextUp: {
    id: string; title: string; difficulty: Difficulty;
    topic: number; topicName: string;
  }[];
}
