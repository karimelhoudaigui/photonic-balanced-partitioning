"""Prepare pending opaque P90a audit metadata only after the original raw seal."""
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
RAW_SEAL = "d3962d5b846a9905d061d8eb28cf2d0876b0ba00"
BINDING = "research/P90a_independent_audit_dataset_binding.json"
CONTRACT = "research/P90a_independent_audit_execution_contract.json"
PRIMARY = "experiments/P90a_dev_veto/run_001/manifest.json"
PRIMARY_QUAL = "research/P90a_dev_veto_preflight/run_001/manifest.json"
CHECKER_QUAL = "research/P90a_independent_audit_preflight/run_001/manifest.json"
CHECKER_SOURCE_SHA = "609959307bbddfb08ac70b71e714e81df962c2c0d615b56aed20a970cf46a62a"


def project_file(relative):
    p = Path(relative)
    assert not p.is_absolute() and p.parts and ".." not in p.parts
    current = ROOT
    for part in p.parts:
        current /= part
        assert not current.is_symlink()
    assert current.is_file() and current.resolve().is_relative_to(ROOT)
    return current


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1048576), b""):
            h.update(block)
    return h.hexdigest()


def descriptor(relative):
    path = project_file(relative)
    return {"name": relative, "path": relative, "sha256": digest(path), "bytes": path.stat().st_size}


def write_new(relative, content):
    with (ROOT/relative).open("x") as stream:
        json.dump(content, stream, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    assert not (ROOT/BINDING).exists() and not (ROOT/CONTRACT).exists()
    template = json.loads(project_file("research/P90a_independent_audit_main_TEMPLATE.json").read_text())
    assert digest(project_file("research/P90a_independent_raw_audit.py")) == CHECKER_SOURCE_SHA
    paths = list(template["execution_artifacts"])
    manifests = {}
    for relative in (PRIMARY, PRIMARY_QUAL, CHECKER_QUAL):
        # Read only manifest metadata, never decoded B/graph/control records.
        manifest = json.loads(project_file(relative).read_text())
        manifests[relative] = manifest
        paths.append(relative)
        paths.extend(row["path"] for row in manifest["input_artifacts"])
        paths.extend(row["path"] for row in manifest["outputs"])
        for row in manifest["input_artifacts"]:
            assert digest(project_file(row["path"])) == row["sha256"] == row["sha256_after"]
        for row in manifest["outputs"]:
            assert digest(project_file(row["path"])) == row["sha256"]
    assert manifests[PRIMARY]["repository"] == {"commit": "b2f9af31af86c83d8aef8841891c4d37832c69e5", "dirty": False}
    for relative in [PRIMARY]+[row["path"] for row in manifests[PRIMARY]["outputs"]]:
        assert subprocess.check_output(["git", "-C", str(ROOT), "show", RAW_SEAL+":"+relative]) == project_file(relative).read_bytes()
    paths += [
        "research/P90a_PRIMARY_MAIN_RECEIPT.md", "research/P90a_QUALIFICATION_RECEIPT.md",
        "research/P90a_INDEPENDENT_AUDIT_QUALIFICATION_RECEIPT.md",
        "research/P90a_INDEPENDENT_CODE_REVIEW.md", "research/P90a_CHECKER_INDEPENDENT_SOURCE_REVIEW.md",
        "reports/P90a_ROOT_MAIN_AUTHORIZATION.md", "reports/P90a_ROOT_QUALIFICATION_AUTHORIZATION.md",
        "reports/P90a_CHECKER_ROOT_QUALIFICATION_AUTHORIZATION.md", "reports/P90a_ROOT_QUALIFICATION_CHECKPOINT.md",
        "reports/P90a_CHECKER_ROOT_QUALIFICATION_CHECKPOINT.md", "reports/P90a_ROOT_PRE_DATA_SOURCE_REVIEW.md",
        "reports/P90a_CHECKER_ROOT_PRE_DATA_REVIEW.md",
        "reports/P90a_integration_validation/recorded_qualification_inspection.json",
        "reports/P90a_integration_validation/checker_recorded_qualification_inspection.json",
        "reports/P90a_integration_validation/checker_metadata_reader_failure.json",
        "reports/P90a_integration_validation/prepare_recorded_audit.py"]
    paths = list(dict.fromkeys(paths))
    output = Path("research/P90a_independent_audit_main/run_001/data")
    assert not (ROOT/output.parent).exists()
    assert all(not Path(p).is_relative_to(output) and not output.is_relative_to(Path(p)) for p in paths)
    contract = dict(template)
    contract["binding_state"] = "SEALED_CONTRACT_REQUIRES_SEPARATE_ROOT_AUTHORIZATION"
    contract["producer_raw_seal_commit"] = RAW_SEAL
    contract["execution_artifacts"] = paths+[CONTRACT, BINDING]
    write_new(CONTRACT, contract)
    binding = {"binding_state": "SEALED_POST_B_PENDING_ROOT_AUTHORIZATION", "b_raw_sealed": True,
        "audit_authorized": False, "producer_source_freeze": "82d7b63d35f2f0495df6ed9c0d86999b649c44ff",
        "producer_execution_commit": "b2f9af31af86c83d8aef8841891c4d37832c69e5",
        "producer_raw_seal_commit": RAW_SEAL, "producer_manifest": PRIMARY,
        "producer_qualification_manifest": PRIMARY_QUAL, "checker_qualification_manifest": CHECKER_QUAL,
        "dataset_directory": "experiments/P90a_dev_veto/run_001/data", "checker_source_sha256": CHECKER_SOURCE_SHA,
        "audit_output_directory": str(output), "artifacts": [descriptor(p) for p in paths+[CONTRACT]]}
    write_new(BINDING, binding)
    print(json.dumps({"state": binding["binding_state"], "repeated_input_count": len(contract["execution_artifacts"]),
        "opaque_artifacts": len(binding["artifacts"]), "contract_sha256": digest(ROOT/CONTRACT),
        "pending_binding_sha256": digest(ROOT/BINDING), "native_calls": 0, "data_replay": False}))
