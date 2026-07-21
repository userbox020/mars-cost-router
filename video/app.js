(() => {
  const fps = 30, duration = 180;
  const cue = [
    [0,15,"When every delegated task gets the premium lane, the decision is easy—but the policy is invisible. Mars Cost Router makes that decision explicit, bounded, and reviewable."],
    [15,35,"Mars Cost Router is an independent, instruction-driven delegation policy for Codex. Mars is our project brand, not a model, and this project is unofficial: it is not affiliated with or endorsed by OpenAI."],
    [35,55,"The policy has three lanes. Economy is for bounded inspection. Balanced is for focused implementation, tests, and review. Premium is for risk, uncertainty, security boundaries, or difficult debugging."],
    [55,75,"Install it from the marketplace repository, add the named plugin, then start a new Codex session. Open it through the plugin browser or at-sign surface. Where skills are exposed, use the Mars Cost Router skill syntax."],
    [75,100,"There is no hidden runtime hook here. The skill and policy guide the root agent. The root writes the child request with an explicit model, reasoning effort, and no inherited turns. The root still owns scope, integration, and final verification."],
    [100,120,"Here is the requested payload shape: a generic task name, a self-contained message, the selected model and effort, and fork turns set to none. This request is not proof of the child’s effective route."],
    [120,140,"For a fixed synthetic read-only series, the selective Terra and Sol policy and the all-Sol high baseline each passed twelve of twelve deterministic checks, with zero observed retries and reroutes."],
    [140,160,"Child-token totals were nearly flat: three hundred fifty-six thousand one hundred sixteen versus three hundred fifty-six thousand four hundred ninety-four, a recorded minus zero point one one percent. Most of the recorded total difference occurred at the root. Total tokens and median wall time are shown neutrally, not as a savings or quality claim."],
    [160,170,"The suite is order- and cache-confounded. It does not prove causality, general quality, billing outcomes, or effective routing."],
    [170,180,"Choose a lane by risk and effort, keep the child task bounded, and verify at the root. Read the policy, evidence, and privacy notes before using it."]
  ];
  const q = new URLSearchParams(location.search), frame = q.has('frame') ? Number(q.get('frame')) : null;
  const maxFrame = duration * fps - 1;
  const normalizeFrame = n => Number.isFinite(n) ? Math.max(0, Math.min(maxFrame, Math.trunc(n))) : 0;
  let currentFrame = frame === null ? 0 : normalizeFrame(frame);
  let t = currentFrame / fps;
  const $ = s => document.querySelector(s), esc = s => s.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
  const time = n => `${String(Math.floor(n/60)).padStart(2,'0')}:${String(Math.floor(n%60)).padStart(2,'0')}`;
  function hero(){return `<div class="hero"><div class="hero-copy"><div class="eyebrow">Instruction-driven delegation policy</div><h1 class="title">Route by risk.<br><span class="accent">Verify</span> at the root.</h1><p class="lede">A deliberate policy for bounded child delegation.</p><div class="hero-words"><b>EXPLICIT</b><b>BOUNDED</b><b>REVIEWABLE</b></div></div><div class="hero-art"><img src="../assets/brand/mars-cost-router-hero.svg" alt="Three deliberate routes meeting at a verified root"></div></div>`}
  function identity(){return `<div class="independent"><div class="eyebrow">A clear boundary</div><h1 class="title">Independent.<br>Instruction-driven.<br><span class="accent">Unofficial.</span></h1><p class="legal"><strong>Mars is this project’s brand, not a model.</strong><br>This project is not affiliated with or endorsed by OpenAI.</p><div class="pill">A policy, not a control plane</div></div>`}
  function lanes(){let active=t<41.67?'economy':t<48.34?'balanced':'premium';return `<div class="lanes"><div class="eyebrow">Three deliberate lanes / use labels, not color alone</div><div class="lane economy ${active==='economy'?'active':''}"><strong>Economy</strong><span>bounded inspection, lookup, low-risk checks</span><small>gpt-5.6-terra</small><small>low · none</small></div><div class="lane balanced ${active==='balanced'?'active':''}"><strong>Balanced</strong><span>focused implementation, tests, documentation, review</span><small>gpt-5.6-terra</small><small>medium · none</small></div><div class="lane premium ${active==='premium'?'active':''}"><strong>Premium</strong><span>risk, uncertainty, security boundaries, difficult debugging</span><small>gpt-5.6-sol</small><small>high · none</small></div></div>`}
  function terminal(){const commands=['codex plugin marketplace add userbox020/mars-cost-router','codex plugin add mars-cost-router@mars-plugins']; let elapsed=t-55, chars=Math.max(0,Math.min(commands.join('\n').length,Math.floor(elapsed*7)));let typed=commands.join('\n').slice(0,chars);return `<div class="terminal"><div class="terminal-top"><span class="dots"><i></i><i></i><i></i></span> SANITIZED INSTALLATION / COMMANDS ONLY</div><pre><span class="prompt">$ </span>${esc(typed).replace('\n','\n<span class="prompt">$ </span>')}<span class="cursor"></span></pre><div class="terminal-note">THEN: START A NEW CODEX SESSION · OPEN PLUGIN BROWSER OR @ SURFACE · $mars-cost-router WHERE SKILLS ARE EXPOSED</div></div>`}
  function flow(){return `<div class="flow"><div class="flow-copy"><div class="eyebrow">Scope stays visible</div><h1 class="nohook">NO HIDDEN<br><span class="accent">RUNTIME HOOK</span></h1><p class="lede">The skill and policy guide the root agent. The root remains responsible.</p><div class="check">Explicit model · reasoning effort · <b>fork_turns: "none"</b><br>Scope · integration · final verification</div></div><img src="../assets/diagrams/delegation-flow.svg" alt="Policy informs root; root makes bounded child calls and verifies results"></div>`}
  function payload(){return `<div class="payload-wrap"><div><div class="eyebrow">Sanitized child request shape</div><div class="payload">{
  <span class="key">"task_name"</span>: <span class="value">"focused_check"</span>,
  <span class="key">"message"</span>: <span class="value">"Inspect one bounded area. Return findings only. Do not delegate or spawn another agent."</span>,
  <span class="key">"model"</span>: <span class="value">"gpt-5.6-terra"</span>,
  <span class="key">"reasoning_effort"</span>: <span class="value">"medium"</span>,
  <span class="key">"fork_turns"</span>: <span class="value">"none"</span>
}</div></div><div class="requested"><div class="eyebrow">Boundary</div><h2>REQUESTED<br><span class="accent">≠</span> EFFECTIVE</h2><p>Fields are explicit requests. This request is not proof of the child’s effective route.</p></div></div>`}
  function evidence(){let stage=t<126.67?1:t<133.34?2:3;return `<div class="evidence"><img src="../assets/evidence/fixed-v1.2-performance.svg" alt="Fixed v1.2 descriptive comparison"><div class="record"><span class="descriptive">DESCRIPTIVE FIXED-SUITE RECORD</span><h2>Observe.<br>Do not overclaim.</h2><div class="stat"><b>12 / 12 · 12 / 12</b>deterministic checks</div>${stage>1?'<div class="stat"><b>0 · 0</b>observed retries · observed reroutes</div>':''}${stage>2?'<div class="stat"><b>356,116 vs 356,494</b>child tokens · −0.11% recorded</div>':''}</div></div>`}
  function record(){return `<div class="evidence"><img src="../assets/evidence/fixed-v1.2-performance.svg" alt="Fixed v1.2 descriptive comparison"><div class="record"><span class="descriptive">NEUTRAL OBSERVATIONS</span><h2>Read the<br>whole record.</h2><div class="stat"><b>Child totals nearly flat</b>−0.11% recorded</div><div class="stat"><b>Most recorded total difference occurred at root</b>Total: 728,706 vs 768,912</div><div class="stat"><b>Median wall</b>45.094 s vs 53.328 s</div></div></div>`}
  function caveat(){return `<div class="caveat"><div class="eyebrow">Evidence boundary</div><h1>Order- and<br>cache-confounded.</h1><p>Not causal. Not general-quality, billing, savings, or effective-routing proof.</p></div>`}
  function outro(){return `<div class="outro"><div><div class="eyebrow">Mars Cost Router</div><h1>Choose a lane.<br>Keep it bounded.<br><span class="accent">Verify at the root.</span></h1><div class="links"><span>READ POLICY</span><span>READ EVIDENCE</span><span>READ PRIVACY NOTES</span></div></div><img src="../assets/brand/mars-cost-router-hero.svg" alt="Mars Cost Router routes meeting at root"></div>`}
  function view(){if(t<15)return hero();if(t<35)return identity();if(t<55)return lanes();if(t<75)return terminal();if(t<100)return flow();if(t<120)return payload();if(t<140)return evidence();if(t<160)return record();if(t<170)return caveat();return outro()}
  const clamp=(n,min=0,max=1)=>Math.max(min,Math.min(max,n));
  const ease=n=>{n=clamp(n);return n*n*(3-2*n)};
  const style=(selector,opacity,y=0,x=0,scale=1)=>{const el=document.querySelector(selector);if(el){el.style.opacity=opacity.toFixed(3);el.style.transform=`translate(${x.toFixed(2)}px,${y.toFixed(2)}px) scale(${scale.toFixed(4)})`}};
  const captionMotion=(opacity,y=0)=>{const el=$('#caption');if(el){el.style.opacity=opacity.toFixed(3);el.style.transform=`translate(-50%,${y.toFixed(2)}px)`}};
  function applyMotion(c){
    const local=t-c[0], span=c[1]-c[0], enter=ease(local/.72), exit=ease((span-local)/.72), presence=Math.min(enter,exit);
    const drift=Math.sin(t*.42), slow=Math.sin(t*.17);
    $('#scene').style.opacity=presence.toFixed(3); $('#scene').style.transform=`translateY(${((1-enter)*18-(1-exit)*8).toFixed(2)}px)`;
    $('#planet').style.transform=`translate(${(slow*22+t*.32).toFixed(2)}px,${(drift*12-t*.12).toFixed(2)}px) scale(${(1.0+Math.sin(t*.11)*.012).toFixed(4)})`;
    $('#stars').style.transform=`translate(${(-t*.12).toFixed(2)}px,${(Math.sin(t*.18)*5).toFixed(2)}px)`;
    captionMotion(presence,(1-enter)*10);
    const scene=cue.indexOf(c);
    if(scene===0){style('.hero-copy',ease((local-.08)/.7),18*(1-ease((local-.08)/.7)));style('.hero-art',ease((local-.28)/.8),-18*(1-ease((local-.28)/.8)),10*Math.sin(t*.4),.985+.015*ease((local-.28)/.8));}
    if(scene===1)style('.independent',ease((local-.12)/.8),28*(1-ease((local-.12)/.8)),0,.985+.015*ease((local-.12)/.8));
    if(scene===2)document.querySelectorAll('.lane').forEach((el,i)=>{const a=ease((local-.22-i*.28)/.48);el.style.opacity=a.toFixed(3);el.style.transform=`translateX(${(1-a)*-28+(el.classList.contains('active')?18:0)}px)`});
    if(scene===3){const a=ease((local-.15)/.55);style('.terminal',a,22*(1-a),0,.99+.01*a);const cursor=document.querySelector('.cursor');if(cursor)cursor.style.opacity=(Math.floor(t*2)%2?'.2':'1');}
    if(scene===4){const a=ease((local-.12)/.7);style('.flow-copy',a,24*(1-a));style('.flow img',ease((local-.38)/.8),-12*(1-ease((local-.38)/.8)),14*(1-ease((local-.38)/.8)),.98+.02*ease((local-.38)/.8));}
    if(scene===5){const a=ease((local-.12)/.65);style('.payload-wrap>div:first-child',a,18*(1-a));style('.requested',ease((local-.42)/.7),18*(1-ease((local-.42)/.7)),0,.985+.015*ease((local-.42)/.7));}
    if(scene===6||scene===7){const a=ease((local-.12)/.7);style('.evidence img',a,18*(1-a),-10*(1-a),.98+.02*a);style('.record',ease((local-.34)/.7),18*(1-ease((local-.34)/.7)),0,.985+.015*ease((local-.34)/.7));}
    if(scene===8)style('.caveat',ease((local-.1)/.8),22*(1-ease((local-.1)/.8)),0,.985+.015*ease((local-.1)/.8));
    if(scene===9){style('.outro>div',ease((local-.1)/.7),20*(1-ease((local-.1)/.7)));style('.outro img',ease((local-.32)/.8),-14*(1-ease((local-.32)/.8)),10*Math.sin(t*.3),.985+.015*ease((local-.32)/.8));}
  }
  function render(){let c=cue.find(x=>t>=x[0]&&t<x[1])||cue[cue.length-1];$('#scene').innerHTML=view();$('#caption').textContent=c[2];$('#clock').textContent=time(t);$('#frame-number').textContent=`${String(currentFrame).padStart(4,'0')} / 5400`;$('#chapter').textContent=`${String(cue.indexOf(c)+1).padStart(2,'0')} / ${['POLICY','IDENTITY','LANES','INSTALL','FLOW','PAYLOAD','EVIDENCE','RECORD','CAVEAT','OUTRO'][cue.indexOf(c)]}`;if(q.get('clean')==='1')$('#guides').style.display='none';applyMotion(c)}
  window.setFrame=n=>{const requestedFrame=normalizeFrame(Number(n));currentFrame=requestedFrame;t=currentFrame/fps;render();return {frame:currentFrame,time:t}};
  render(); if(frame===null){let start=performance.now();function tick(now){t=Math.min(duration-1/fps,(now-start)/1000);currentFrame=Math.min(maxFrame,Math.floor(t*fps));render();requestAnimationFrame(tick)}requestAnimationFrame(tick)}
})();
