/** Per-account settings. Stored server-side; defaults when signed out. */
export interface Preferences {
  language: string;
}

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
  runtime: string;
  available: boolean;
  /** Why it is unavailable, or which runtime satisfied it. */
  detail: string;
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
  /** Can this problem's tests be serialised for a non-Python runner? */
  portable: boolean;
  /** Languages that can grade THIS problem. Python is always present. */
  languages: string[];
  /** Progressive unlocking: locked until its module opens. */
  locked: boolean;
  lockedReason: string | null;
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
  /** Per-target explanations of why a language is unavailable here. */
  languageNotes: string[];
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

export interface Learning {
  courses: { id: string; title: string; lessonsRead: number; lessonCount: number }[];
  next: {
    courseId: string; courseTitle: string; moduleId: string;
    moduleTitle: string; slug: string; title: string; minutes: number;
  } | null;
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
  learning: Learning;
}


/* ------------------------------------------------------------------ courses */

export interface LessonSummary {
  slug: string;
  title: string;
  ordinal: number;
  minutes: number;
  words: number;
  codeBlocks: number;
  codeLines: number;
  completed?: boolean;
}

export interface LessonDetail extends LessonSummary {
  body: string;                 // raw markdown, rendered client-side
  completed: boolean;
  courseId: string;
  courseTitle: string;
  moduleId: string;
  moduleTitle: string;
  moduleLessonCount: number;
  prev: { moduleId: string; slug: string; title: string } | null;
  next: { moduleId: string; slug: string; title: string } | null;
}

export interface ModuleSummary {
  id: string;
  title: string;
  level: string;
  intro: string;
  lessonCount: number;
  minutes: number;
  hasExamples: boolean;
  hasProject: boolean;
  lessonsRead: number;
  problemTotal: number;
  problemsSolved: number;
  unlocked: boolean;
  lockedReason: string | null;
}

export interface ModuleDetail extends ModuleSummary {
  lessons: LessonSummary[];
  practice: ProblemSummary[];
  courseId: string;
  courseTitle: string;
  prevModule: string | null;
  nextModule: string | null;
}

export interface CourseSummary {
  id: string;
  title: string;
  subtitle: string;
  language: string;
  levels: string[];
  moduleCount: number;
  lessonCount: number;
  minutes: number;
  practiceLanguages: string[];
  lessonsRead: number;
  lessonTotal?: number;
  problemTotal?: number;
  problemsSolved?: number;
}

export interface Progression {
  enabled: boolean;
  rule: { requireLessons: number; requireProblems: number };
  modulesUnlocked: number;
  moduleCount: number;
}

export interface CourseDetail extends CourseSummary {
  modules: ModuleSummary[];
  progression: Progression;
  resume: {
    moduleId: string; moduleTitle: string; slug: string;
    title: string; ordinal: number; minutes: number;
  } | null;
}
