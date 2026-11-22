#!/usr/bin/env python3
"""Local stdio MCP: parameterless, bounded scientific actions; no shell parser."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
ACTIONS={'run_density_primary':'primary','run_density_replication':'replication',
         'audit_density_primary':'audit-primary','audit_density_pair':'audit-pair'}


def tool_list():
    tools=[]
    for name,mode in ACTIONS.items():
        tools.append(dict(name=name,description='Execute the fixed local density action '+mode+
            '. No arguments. The code supplies and records all scientific parameters. Never overwrites existing evidence.',
            inputSchema={'type':'object','properties':{},'additionalProperties':False},
            annotations={'readOnlyHint':False,'destructiveHint':False,'idempotentHint':False,'openWorldHint':False}))
    tools.append(dict(name='health',description='Read local bridge health and repository access without running research.',
        inputSchema={'type':'object','properties':{},'additionalProperties':False},
        annotations={'readOnlyHint':True,'destructiveHint':False,'idempotentHint':True,'openWorldHint':False}))
    return tools


def call(name,arguments):
    if arguments:raise ValueError('These actions take no arguments; the protocol is fixed in versioned code')
    if name=='health':
        return {'content':[{'type':'text','text':json.dumps({'status':'READY','repo_access':(ROOT/'AGENTS.md').is_file(),
                    'pinned_scientific_python_configured':bool(os.environ.get('PASQAL_PYTHON'))})}],'isError':False}
    if name not in ACTIONS:raise ValueError('Unknown scientific action')
    python=os.environ.get('PASQAL_PYTHON')
    if not python:raise ValueError('Use the controlled project launcher; PASQAL_PYTHON is required')
    command=[python,str(ROOT/'scripts/qwen_density_job.py'),ACTIONS[name]]
    # The nested scientific runner enforces its 300-second process-group cap.
    result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=340,check=False)
    text=json.dumps({'action':name,'exit_code':result.returncode,'stdout':result.stdout,
                     'stderr':result.stderr},ensure_ascii=False)
    return {'content':[{'type':'text','text':text}],'isError':result.returncode!=0}


def handle(request):
    method=request.get('method');params=request.get('params',{})
    if method=='initialize':
        return {'protocolVersion':params.get('protocolVersion','2024-11-05'),
                'capabilities':{'tools':{'listChanged':False}},
                'serverInfo':{'name':'pasqal-local-research-actions','version':'1.0.0'}}
    if method=='ping':return {}
    if method=='tools/list':return {'tools':tool_list()}
    if method=='tools/call':return call(params.get('name'),params.get('arguments',{}))
    raise ValueError('Unsupported MCP method')


def main():
    # This is a request server, not an autonomous experiment loop. EOF ends it.
    for line in sys.stdin:
        request=None
        try:
            request=json.loads(line)
            if 'id' not in request:continue
            result=handle(request)
            response={'jsonrpc':'2.0','id':request['id'],'result':result}
        except Exception as error:
            if request is None or 'id' not in request:continue
            if request.get('method')=='tools/call':
                response={'jsonrpc':'2.0','id':request['id'],'result':{
                    'content':[{'type':'text','text':type(error).__name__+': '+str(error)}],'isError':True}}
            else:response={'jsonrpc':'2.0','id':request['id'],'error':{'code':-32602,'message':str(error)}}
        print(json.dumps(response,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
