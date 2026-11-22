export const meta={name:'Local typed-action smoke test',description:'One native agent calls only the local read-only health action.'};
const result=await agent('First call mcp__research__health exactly once with empty arguments {}. Then finish by calling structured_output with {"observed":"the actual response text"}. No further tool calls or scientific experiment.',
  {agentType:'experiment-runner',label:'typed-action-health',tools:['mcp__research__health'],stallMs:0,
   schema:{type:'object',properties:{observed:{type:'string'}},required:['observed'],additionalProperties:false}});
return {status:result===null?'INCONCLUSIVE':'EXECUTED_PENDING_ASTRA_REVIEW',result};
