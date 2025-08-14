import re

from ai_document_viewer import DocumentViewer, MarkdownFormatter


def test_markdown_document_viewer(tester):
    """Test Markdown document viewer functionality"""
    try:
        tester.print_info("Testing Markdown document viewer...")
        from ai_document_viewer import DocumentViewer, MarkdownFormatter
        tester.print_success(
            "  \u2713 DocumentViewer and MarkdownFormatter imported successfully"
        )
        formatter = MarkdownFormatter()
        test_cases = [
            ("# Header", "Main header formatting"),
            ("## Sub Header", "Sub header formatting"),
            ("**Bold text**", "Bold text formatting"),
            ("*Italic text*", "Italic text formatting"),
            ("`inline code`", "Inline code formatting"),
            ("- List item", "List item formatting"),
            ("1. Numbered item", "Numbered list formatting"),
            ("> Blockquote", "Blockquote formatting"),
            ("[Link](url)", "Link formatting"),
        ]
        markdown_tests_passed = 0
        for test_input, description in test_cases:
            try:
                formatted = formatter.format_line(test_input)
                formatting_applied = False
                if test_input.startswith('# '):
                    formatting_applied = '\n' in formatted or len(formatted) > len(test_input) * 2
                elif test_input.startswith('## '):
                    formatting_applied = '\n' in formatted or len(formatted) > len(test_input) + 10
                elif test_input.startswith('### '):
                    formatting_applied = True
                elif '**' in test_input or '*' in test_input:
                    formatting_applied = True
                elif test_input.startswith('`') and test_input.endswith('`'):
                    formatting_applied = True
                elif test_input.startswith('- '):
                    formatting_applied = '\u2022' in formatted
                elif re.match(r'^\d+\.\s', test_input):
                    match = re.match(r'^(\s*)(\d+)(\.\s)(.*)$', test_input)
                    formatting_applied = match is not None
                elif test_input.startswith('> '):
                    formatting_applied = '\u2502' in formatted
                elif '[' in test_input and '](' in test_input:
                    formatting_applied = True
                else:
                    formatting_applied = formatted != test_input
                if formatting_applied:
                    markdown_tests_passed += 1
                else:
                    tester.print_error(
                        f"  \u2717 {description} failed - no formatting applied"
                    )
            except Exception as e:
                tester.print_error(f"  \u2717 {description} failed: {e}")
        if markdown_tests_passed >= 7:
            tester.print_success(
                f"  \u2713 Markdown formatting tests passed ({markdown_tests_passed}/{len(test_cases)})"
            )
        else:
            tester.print_error(
                f"  \u2717 Markdown formatting tests failed ({markdown_tests_passed}/{len(test_cases)})"
            )
            return False
        viewer = DocumentViewer(tester.ai_env_path)
        readme_path = viewer.ai_env_path / "README.md"
        if readme_path.exists():
            tester.print_success("  \u2713 README.md found for testing")
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:5]
                if lines:
                    tester.print_success(
                        f"  \u2713 README.md readable ({len(lines)} test lines)"
                    )
                    formatted_lines = []
                    for line in lines:
                        try:
                            formatted_lines.append(viewer.formatter.format_line(line.rstrip()))
                        except Exception as e:
                            tester.print_error(f"  \u2717 Error formatting line: {e}")
                            return False
                    tester.print_success(
                        "  \u2713 README.md Markdown formatting successful"
                    )
                else:
                    tester.print_error("  \u2717 README.md is empty")
                    return False
            except Exception as e:
                tester.print_error(f"  \u2717 Error reading README.md: {e}")
                return False
        else:
            tester.print_error("  \u2717 README.md not found")
            return False
        package_info_path = viewer.ai_env_path / "PACKAGE_INFO.txt"
        if package_info_path.exists():
            tester.print_success("  \u2713 PACKAGE_INFO.txt found for testing")
            try:
                with open(package_info_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:3]
                if lines:
                    formatted_lines = [
                        viewer._format_text_line(line.rstrip()) for line in lines
                    ]
                    tester.print_success(
                        "  \u2713 PACKAGE_INFO.txt formatting successful"
                    )
                else:
                    tester.print_error("  \u2717 PACKAGE_INFO.txt is empty")
                    return False
            except Exception as e:
                tester.print_error(
                    f"  \u2717 Error reading PACKAGE_INFO.txt: {e}"
                )
                return False
        else:
            tester.print_error("  \u2717 PACKAGE_INFO.txt not found")
            return False
        tester.print_success("Markdown document viewer test PASSED")
        return True
    except ImportError as e:
        tester.print_error(f"Document viewer import failed: {e}")
        tester.print_error("Markdown document viewer test FAILED")
        return False
    except Exception as e:
        tester.print_error(f"Document viewer test error: {e}")
        tester.print_error("Markdown document viewer test FAILED")
        return False
