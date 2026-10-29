import os
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(__file__))
sys.modules.setdefault('litellm', types.ModuleType('litellm'))
rocketchat_api = types.ModuleType('rocketchat_API')
rocketchat_api.rocketchat = types.SimpleNamespace(RocketChat=object)
sys.modules.setdefault('rocketchat_API', rocketchat_api)
sys.modules.setdefault('rocketchat_API.rocketchat', rocketchat_api.rocketchat)

from common import (
    CodexJudgeError,
    codex_judge,
    evaluate_chat_history_with_llm,
    evaluate_with_llm,
    grader,
)


class CodexJudgeTest(unittest.TestCase):
    @staticmethod
    def completed(stdout='{"type":"turn.completed"}\n'):
        return types.SimpleNamespace(returncode=0, stdout=stdout, stderr='')

    def test_missing_model_fails_clearly(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(CodexJudgeError) as raised:
                codex_judge('Judge this.')
        self.assertEqual(raised.exception.code, 'configuration_missing')

    def test_uses_configured_model_and_reads_schema_constrained_answer(self):
        def run(command, **kwargs):
            output_path = command[command.index('-o') + 1]
            with open(output_path, 'w', encoding='utf-8') as output:
                output.write('{"answer":"yes"}')
            return self.completed()

        with patch.dict(os.environ, {'CODEX_JUDGE_MODEL': 'configured-luna'}), \
                patch('common.subprocess.run', side_effect=run) as run_mock:
            self.assertTrue(codex_judge('Does this satisfy the predicate?'))

        self.assertIn('--model', run_mock.call_args.args[0])
        self.assertEqual(
            run_mock.call_args.args[0][run_mock.call_args.args[0].index('--model') + 1],
            'configured-luna',
        )
        command = run_mock.call_args.args[0]
        self.assertLess(command.index('--ask-for-approval'), command.index('exec'))
        self.assertIn('--skip-git-repo-check', command)
        for feature in ('shell_tool', 'apps', 'browser_use', 'computer_use', 'multi_agent', 'code_mode_host'):
            self.assertIn(feature, command)
        self.assertEqual(run_mock.call_args.kwargs['input'], 'Does this satisfy the predicate?')

    def test_nonzero_exit_fails_clearly(self):
        with patch.dict(os.environ, {'CODEX_JUDGE_MODEL': 'configured-luna'}), \
                patch('common.subprocess.run', return_value=types.SimpleNamespace(
                    returncode=2, stdout='', stderr='sensitive process detail')):
            with self.assertRaises(CodexJudgeError) as raised:
                codex_judge('Judge this.')
        self.assertEqual(raised.exception.code, 'process_exit')
        self.assertIsInstance(raised.exception.__cause__, subprocess.CalledProcessError)
        self.assertNotIn('sensitive process detail', str(raised.exception))

    def test_timeout_preserves_cause(self):
        timeout = subprocess.TimeoutExpired('codex', 1)
        with patch.dict(os.environ, {'CODEX_JUDGE_MODEL': 'configured-luna'}), \
                patch('common.subprocess.run', side_effect=timeout):
            with self.assertRaises(CodexJudgeError) as raised:
                codex_judge('Judge this.')
        self.assertEqual(raised.exception.code, 'timeout')
        self.assertIs(raised.exception.__cause__, timeout)

    def test_failed_terminal_event_rejects_valid_result_file(self):
        def run(command, **kwargs):
            with open(command[command.index('-o') + 1], 'w', encoding='utf-8') as output:
                output.write('{"answer":"yes"}')
            return self.completed('{"type":"turn.failed","error":{"message":"sensitive"}}\n')

        with patch.dict(os.environ, {'CODEX_JUDGE_MODEL': 'configured-luna'}), \
                patch('common.subprocess.run', side_effect=run):
            with self.assertRaises(CodexJudgeError) as raised:
                codex_judge('Judge this.')
        self.assertEqual(raised.exception.code, 'turn_failed')
        self.assertNotIn('sensitive', str(raised.exception))

    def test_malformed_jsonl_is_a_protocol_error(self):
        with patch.dict(os.environ, {'CODEX_JUDGE_MODEL': 'configured-luna'}), \
                patch('common.subprocess.run', return_value=self.completed('not json\n')):
            with self.assertRaises(CodexJudgeError) as raised:
                codex_judge('Judge this.')
        self.assertEqual(raised.exception.code, 'invalid_event_stream')

    def test_schema_violation_fails_instead_of_becoming_a_negative_judgment(self):
        def run(command, **kwargs):
            with open(command[command.index('-o') + 1], 'w', encoding='utf-8') as output:
                output.write('{"answer":"yes","unexpected":true}')
            return self.completed()

        with patch.dict(os.environ, {'CODEX_JUDGE_MODEL': 'configured-luna'}), \
                patch('common.subprocess.run', side_effect=run):
            with self.assertRaises(CodexJudgeError) as raised:
                codex_judge('Judge this.')
        self.assertEqual(raised.exception.code, 'invalid_result')

    def test_grader_does_not_turn_codex_failure_into_a_zero_score(self):
        @grader
        def failing_grader():
            raise CodexJudgeError('process_exit', 'correlation-id')

        with self.assertRaises(CodexJudgeError) as raised:
            failing_grader()
        self.assertEqual(raised.exception.correlation_id, 'correlation-id')

    def test_image_is_passed_as_cli_attachment(self):
        with tempfile.NamedTemporaryFile() as image:
            def run(command, **kwargs):
                with open(command[command.index('-o') + 1], 'w', encoding='utf-8') as output:
                    output.write('{"answer":"no"}')
                return self.completed()

            with patch.dict(os.environ, {'CODEX_JUDGE_MODEL': 'configured-luna'}), \
                    patch('common.subprocess.run', side_effect=run) as run_mock:
                self.assertFalse(codex_judge('Judge image.', image.name))

        command = run_mock.call_args.args[0]
        self.assertEqual(command[command.index('--image') + 1], image.name)

    def test_evaluate_with_llm_propagates_failure_through_grader(self):
        @grader
        def graded_predicate():
            return evaluate_with_llm('evidence', 'the evidence satisfies the predicate')

        with patch.dict(os.environ, {'CODEX_JUDGE_MODEL': 'configured-luna'}), \
                patch('common.subprocess.run', return_value=self.completed(
                    '{"type":"error","message":"sensitive diagnostic"}\n')):
            with self.assertRaises(CodexJudgeError) as raised:
                graded_predicate()
        self.assertEqual(raised.exception.code, 'error')

    def test_evaluate_with_llm_returns_yes_through_grader(self):
        @grader
        def graded_predicate():
            return evaluate_with_llm('evidence', 'the evidence satisfies the predicate')

        def run(command, **kwargs):
            with open(command[command.index('-o') + 1], 'w', encoding='utf-8') as output:
                output.write('{"answer":"yes"}')
            return self.completed()

        with patch.dict(os.environ, {'CODEX_JUDGE_MODEL': 'configured-luna'}), \
                patch('common.subprocess.run', side_effect=run):
            self.assertTrue(graded_predicate())

    def test_chat_history_judge_failure_propagates_through_grader(self):
        @grader
        def graded_chat_predicate():
            return evaluate_chat_history_with_llm(object(), 'reviewer', 'the chat satisfies the predicate')

        with patch.dict(os.environ, {'CODEX_JUDGE_MODEL': 'configured-luna'}), \
                patch('common.get_rocketchat_personal_chat_history', return_value=['evidence']), \
                patch('common.subprocess.run', return_value=self.completed(
                    '{"type":"turn.failed","error":{"message":"private detail"}}\n')):
            with self.assertRaises(CodexJudgeError) as raised:
                graded_chat_predicate()
        self.assertEqual(raised.exception.code, 'turn_failed')


if __name__ == '__main__':
    unittest.main()
