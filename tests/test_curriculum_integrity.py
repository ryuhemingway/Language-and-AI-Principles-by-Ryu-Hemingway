import re
import unittest
from pathlib import Path

import learn


def _question_key(question: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", question.lower()).strip()


class CurriculumIntegrityTests(unittest.TestCase):
    def test_operator_answers_do_not_collapse_to_empty_matches(self):
        self.assertTrue(learn._answer_matches("&", ["&", "and"]))
        self.assertTrue(learn._answer_matches("the & operator", ["&", "and"]))
        self.assertFalse(learn._answer_matches("%", ["&", "and"]))

        self.assertTrue(learn._answer_matches(">>>", [">>>", "unsigned right shift"]))
        self.assertFalse(learn._answer_matches("???", [">>>", "unsigned right shift"]))

    def test_ai_quiz_questions_are_unique_after_normalization(self):
        seen = {}
        for module in learn.AI_MODULES:
            for lesson in learn._ai_curriculum(module):
                question = lesson["quiz"][0]
                key = _question_key(question)
                previous = seen.get(key)
                self.assertIsNone(
                    previous,
                    f"duplicate AI quiz question {question!r} in {module} lesson {lesson['day']} "
                    f"and {previous}",
                )
                seen[key] = f"{module} lesson {lesson['day']}"

    def test_thin_ai_modules_have_audit_appendices(self):
        for module in ("locallm", "mlops", "safety"):
            with self.subTest(module=module):
                self.assertGreaterEqual(len(learn.AI_AUDIT_APPENDIX.get(module, [])), 3)
                self.assertGreaterEqual(len(learn._ai_curriculum(module)), 7)

    def test_ai_teach_view_does_not_repeat_fundamentals_as_key_ideas(self):
        lesson = learn._ai_curriculum("prompting")[0]
        view = learn._ai_lesson_view("prompting", lesson)

        self.assertNotIn("Key ideas:", view["teach"])

    def test_ai_lesson_view_uses_concept_check_not_coding_prompt(self):
        lesson = learn._ai_curriculum("rag")[0]
        view = learn._ai_lesson_view("rag", lesson)

        self.assertEqual(view["next_stage_label"], "concept check")
        self.assertEqual(view["concept_prompt"], "When is RAG a better choice than prompting alone?")
        self.assertNotIn("Sketch", view["concept_prompt"])
        self.assertNotIn("Coding problem", view["concept_prompt"])

    def test_legacy_mapped_language_course_is_not_tracked(self):
        legacy_course = "cs" + "5008"
        removed_language = "c-" + legacy_course
        removed_label = "C - " + legacy_course.upper() + " Mapped"
        self.assertNotIn(removed_language, learn.LEARN_LANGUAGES)
        self.assertNotIn(removed_label, learn.LEARN_LANGUAGES.values())
        self.assertFalse(hasattr(learn, legacy_course.upper() + "_TOPIC_ORDER"))
        self.assertFalse(hasattr(learn, legacy_course.upper() + "_MODULE_BY_TOPIC"))

    def test_c_review_lessons_have_examples(self):
        c_examples = learn.AUDIT_EXAMPLE_SNIPPETS["c"]
        for topic in ("c_integration_review", "c_correctness_invariants"):
            with self.subTest(topic=topic):
                self.assertIn(topic, c_examples)
                self.assertGreater(len(c_examples[topic].strip()), 20)

    def test_core_starter_hints_cover_first_six_topics_all_languages(self):
        topics = ("variables", "types", "input", "conditionals", "loops", "functions")
        languages = ("python", "c", "java")

        for topic in topics:
            for language in languages:
                with self.subTest(topic=topic, language=language):
                    self.assertIn((topic, language), learn.CODE_STARTER_HINTS)

    def test_offline_ai_review_rejects_placeholder_response(self):
        lesson = next(item for item in learn._ai_curriculum("safety") if item["title"] == "Prompt injection defenses")
        view = learn._ai_lesson_view("safety", lesson)

        lines, passed = learn._offline_submission_review(view, "todo not sure placeholder")

        self.assertFalse(passed)
        self.assertIn("Needs revision:", lines[0])

    def test_offline_ai_review_accepts_concrete_response(self):
        lesson = next(item for item in learn._ai_curriculum("safety") if item["title"] == "Prompt injection defenses")
        view = learn._ai_lesson_view("safety", lesson)
        submission = (
            "Retrieved content is untrusted evidence, so I would quote it separately from system rules, "
            "validate tool arguments, and use permission scopes before any tool call."
        )

        lines, passed = learn._offline_submission_review(view, submission)

        self.assertTrue(passed)
        self.assertIn("Promising offline check:", lines[0])

    def test_sanitize_intel_cleans_placeholders_recursively(self):
        data = {
            "ai_demand": {"shifts": "not_specified"},
            "job_market": {"trend": "not specified"},
            "research": [{"title": "ok", "url": "not_specified"}],
        }

        cleaned = learn._sanitize_intel(data)

        self.assertEqual(cleaned["ai_demand"]["shifts"], "--")
        self.assertEqual(cleaned["job_market"]["trend"], "--")
        self.assertEqual(cleaned["research"][0]["url"], "--")

    def test_deepseek_models_are_normalized_from_config_and_progress(self):
        cfg = {"deepseek_model": "deepseek-chat"}
        self.assertEqual(learn._apply_progress_models(cfg, {})["deepseek_model"], "deepseek-v4-flash")

        blank_cfg = {"deepseek_model": ""}
        self.assertEqual(learn._apply_progress_models(blank_cfg, {})["deepseek_model"], "deepseek-v4-flash")

        progress = {"deepseek_model": "deepseek-reasoner"}
        self.assertEqual(learn._apply_progress_models({}, progress)["deepseek_model"], "deepseek-v4-flash")

    def test_parse_json_response_prefers_final_correct_payload_and_spaced_fence(self):
        raw = (
            "Example first:\n``` json\n{\"demo\": true}\n```\n"
            "Final answer:\n``` json\n{\"correct\": false, \"feedback\": \"try again\"}\n```"
        )

        parsed = learn._parse_json_response(raw)

        self.assertEqual(parsed, {"correct": False, "feedback": "try again"})

    def test_output_patterns_cover_common_alternatives_without_false_print_words(self):
        self.assertTrue(learn._has_any("sys.stdout.write('ok')", learn._output_patterns("python")))
        self.assertTrue(learn._has_any("logging.info('ok')", learn._output_patterns("python")))
        self.assertFalse(learn._has_any("blueprint = 'plan'", learn._output_patterns("python")))
        self.assertTrue(learn._has_any('puts("ok");', learn._output_patterns("c")))
        self.assertTrue(learn._has_any('fprintf(stdout, "ok\\n");', learn._output_patterns("c")))
        self.assertTrue(learn._has_any('System.out.printf("%d", n);', learn._output_patterns("java")))
        self.assertTrue(learn._has_any('System.err.println("bad");', learn._output_patterns("java")))

    def test_audit_followup_hard_checks_accept_valid_common_forms(self):
        cases = [
            (
                {"topic": "hash_maps", "language": "python"},
                "counts = {}\nfor ch in text:\n    counts[ch] = counts.get(ch, 0) + 1\nprint(counts)",
            ),
            (
                {"topic": "sliding_window", "language": "python"},
                "window = sum(nums[:k])\nbest = window\nfor right in range(k, len(nums)):\n    window += nums[right]\n    window -= nums[right-k]\n    best = max(best, window)\nprint(best)",
            ),
            (
                {"topic": "heap", "language": "python"},
                "import heapq\nheapq.heapify(nums)\nprint(heapq.heappop(nums))",
            ),
            (
                {"topic": "dynamic_programming", "language": "python"},
                "dp = [0] * (n + 1)\ndp[0] = 0\ndp[1] = 1\nfor i in range(2, n + 1):\n    dp[i] = dp[i-1] + dp[i-2]\nprint(dp[n])",
            ),
            (
                {"topic": "variables", "language": "c"},
                '#include <stdio.h>\nint main(void) {\n    char name[] = "Alex";\n    int age = 21;\n    printf("%s %d\\n", name, age);\n}',
            ),
        ]

        for view, code in cases:
            with self.subTest(topic=view["topic"]):
                passed, feedback = learn._programming_hard_review(view, code)
                self.assertTrue(passed, feedback)

    def test_audit_followup_new_topic_hard_checks(self):
        cases = [
            ("classes", "python", "class Dog:\n    def __init__(self, name):\n        self.name = name\n    def bark(self):\n        print(self.name)"),
            ("c_debug_assembly", "c", "gdb ./app\nbreak main\nrun\nprint i\nbacktrace\ninfo registers\n disassemble"),
            ("c_compilers_linkers", "c", "gcc -c main.c -o main.o\ngcc -c util.c -o util.o\ngcc main.o util.o -o app\nlinker resolves symbols"),
            ("c_processes_memory", "c", "process memory map: text has code, data/BSS has globals, heap has malloc, stack has frames, cache affects locality"),
            ("c_networking_sockets", "c", "int s = socket(AF_INET, SOCK_STREAM, 0);\nbind(s, addr, len);\nlisten(s, 8);\nint c = accept(s, NULL, NULL);\nrecv(c, buf, n, 0);\nsend(c, buf, n, 0);\nclose(c);"),
            ("c_trees_heaps", "c", "struct Node { int value; struct Node *left; struct Node *right; };\nNode *insert(Node *root, int value);\nint heap[16]; // min-heap array"),
            ("java_uml", "java", "UML class diagram: Book has fields and methods; Member composition relationship with Loan; +checkout() public, -id private"),
            ("java_packages_builds", "java", "package app.model;\nimport java.util.List;\n// Gradle build.gradle declares implementation dependency and classpath/JAR layout"),
            ("python_modules_packages_envs", "python", "from pathlib import Path\n# package/__init__.py\n# python -m venv .venv\n# requirements.txt\nif __name__ == \"__main__\":\n    print(Path.cwd())"),
        ]

        for topic, language, code in cases:
            with self.subTest(topic=topic):
                passed, feedback = learn._programming_hard_review({"topic": topic, "language": language}, code)
                self.assertTrue(passed, feedback)

    def test_audit_report_topics_have_deterministic_hard_checks(self):
        topics = {
            "hash_maps", "stack", "two_pointers", "sliding_window", "binary_search", "linked_lists",
            "recursion", "trees", "graphs", "dynamic_programming", "heap", "matrix", "design",
            "classes",
            "python_control_flow_deep", "python_builtin_data_structures", "python_text_processing",
            "python_file_io_data", "python_error_handling", "python_iterators_generators_decorators",
            "python_testing", "python_ai_ml_readiness", "python_modules_packages_envs",
            "c_foundations_headers", "c_structs_types", "c_concurrency_threads", "c_stacks_queues",
            "c_algorithm_analysis_formal", "c_quadratic_sorts", "c_nlogn_sorts_proofs",
            "c_trees_heaps", "c_hash_tables", "c_graph_algorithms", "c_greedy",
            "c_dynamic_programming_deep", "c_recursion_divide_conquer",
            "c_debug_assembly", "c_compilers_linkers", "c_processes_memory", "c_networking_sockets",
            "java_language_foundations", "java_control_flow", "java_methods_contracts",
            "java_enums_exceptions", "java_encapsulation_invariants", "java_abstract_interfaces",
            "java_equality_hashing", "java_generics_hofs", "java_recursive_lists",
            "java_adts_collections", "java_design_patterns", "java_mvc",
            "java_testing_debug_docs", "java_big_o", "java_uml", "java_packages_builds",
        }

        checks = learn._programming_hard_review({"topic": "missing", "language": "python"}, "print('x')")
        self.assertIsNone(checks[0])

        source = Path(learn.__file__).read_text(encoding="utf-8")
        for topic in topics:
            with self.subTest(topic=topic):
                self.assertIn(f'"{topic}": (', source)

    def test_editor_hint_uses_explicit_ctrl_g_not_plain_h(self):
        source = Path(learn.__file__).read_text(encoding="utf-8")

        self.assertIn('@bindings.add("c-g")', source)
        self.assertNotIn('@bindings.add("h")', source)
        self.assertIn("Ctrl+G hint", source)
        self.assertIn("Type :hint on the first line", source)
        self.assertNotIn("Type h on the first line", source)
        self.assertNotIn('stripped.lower() in ("h", "hint", ":hint")', source)


if __name__ == "__main__":
    unittest.main()
