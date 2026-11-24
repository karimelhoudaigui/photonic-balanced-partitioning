"""Publication provenance, exact graph controls, rational choices and corruption."""
import csv
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('publication_build',ROOT/'scripts/build_publication.py')
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)


def archive_root():
    # Test input fallback is explicit and confined to the local evidence archive.
    # Once integrated, all inputs are present under ROOT and no fallback is used.
    import os
    value=os.environ.get('PBP_PUBLICATION_ARCHIVE_ROOT')
    return Path(value).resolve() if value else ROOT

@pytest.fixture(scope='module')
def published_copy(tmp_path_factory):
    root=tmp_path_factory.mktemp('publication-copy');archive=archive_root()
    for logical in (*m.INPUTS,m.GENERATOR):
        source=m.resolve(ROOT,archive,logical);target=root/logical;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    manifest=m.build(root)
    return root,manifest


def test_graph_minima_count_bitstrings_including_complements():
    rows={r['label']:r for r in m.graph_rows()}
    assert rows['K4']['optimum']==4 and rows['K4']['optimal_strings']==6
    assert rows['K22']['optimum']==2 and rows['K22']['optimal_strings']==4
    assert {r['haar_denominator'] for r in rows.values()}=={10}
    assert rows['Path']['optimum']==1 and rows['Path']['optimal_strings']==2


def test_counts_and_seven_method_table_are_derived(published_copy):
    root,manifest=published_copy
    summary=json.loads((root/f'{m.VALIDATED}/summary.json').read_text())
    loss=json.loads((root/f'{m.LOSS}/data/raw.json').read_text())
    with (root/f'{m.VALIDATED}/benchmark.csv').open() as f:count=sum(1 for _ in csv.DictReader(f))
    expected=dict(ErunCount=count,SourceProbabilityCount=sum(len(c['values']) for c in loss['grid']),SourceBracketCount=len(loss['transitions']))
    assert manifest['counts']==expected
    macros=(root/m.OUTPUTS[0]).read_text()
    for key,value in expected.items():assert rf'\providecommand{{\{key}}}{{{value}}}' in macros
    table=(root/m.OUTPUTS[2]).read_text()
    methods={(g['model'],g['lambda_value']) for g in summary['e05b']['groups']}
    assert len(methods)==7
    assert table.count('Product Bernoulli penalty')==sum(model=='classical_penalty' for model,lam in methods)
    assert 'graph-cluster' in table and 'No hardware shots' in table
    assert r'\\[' not in table  # TeX would parse a length argument after the line break.
    assert r'\\{[' in table


def test_fraction_selection_preserves_ties_and_tiny_differences():
    rows=[]
    encode=lambda value:dict(numerator=str(value.numerator),denominator=str(value.denominator))
    for eta in (Fraction(3,4),Fraction(9,10),Fraction(99,100),Fraction(1)):
        rows.append(dict(m=8,eta=encode(eta),values=[dict(source=6,probability=encode(Fraction(1,3)),per_photon=encode(Fraction(1,4))),
                     dict(source=7,probability=encode(Fraction(1,3)+Fraction(1,10**30)),per_photon=encode(Fraction(1,4)))],
                     per_attempt_maximizers=[7],per_photon_maximizers=[6,7]))
    chosen=m.loss_rows(dict(grid=rows))
    assert all(r['per_attempt']==[7] and r['per_photon']==[6,7] for r in chosen)


@pytest.mark.parametrize('logical',[m.GENERATOR,*m.OUTPUTS,*(f'{m.VALIDATED}/{name}' for name in ('summary.json','benchmark.csv','campaigns.json','source_hashes.json')),f'{m.LOSS}/data/raw.json',f'{m.DENSITY}/primary/data/raw.json'])
def test_check_detects_changed_generator_inputs_tables_and_figures(published_copy,logical):
    root,_=published_copy;path=root/logical;original=path.read_bytes()
    try:
        path.write_bytes(original+b'\n% intentional corruption\n')
        with pytest.raises(m.PublicationError,match='SHA mismatch'):m.check(root)
    finally:path.write_bytes(original)
    m.check(root)


def test_pdf_metadata_and_build_are_deterministic(published_copy):
    root,first=published_copy
    second=m.build(root)
    assert first==second
    assert all((root/r['path']).read_bytes().startswith(b'%PDF-') for r in second['outputs'] if r['path'].endswith('.pdf'))
    assert all(r['path'].startswith(m.DENSITY) for r in second['inputs'] if 'P33_' in r['path'])
    assert second['pdf_metadata']['CreationDate']==second['pdf_metadata']['ModDate']
