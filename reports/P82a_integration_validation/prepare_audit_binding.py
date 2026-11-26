"""Assemble opaque sealed inputs; leave the recorded audit unauthorized."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FINAL_CONTRACT = "research/P82a_independent_audit_execution_contract.json"
BINDING = "research/P82a_independent_audit_dataset_binding.json"
PRIMARY_MANIFEST = "experiments/P82a_dev_veto/run_001/manifest.json"
DATASET = "experiments/P82a_dev_veto/run_001/data"
CHECKER_SHA = "f595fcaea18dee10b7c89982c2ef700cadca417ec8b2ff63557e95b0e9ba9529"


def load(relative):
    return json.loads((ROOT / relative).read_text())


def regular(relative):
    candidate = Path(relative)
    assert not candidate.is_absolute() and ".." not in candidate.parts
    current = ROOT
    for part in candidate.parts:
        current = current / part
        assert not current.is_symlink()
    assert current.is_file() and current.resolve().is_relative_to(ROOT)
    return current


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(relative, value):
    with (ROOT / relative).open("x") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def prepare():
    assert not (ROOT / FINAL_CONTRACT).exists() and not (ROOT / BINDING).exists()
    assert sha(regular("research/P82a_independent_raw_audit.py")) == CHECKER_SHA
    primary = load(PRIMARY_MANIFEST)
    qualification_path = "research/P82a_independent_audit_preflight/run_002/manifest.json"
    qualification = load(qualification_path)
    for record in (primary, qualification):
        assert record["run"]["status"] == "completed" and record["run"]["exit_status"] == 0
        assert all(check["passed"] for check in record["checks"])
        for item in record["input_artifacts"]:
            assert sha(regular(item["path"])) == item["sha256"] == item["sha256_after"]
        for item in record["outputs"]:
            assert sha(regular(item["path"])) == item["sha256"]
    assert primary["repository"]["commit"] == "39b61bb9289cab7439ca15a4aa79d265b068f6f9"
    template = load("research/P82a_independent_audit_main_TEMPLATE.json")
    additions = [FINAL_CONTRACT, PRIMARY_MANIFEST, qualification_path,
        "research/P82a_INDEPENDENT_AUDIT_QUALIFICATION_RECEIPT.md",
        "research/P82a_CHECKER_INDEPENDENT_SOURCE_REVIEW.md",
        "research/P82a_CHECKER_PATH_CORRECTION_REVIEW.md",
        "research/P82a_independent_audit_preflight/run_001/prelaunch_rejection.json",
        "reports/P82a_integration_validation/prepare_audit_binding.py"]
    additions += [item["path"] for item in primary["outputs"]]
    additions += [item["path"] for item in qualification["outputs"]]
    inputs = list(dict.fromkeys(template["execution_artifacts"] + additions))
    assert BINDING in inputs
    for relative in inputs:
        if relative not in (FINAL_CONTRACT, BINDING):
            regular(relative)
    final = deepcopy(template)
    final["binding_state"] = "POST_SEAL_INPUTS_PREPARED_CHECKER_GUARD_STILL_CLOSED"
    final["execution_artifacts"] = inputs
    final["mathematics"]["inputs"][0] = "Opaque sealed primary manifest/results and qualified checker input hashes; actual repeated input closure below"
    final["resource_note"] = "Prepared opaque postseal binding only. The separate dataset binding remains unauthorized until ROOT review. CPU30/wall60/env1/no native backend/log4MiB/output512KiB/raw32MiB/logical256MiB PLAN/zero automatic retries. No behavior, tolerance or scientific setting changed."
    write_new(FINAL_CONTRACT, final)
    binding = deepcopy(load("research/P82a_independent_audit_spec.json")["main_binding"])
    binding.update(binding_state="SEALED_POST_B_RAW_REVIEW_PENDING", b_raw_sealed=True,
                   audit_authorized=False, checker_source_sha256=CHECKER_SHA,
                   producer_execution_commit=primary["repository"]["commit"], dataset_directory=DATASET)
    aliases = {PRIMARY_MANIFEST: "producer_manifest"}
    for item in primary["outputs"]:
        if Path(item["path"]).parent.as_posix() == DATASET:
            aliases[item["path"]] = Path(item["path"]).name
    binding["artifacts"] = [{"name": aliases.get(relative, relative), "path": relative,
                              "sha256": sha(regular(relative)), "bytes": regular(relative).stat().st_size}
                             for relative in inputs if relative != BINDING]
    assert len({item["name"] for item in binding["artifacts"]}) == len(binding["artifacts"])
    write_new(BINDING, binding)
    print(json.dumps({"state": binding["binding_state"], "audit_authorized": False,
                      "runner_input_count": len(inputs), "opaque_records": len(binding["artifacts"]),
                      "contract_sha256": sha(ROOT / FINAL_CONTRACT), "binding_sha256": sha(ROOT / BINDING),
                      "scientific_execution": False}))


if __name__ == "__main__":
    prepare()
