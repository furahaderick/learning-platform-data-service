-- Completion percentage for every course in which a student is enrolled.
SELECT
    e.student_id,
    e.course_id,
    c.title,
    COALESCE(p.completed_lessons, 0) AS completed_lessons,
    totals.total_lessons,
    CASE
        WHEN totals.total_lessons = 0 THEN 0
        ELSE ROUND(COALESCE(p.completed_lessons, 0) * 100.0
                    / totals.total_lessons, 2)
    END AS completion_percentage
FROM enrollments e
JOIN courses c ON c.id = e.course_id
JOIN (
    SELECT m.course_id, COUNT(l.id) AS total_lessons
    FROM modules m
    JOIN lessons l ON l.module_id = m.id
    GROUP BY m.course_id
) totals ON totals.course_id = e.course_id
LEFT JOIN (
    SELECT lp.student_id, m.course_id, COUNT(*) AS completed_lessons
    FROM lesson_progress lp
    JOIN lessons l ON l.id = lp.lesson_id
    JOIN modules m ON m.id = l.module_id
    GROUP BY lp.student_id, m.course_id
) p ON p.student_id = e.student_id AND p.course_id = e.course_id
ORDER BY e.student_id, e.course_id;

-- Time between consecutive lesson completions for each student.
SELECT
    student_id,
    lesson_id,
    completed_at,
    LAG(completed_at) OVER (
        PARTITION BY student_id ORDER BY completed_at
    ) AS previous_completion,
    completed_at - LAG(completed_at) OVER (
        PARTITION BY student_id ORDER BY completed_at
    ) AS time_since_previous
FROM lesson_progress
ORDER BY student_id, completed_at;

-- Compare the query plan and actual execution time.
EXPLAIN ANALYZE
SELECT lesson_id, completed_at
FROM lesson_progress
WHERE student_id = 1
ORDER BY completed_at DESC;
