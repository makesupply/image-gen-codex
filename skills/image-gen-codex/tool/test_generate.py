import importlib.util
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).with_name("generate.py")
spec = importlib.util.spec_from_file_location("codex_imagegen", MODULE_PATH)
codex_imagegen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(codex_imagegen)


def valid_rgba_png(width: int, height: int) -> bytes:
    def chunk(chunk_type: bytes, data: bytes) -> bytes:
        checksum = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", checksum)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    scanlines = b"".join(b"\x00" + (b"\x00\x00\x00\xff" * width) for _ in range(height))
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(scanlines))
        + chunk(b"IEND", b"")
    )


class DiscoverCodexTests(unittest.TestCase):
    def test_prefers_explicit_codex_executable(self):
        with tempfile.TemporaryDirectory() as tmp:
            exe = Path(tmp) / "codex.exe"
            exe.write_bytes(b"test")

            found = codex_imagegen.discover_codex(executable=str(exe))

            self.assertEqual(found, exe.resolve())


class SubscriptionGuardTests(unittest.TestCase):
    @mock.patch.object(codex_imagegen.subprocess, "run")
    def test_accepts_chatgpt_login(self, run):
        run.return_value = mock.Mock(returncode=0, stdout="Logged in using ChatGPT\n", stderr="")
        status = codex_imagegen.require_chatgpt_login(Path("codex.exe"))
        self.assertEqual(status, "Logged in using ChatGPT")

    @mock.patch.object(codex_imagegen.subprocess, "run")
    def test_rejects_api_key_login(self, run):
        run.return_value = mock.Mock(returncode=0, stdout="Logged in using API key\n", stderr="")
        with self.assertRaisesRegex(codex_imagegen.BridgeError, "ChatGPT subscription"):
            codex_imagegen.require_chatgpt_login(Path("codex.exe"))


class PromptTests(unittest.TestCase):
    def test_prompt_requires_builtin_imagegen_and_exact_destination(self):
        output = Path(r"D:\project\generated\job\hero.png")
        prompt = codex_imagegen.build_codex_prompt("Create a clean product hero.", output)
        self.assertIn("$imagegen", prompt)
        self.assertIn(str(output), prompt)
        self.assertIn("Do not use the API-key fallback", prompt)
        self.assertIn("RESULT:", prompt)


class PngVerificationTests(unittest.TestCase):
    def test_reads_png_dimensions_without_third_party_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            png = Path(tmp) / "image.png"
            png.write_bytes(valid_rgba_png(512, 768))
            info = codex_imagegen.verify_png(png)
            self.assertEqual(info["width"], 512)
            self.assertEqual(info["height"], 768)

    def test_rejects_non_png_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "image.png"
            bad.write_text("not an image", encoding="utf-8")
            with self.assertRaisesRegex(codex_imagegen.BridgeError, "valid PNG"):
                codex_imagegen.verify_png(bad)

    def test_rejects_truncated_png_with_valid_signature_and_ihdr(self):
        with tempfile.TemporaryDirectory() as tmp:
            truncated = Path(tmp) / "truncated.png"
            truncated.write_bytes(valid_rgba_png(512, 768)[:33])
            with self.assertRaisesRegex(codex_imagegen.BridgeError, "truncated"):
                codex_imagegen.verify_png(truncated)


class OutputPolicyTests(unittest.TestCase):
    def test_accepts_png_below_allowed_subdir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            output = codex_imagegen.resolve_output(root, "generated/smoke/test.png")
            self.assertEqual(output, (root / "generated/smoke/test.png").resolve())

    def test_accepts_custom_allowed_subdir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            output = codex_imagegen.resolve_output(
                root, "assets/out/test.png", allowed_subdir="assets/out"
            )
            self.assertEqual(output, (root / "assets/out/test.png").resolve())

    def test_rejects_output_outside_allowed_subdir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            with self.assertRaisesRegex(codex_imagegen.BridgeError, "generated"):
                codex_imagegen.resolve_output(root, "outside.png")

    def test_refuses_overwrite_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            existing = root / "generated/job/test.png"
            existing.parent.mkdir(parents=True)
            existing.write_bytes(b"old")
            with self.assertRaisesRegex(codex_imagegen.BridgeError, "already exists"):
                codex_imagegen.resolve_output(root, existing, force=False)


class ReferencePolicyTests(unittest.TestCase):
    def test_accepts_project_image_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            reference = root / "assets/product.png"
            reference.parent.mkdir()
            reference.write_bytes(b"image")
            self.assertEqual(
                codex_imagegen.resolve_references(root, [reference]),
                [reference.resolve()],
            )

    def test_rejects_reference_outside_project(self):
        with tempfile.TemporaryDirectory() as project, tempfile.TemporaryDirectory() as other:
            root = Path(project).resolve()
            reference = Path(other) / "private.png"
            reference.write_bytes(b"image")
            with self.assertRaisesRegex(codex_imagegen.BridgeError, "inside the project"):
                codex_imagegen.resolve_references(root, [reference])


class CommandTests(unittest.TestCase):
    def test_attaches_each_reference_image(self):
        command = codex_imagegen.build_command(
            executable=Path("codex.exe"),
            references=[Path("one.png"), Path("two.jpg")],
            last_message=Path("last.txt"),
        )
        self.assertEqual(command.count("-i"), 2)
        self.assertIn("one.png", command)
        self.assertIn("two.jpg", command)
        self.assertIn("--output-last-message", command)

    def test_does_not_place_prompt_after_variadic_image_arguments(self):
        command = codex_imagegen.build_command(
            executable=Path("codex.exe"),
            references=[Path("product.png")],
            last_message=Path("last.txt"),
        )
        self.assertNotIn("Use $imagegen", command)


class RunGenerationTests(unittest.TestCase):
    def test_pipes_prompt_to_codex_stdin(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "generated/job/image.png"
            output.parent.mkdir(parents=True)
            request = "Use $imagegen with this reference"
            with (
                mock.patch.object(
                    codex_imagegen,
                    "require_chatgpt_login",
                    return_value="Logged in using ChatGPT",
                ),
                mock.patch.object(codex_imagegen.subprocess, "run") as run,
                mock.patch.object(
                    codex_imagegen,
                    "verify_png",
                    return_value={"width": 100, "height": 100},
                ),
                mock.patch.object(
                    codex_imagegen,
                    "write_manifest",
                    return_value=output.with_suffix(".manifest.json"),
                ),
            ):
                def successful_codex(command, **_kwargs):
                    last_message = Path(
                        command[command.index("--output-last-message") + 1]
                    )
                    last_message.write_text(f"RESULT: {output}\n", encoding="utf-8")
                    return mock.Mock(returncode=0, stdout="", stderr="")

                run.side_effect = successful_codex
                codex_imagegen.run_generation(
                    root=root,
                    request=request,
                    output=output,
                    references=[root / "product.png"],
                    executable=Path("codex.exe"),
                    timeout=30,
                )

            self.assertEqual(
                run.call_args.kwargs.get("input"),
                codex_imagegen.build_codex_prompt(request, output),
            )

    def test_rejects_result_path_that_does_not_match_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "generated/job/image.png"
            output.parent.mkdir(parents=True)
            with (
                mock.patch.object(
                    codex_imagegen,
                    "require_chatgpt_login",
                    return_value="Logged in using ChatGPT",
                ),
                mock.patch.object(codex_imagegen.subprocess, "run") as run,
                mock.patch.object(
                    codex_imagegen,
                    "verify_png",
                    return_value={"width": 100, "height": 100},
                ),
                mock.patch.object(
                    codex_imagegen,
                    "write_manifest",
                    return_value=output.with_suffix(".manifest.json"),
                ),
            ):
                def wrong_result_codex(command, **_kwargs):
                    last_message = Path(
                        command[command.index("--output-last-message") + 1]
                    )
                    last_message.write_text(
                        f"RESULT: {output.with_name('other.png')}\n",
                        encoding="utf-8",
                    )
                    return mock.Mock(returncode=0, stdout="", stderr="")

                run.side_effect = wrong_result_codex
                with self.assertRaisesRegex(codex_imagegen.BridgeError, "RESULT"):
                    codex_imagegen.run_generation(
                        root=root,
                        request="Use $imagegen",
                        output=output,
                        references=[],
                        executable=Path("codex.exe"),
                        timeout=30,
                    )


class ManifestTests(unittest.TestCase):
    def test_writes_verifiable_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "image.png"
            output.write_bytes(b"png bytes")
            manifest_path = codex_imagegen.write_manifest(
                output=output,
                request="Create a test image",
                references=[root / "ref.png"],
                executable=Path("codex.exe"),
                auth_status="Logged in using ChatGPT",
                png_info={"width": 100, "height": 200},
            )
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["auth"], "Logged in using ChatGPT")
            self.assertEqual(payload["width"], 100)
            self.assertEqual(payload["height"], 200)
            self.assertEqual(len(payload["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
