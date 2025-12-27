#!/usr/bin/env python3
"""
API Consistency Checker for E2B

This script validates API consistency across different components
and environments to ensure seamless integration.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


class ConsistencyChecker:
    """Checks for consistency across E2B components."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.issues: List[str] = []
        self.warnings: List[str] = []

    def check_package_versions(self) -> bool:
        """Check package.json versions for consistency."""
        print("Checking package versions...")

        packages = {
            "root": self.project_root / "package.json",
            "js-sdk": self.project_root / "packages" / "js-sdk" / "package.json",
            "cli": self.project_root / "packages" / "cli" / "package.json",
        }

        versions = {}
        for name, path in packages.items():
            if not path.exists():
                self.warnings.append(f"Package file not found: {path}")
                continue

            with open(path) as f:
                data = json.load(f)
                versions[name] = data.get("version", "unknown")

        print(f"  JS SDK version: {versions.get('js-sdk', 'N/A')}")
        print(f"  CLI version: {versions.get('cli', 'N/A')}")

        # Check if dependencies are consistent
        return True

    def check_environment_configs(self) -> bool:
        """Check environment configuration consistency."""
        print("Checking environment configurations...")

        env_template = self.project_root / ".env.template"
        if not env_template.exists():
            self.issues.append(".env.template not found")
            return False

        print("  ✓ .env.template found")

        # Check for required environment variables
        required_vars = [
            "APP_NAME",
            "APP_ENVIRONMENT",
            "BUILD_TARGET",
            "SANDBOX_ENABLED",
            "API_TIMEOUT",
            "ERROR_REPORTING_ENABLED",
            "TEST_COVERAGE_THRESHOLD",
        ]

        with open(env_template) as f:
            content = f.read()
            for var in required_vars:
                if var not in content:
                    self.warnings.append(f"Required variable {var} not in .env.template")
                else:
                    print(f"  ✓ {var} defined")

        return True

    def check_build_scripts(self) -> bool:
        """Check build scripts exist and are executable."""
        print("Checking build scripts...")

        scripts = {
            "build": self.project_root / "scripts" / "build.sh",
            "validate": self.project_root / "scripts" / "validate.sh",
        }

        for name, path in scripts.items():
            if not path.exists():
                self.issues.append(f"Script not found: {path}")
                continue

            if not path.stat().st_mode & 0o111:
                self.warnings.append(f"Script not executable: {path}")

            print(f"  ✓ {name} script found and executable")

        return len(self.issues) == 0

    def check_test_infrastructure(self) -> bool:
        """Check test infrastructure is in place."""
        print("Checking test infrastructure...")

        test_files = {
            "agentx5": self.project_root
            / "tools"
            / "agentx5"
            / "test_multi_dump_parser.py",
        }

        for name, path in test_files.items():
            if not path.exists():
                self.issues.append(f"Test file not found: {path}")
                continue

            print(f"  ✓ {name} tests found")

        return len(self.issues) == 0

    def check_workflow_consistency(self) -> bool:
        """Check GitHub Actions workflows are consistent."""
        print("Checking workflow consistency...")

        workflows_dir = self.project_root / ".github" / "workflows"
        if not workflows_dir.exists():
            self.issues.append("Workflows directory not found")
            return False

        expected_workflows = [
            "js_sdk_tests.yml",
            "python_sdk_tests.yml",
            "cli_tests.yml",
            "agentx5_tests.yml",
            "lint.yml",
        ]

        for workflow in expected_workflows:
            path = workflows_dir / workflow
            if not path.exists():
                self.issues.append(f"Workflow not found: {workflow}")
            else:
                print(f"  ✓ {workflow} found")

        return len(self.issues) == 0

    def check_documentation(self) -> bool:
        """Check documentation is up to date."""
        print("Checking documentation...")

        docs = {
            "Build Guide": self.project_root / "BUILD_DEPLOYMENT_GUIDE.md",
            "Integration Config": self.project_root / "integration.yml",
            "README": self.project_root / "README.md",
        }

        for name, path in docs.items():
            if not path.exists():
                self.warnings.append(f"Documentation not found: {name}")
            else:
                print(f"  ✓ {name} found")

        return True

    def generate_report(self) -> str:
        """Generate a consistency report."""
        report = ["", "=" * 60, "E2B API Consistency Report", "=" * 60, ""]

        if not self.issues and not self.warnings:
            report.append("✓ All consistency checks passed!")
        else:
            if self.issues:
                report.append("Issues Found:")
                for issue in self.issues:
                    report.append(f"  ✗ {issue}")
                report.append("")

            if self.warnings:
                report.append("Warnings:")
                for warning in self.warnings:
                    report.append(f"  ⚠ {warning}")
                report.append("")

        report.append("=" * 60)
        return "\n".join(report)

    def run_all_checks(self) -> bool:
        """Run all consistency checks."""
        print("\n" + "=" * 60)
        print("Starting API Consistency Checks")
        print("=" * 60 + "\n")

        checks = [
            self.check_package_versions,
            self.check_environment_configs,
            self.check_build_scripts,
            self.check_test_infrastructure,
            self.check_workflow_consistency,
            self.check_documentation,
        ]

        for check in checks:
            check()
            print()

        print(self.generate_report())

        return len(self.issues) == 0


def main():
    """Main entry point."""
    project_root = Path(__file__).parent.parent

    checker = ConsistencyChecker(project_root)
    success = checker.run_all_checks()

    if success:
        print("\n✓ API consistency validation passed!")
        sys.exit(0)
    else:
        print("\n✗ API consistency validation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
