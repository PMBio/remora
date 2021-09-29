""" Test main module.
"""
from pathlib import Path
import pytest
from subprocess import check_call

pytestmark = pytest.mark.main

MODELS_DIR = Path(__file__).absolute().parent.parent / "models"
MODEL_PATHS = [
    model_path
    for model_path in MODELS_DIR.iterdir()
    if str(model_path).endswith(".py")
]


@pytest.mark.unit
def test_help():
    check_call(["remora", "-h"])


@pytest.mark.unit
def test_prep_can(can_chunks):
    print(can_chunks)


@pytest.mark.unit
def test_prep_mod(mod_chunks):
    print(mod_chunks)


@pytest.mark.parametrize("model_path", MODEL_PATHS)
def test_train_mod(model_path, tmpdir_factory, mod_chunks, train_cli_args):
    """Run `train_model` on the command line."""
    print(f"Running command line `remora train_model` with model {model_path}")
    out_dir = tmpdir_factory.mktemp("remora_tests") / "train_mod_model"
    print(f"Output file: {out_dir}")
    check_call(
        [
            "remora",
            "train_model",
            "--dataset-path",
            str(mod_chunks),
            "--output-path",
            str(out_dir),
            "--model",
            model_path,
            *train_cli_args,
        ],
    )
    return out_dir


@pytest.mark.unit
def test_mod_infer(tmpdir_factory, mod_tai_map_sig, fw_model_checkpoint):
    out_dir = tmpdir_factory.mktemp("remora_tests") / "mod_infer"
    check_call(
        [
            "remora",
            "infer",
            mod_tai_map_sig,
            fw_model_checkpoint,
            "--full",
            "--batch-size",
            "100",
            "--output-path",
            out_dir,
        ],
    )


@pytest.mark.unit
def test_can_infer(tmpdir_factory, can_tai_map_sig, fw_model_checkpoint):
    out_dir = tmpdir_factory.mktemp("remora_tests") / "can_infer"
    check_call(
        [
            "remora",
            "infer",
            can_tai_map_sig,
            fw_model_checkpoint,
            "--full",
            "--batch-size",
            "100",
            "--output-path",
            out_dir,
        ],
    )


@pytest.mark.unit
def test_chunk_infer(tmpdir_factory, mod_chunks, fw_model_checkpoint):
    out_dir = tmpdir_factory.mktemp("remora_tests") / "chunk_infer"
    check_call(
        [
            "remora",
            "infer",
            str(mod_chunks),
            fw_model_checkpoint,
            "--batch-size",
            "100",
            "--output-path",
            out_dir,
        ],
    )
