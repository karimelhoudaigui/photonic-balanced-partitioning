export const meta={name:'Local typed-action smoke test',description:'One native agent calls only the local read-only health action.'};
const result=await agent('Call mcp__research__health exactly once with empty arguments {}. After its result, finish with one plain sentence describing what you actually observed. Do not output JSON or make any more tool calls. No scientific experiment.',
  {agentType:'experiment-runner',label:'typed-action-health',tools:['mcp__research__health'],stallMs:0});
return {status:result===null?'INCONCLUSIVE':'EXECUTED_PENDING_ASTRA_REVIEW',result};
