"""
The course layer: manifest loading, theory parsing, and the lesson routes.

The parsing tests matter more than they look. `theory.md` contains 315 code
fences full of Python comments, so a scanner that is not fence-aware reads `#
build the heap` as a heading -- one module appeared to have 21 titles that way.
And lesson ids are slugs rather than positions specifically so that inserting a
section does not silently reset everybody's progress; there is a test for that.
"""

from __future__ import annotations

import pytest

from app import content


# ------------------------------------------------------------------ parsing

def test_headings_inside_code_fences_are_not_lessons():
    markdown = """# Module title

Intro prose.

## 1. First Section

```python
# this is a comment, not a heading
## neither is this
def f():
    pass
```

Body after the code.

## 2. Second Section

Done.
"""
    intro, lessons = content.parse_theory(markdown)
    assert [l.title for l in lessons] == ["First Section", "Second Section"]
    assert "Intro prose." in intro
    assert "# this is a comment" in lessons[0].body


def test_slug_ignores_the_section_number():
    """
    Inserting a section must not change the ids of the ones after it.

    Position-based ids would shift every lesson and orphan every completion row.
    """
    first = content.parse_theory("## 3. The Two Core Operations\n\nx\n")[1][0]
    later = content.parse_theory("## 9. The Two Core Operations\n\nx\n")[1][0]
    assert first.slug == later.slug == "the-two-core-operations"


def test_title_has_markdown_stripped():
    lessons = content.parse_theory("## 5. Python's `heapq` and **more**\n\nx\n")[1]
    assert lessons[0].title == "Python's heapq and more"


def test_trailing_horizontal_rule_is_dropped():
    lessons = content.parse_theory("## 1. A\n\nbody\n\n---\n\n## 2. B\n\nmore\n")[1]
    assert not lessons[0].body.rstrip().endswith("---")
    assert lessons[0].body.strip() == "body"


def test_reading_time_counts_code_separately():
    """Prose-only counting put "1 min" on lessons that are mostly code."""
    prose = "## A\n\n" + ("word " * 190) + "\n"
    code = "## B\n\n```python\n" + ("x = 1\n" * 110) + "```\n"
    prose_lesson = content.parse_theory(prose)[1][0]
    code_lesson = content.parse_theory(code)[1][0]
    assert prose_lesson.minutes == 1
    assert code_lesson.words == 0
    assert code_lesson.minutes >= 8, "110 lines of code is not a one-minute read"


def test_comment_only_code_lines_do_not_inflate_the_estimate():
    body = "## A\n\n```python\n" + ("# just a comment\n" * 60) + "```\n"
    lesson = content.parse_theory(body)[1][0]
    assert lesson.code_lines == 0


def test_slugify_is_stable_and_url_safe():
    assert content.slugify("  7) Heapify: Building a Heap in O(n) ") \
        == "heapify-building-a-heap-in-o-n"
    assert content.slugify("###") == "section"


# ------------------------------------------------------------ the real course

def test_the_dsa_course_loads():
    course = content.get("dsa")
    assert course is not None
    assert len(course.modules) == 22
    assert sum(len(m.lessons) for m in course.modules) > 200
    assert all(m.title for m in course.modules)
    assert all(m.level for m in course.modules)


def test_every_lesson_has_a_unique_id_within_its_module():
    """A duplicate slug would make two lessons share one completion row."""
    course = content.get("dsa")
    for module in course.modules:
        slugs = [l.slug for l in module.lessons]
        assert len(slugs) == len(set(slugs)), f"module {module.id} has duplicates"


def test_neighbours_cross_module_boundaries():
    course = content.get("dsa")
    first = course.modules[0]
    last_of_first = first.lessons[-1].slug
    hop = content.neighbours("dsa", first.id, last_of_first)
    assert hop["next"] is not None
    assert hop["next"]["moduleId"] == course.modules[1].id


def test_the_first_lesson_has_no_previous():
    course = content.get("dsa")
    start = content.neighbours("dsa", course.modules[0].id,
                               course.modules[0].lessons[0].slug)
    assert start["prev"] is None


# -------------------------------------------------------------------- routes

def test_course_list_is_public(client):
    body = client.get("/api/courses").json()
    assert any(c["id"] == "dsa" for c in body)
    dsa = next(c for c in body if c["id"] == "dsa")
    assert dsa["lessonCount"] > 200
    assert dsa["lessonsRead"] == 0          # signed out


def test_lesson_body_is_served(client):
    res = client.get("/api/courses/dsa/modules/19/lessons/the-two-core-operations")
    assert res.status_code == 200
    lesson = res.json()
    assert "sift_up" in lesson["body"]
    assert lesson["moduleId"] == "19"
    assert lesson["completed"] is False
    assert lesson["next"]["slug"]


def test_unknown_course_and_lesson_404(client):
    assert client.get("/api/courses/nope").status_code == 404
    assert client.get("/api/courses/dsa/modules/99").status_code == 404
    assert client.get(
        "/api/courses/dsa/modules/19/lessons/not-a-lesson").status_code == 404


def test_marking_a_lesson_needs_an_account(client):
    res = client.post(
        "/api/courses/dsa/modules/19/lessons/the-structure/done", json={"done": True})
    assert res.status_code == 401


def test_marking_a_lesson_updates_the_counts(account):
    client, _, _ = account
    res = client.post(
        "/api/courses/dsa/modules/19/lessons/the-structure/done", json={"done": True})
    assert res.status_code == 200
    assert res.json()["moduleLessonsRead"] == 1
    assert res.json()["courseLessonsRead"] == 1

    # Idempotent: marking twice is not two rows.
    client.post("/api/courses/dsa/modules/19/lessons/the-structure/done",
                json={"done": True})
    assert client.get("/api/courses/dsa").json()["lessonsRead"] == 1

    off = client.post("/api/courses/dsa/modules/19/lessons/the-structure/done",
                      json={"done": False})
    assert off.json()["courseLessonsRead"] == 0


def test_resume_points_at_the_first_unread_lesson(account):
    client, _, _ = account
    course = client.get("/api/courses/dsa").json()
    first = course["resume"]
    assert first is not None

    client.post(f"/api/courses/dsa/modules/{first['moduleId']}"
                f"/lessons/{first['slug']}/done", json={"done": True})
    moved = client.get("/api/courses/dsa").json()["resume"]
    assert moved["slug"] != first["slug"], "resume should advance past what was read"


def test_module_page_carries_its_practice_problems(account):
    client, _, _ = account
    module = client.get("/api/courses/dsa/modules/19").json()
    assert module["problemTotal"] > 0
    assert len(module["practice"]) == module["problemTotal"]
    assert all("status" in p for p in module["practice"]), \
        "problems must be decorated with per-user state"


def test_lesson_progress_is_per_account(client):
    a = {"email": "reader-a@example.com", "password": "first reader here"}
    b = {"email": "reader-b@example.com", "password": "second reader here"}
    client.post("/api/auth/register", json=a)
    client.post("/api/courses/dsa/modules/19/lessons/the-structure/done",
                json={"done": True})
    client.post("/api/auth/logout")

    client.post("/api/auth/register", json=b)
    assert client.get("/api/courses/dsa").json()["lessonsRead"] == 0


def test_deleting_an_account_removes_its_lesson_progress(account):
    from app import db, store
    client, email, _ = account
    user_id = store.user_by_email(email)["id"]
    client.post("/api/courses/dsa/modules/19/lessons/the-structure/done",
                json={"done": True})
    assert store.completed_lessons(user_id, "dsa")

    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    assert db.query_all(
        "SELECT * FROM lesson_progress WHERE user_id = ?", (user_id,)) == []


def test_running_examples_needs_an_account(client):
    assert client.post("/api/courses/dsa/modules/19/examples").status_code == 401


def test_a_module_without_examples_says_so(account):
    """No examples file must be a clear 404, not an empty success."""
    client, _, _ = account
    res = client.post("/api/courses/dsa/modules/99/examples")
    assert res.status_code == 404
