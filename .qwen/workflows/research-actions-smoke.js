export const meta={name:'Local typed-action smoke test',description:'One native agent calls only the local read-only health action.'};
const result=await agent('Call mcp__research__health exactly once with empty arguments {}. Return only its actual response. Do not run a scientific experiment.',
  {agentType:'experiment-runner',label:'typed-action-health',tools:['mcp__research__health'],stallMs:0});
return {status:result===null?'INCONCLUSIVE':'EXECUTED_PENDING_ASTRA_REVIEW',result};
