/* The poster is the same orthographic view as the live model. Keep it visible
   until the environment, model and first GPU frame have all finished. */
const mount=document.getElementById('instrument');
const surface=document.getElementById('globe-surface');
const motionQuery=window.matchMedia('(prefers-reduced-motion: reduce)');

async function createWebGLView(){
  const canvas=document.createElement('canvas');
  const attributes={alpha:true,antialias:true,powerPreference:'low-power',premultipliedAlpha:true};
  let context;
  try{context=canvas.getContext('webgl2',attributes)||canvas.getContext('webgl',attributes);}catch{}
  if(!context)throw new Error('webgl-unavailable');
  const [THREE,{GLTFLoader}]=await Promise.all([import('./vendor/three.module.min.js'),import('./vendor/GLTFLoader.js')]);
  const renderer=new THREE.WebGLRenderer({canvas,context,...attributes});
  renderer.setClearColor(0,0);
  renderer.outputColorSpace=THREE.SRGBColorSpace;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure=1.26;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,1.6));
  const scene=new THREE.Scene();
  const envProcessor=new THREE.PMREMGenerator(renderer);
  const [asset,reflection]=await Promise.all([
    new GLTFLoader().loadAsync('/assets/meridian.glb'),
    new THREE.TextureLoader().loadAsync('/assets/studio-reflection.jpg')
  ]);
  reflection.colorSpace=THREE.SRGBColorSpace;
  reflection.mapping=THREE.EquirectangularReflectionMapping;
  const environment=envProcessor.fromEquirectangular(reflection);
  scene.environment=environment.texture;
  reflection.dispose();
  envProcessor.dispose();

  const model=asset.scene;
  scene.add(model);
  const rotor=model.getObjectByName('EarthRotor');
  if(!rotor)throw new Error('The globe is missing its rotating assembly.');
  model.traverse(node=>{
    if(!node.isMesh)return;
    const materials=Array.isArray(node.material)?node.material:[node.material];
    materials.forEach(material=>{material.envMapIntensity=1.6});
  });
  scene.add(new THREE.HemisphereLight(0xf2f7f1,0x5b6d61,1.35));
  const key=new THREE.DirectionalLight(0xfff8ea,2.6);key.position.set(-3.7,5.5,4.5);scene.add(key);
  const rim=new THREE.DirectionalLight(0xd5e7ee,1.65);rim.position.set(3.5,2.8,-3.4);scene.add(rim);
  const camera=new THREE.OrthographicCamera(-1.635,1.635,1.635,-1.635,.1,40);
  camera.position.set(2.5,2.2,8.3);camera.lookAt(0,.073,0);
  const earthInitial=rotor.rotation.y;

  function resizeView(){
    const {width,height}=surface.getBoundingClientRect();
    if(!width||!height)return;
    const span=3.27;
    camera.left=-span*width/height/2;camera.right=-camera.left;
    camera.top=span/2;camera.bottom=-camera.top;camera.updateProjectionMatrix();
    renderer.setSize(width,height,false);
  }
  return {
    mode:'webgl',canvas,resize:resizeView,
    paint(angle,yaw){
      rotor.rotation.y=earthInitial+angle;
      model.rotation.y=yaw;
      renderer.render(scene,camera);
    }
  };
}

/* Software-only devices use the same model and camera, rendered at 10° intervals.
   Interpolating adjacent views keeps drag continuous between the 36 poses. */
async function createTurntableView(){
  const sprite=new Image();
  sprite.src='/assets/meridian-turntable.webp';
  await sprite.decode();
  const count=36, columns=6, width=sprite.width/columns, height=sprite.height/(count/columns);
  const canvas=document.createElement('canvas');
  canvas.width=width;canvas.height=height;
  const ctx=canvas.getContext('2d');
  if(!ctx)throw new Error('canvas-unavailable');
  let lastPosition=null;
  function frame(index){
    const cell=index%count;
    ctx.drawImage(sprite,(cell%columns)*width,Math.floor(cell/columns)*height,width,height,0,0,width,height);
  }
  return {
    mode:'turntable',canvas,resize(){},
    paint(angle){
      const position=((angle/(Math.PI*2)*count)%count+count)%count;
      if(lastPosition!==null&&Math.abs(position-lastPosition)<.003)return;
      lastPosition=position;
      const lower=Math.floor(position);
      ctx.clearRect(0,0,width,height);ctx.globalAlpha=1;frame(lower);
      const blend=position-lower;
      if(blend>.01){ctx.globalAlpha=blend;frame(lower+1);ctx.globalAlpha=1}
      canvas.dataset.frame=String(lower);
    }
  };
}

async function activateGlobe(){
  if(!mount||!surface)return;
  let view;
  try{view=await createWebGLView()}catch{view=await createTurntableView()}
  let visible=true, paused=motionQuery.matches, activePointer=null, lastX=0;
  let pointerStartX=0, pointerStartY=0, dragged=false;
  let spin=motionQuery.matches?0:-.20,targetSpin=0,velocity=0,request=0,previous=0,ready=false;
  let scrollAmount=0,baseYaw=0;
  let dirty=true;
  function setPaused(value){
    paused=value;
    surface.setAttribute('aria-description','Drag or use the left and right arrow keys to turn. Tap or press Space to '+(paused?'resume.':'pause.'));
    previous=0;dirty=true;schedule();
  }
  function schedule(){
    if(!request&&visible&&!document.hidden)request=requestAnimationFrame(draw);
  }
  function draw(time){
    request=0;
    if(!visible||document.hidden)return;
    const elapsed=previous?Math.min((time-previous)/1000,.065):0;
    if(previous&&time-previous<29&&!dirty){schedule();return}
    previous=time;
    if(!paused&&activePointer===null){targetSpin+=elapsed*.115}
    if(activePointer===null&&Math.abs(velocity)>.0001){
      targetSpin+=velocity;
      velocity*=.87;
    }else if(activePointer===null){velocity=0}
    const fraction=1-Math.exp(-Math.max(elapsed,1/60)*12);
    spin+=(targetSpin-spin)*fraction;
    const yawTarget=motionQuery.matches?0:scrollAmount*.21;
    baseYaw+=(yawTarget-baseYaw)*fraction;
    view.paint(spin,baseYaw);
    dirty=false;
    if(!ready){
      ready=true;
      surface.replaceChildren(view.canvas);
      mount.dataset.renderer=view.mode;
      surface.tabIndex=0;
      surface.setAttribute('role','group');
      surface.setAttribute('aria-label','Interactive globe');
      surface.setAttribute('aria-keyshortcuts','ArrowLeft ArrowRight Space');
      setPaused(paused);
    }
    if(!paused||Math.abs(targetSpin-spin)>.0005||Math.abs(yawTarget-baseYaw)>.001||Math.abs(velocity)>.0001)schedule();
  }
  function resize(){view.resize();dirty=true;schedule()}
  new ResizeObserver(resize).observe(surface);
  new IntersectionObserver(entries=>{
    visible=entries[0].isIntersecting;
    if(visible){previous=0;dirty=true;schedule()}else if(request){cancelAnimationFrame(request);request=0}
  },{rootMargin:'85px'}).observe(mount);
  document.addEventListener('visibilitychange',()=>{if(!document.hidden){previous=0;schedule()}});
  function updateScroll(){
    const hero=mount.closest('.film-hero');
    const box=hero.getBoundingClientRect();
    scrollAmount=Math.max(0,Math.min(1,-box.top/box.height));
    if(!motionQuery.matches&&box.bottom>0){
      hero.style.setProperty('--light-shift',Math.round(scrollAmount*75)+'px');
      hero.style.setProperty('--object-shift',Math.round(scrollAmount*45)+'px');
      dirty=true;schedule();
    }
  }
  window.addEventListener('scroll',updateScroll,{passive:true});
  surface.addEventListener('pointerdown',event=>{
    if(!event.isPrimary||event.button!==0)return;
    activePointer=event.pointerId;lastX=pointerStartX=event.clientX;
    pointerStartY=event.clientY;dragged=false;velocity=0;
    surface.setPointerCapture(activePointer);mount.classList.add('dragging');
  });
  surface.addEventListener('pointermove',event=>{
    if(event.pointerId!==activePointer)return;
    if(!dragged){
      dragged=Math.hypot(event.clientX-pointerStartX,event.clientY-pointerStartY)>5;
      if(!dragged)return;
    }
    const step=(event.clientX-lastX)*.014;
    targetSpin+=step;velocity=Math.max(-.075,Math.min(.075,step*.2));
    lastX=event.clientX;dirty=true;schedule();
  });
  function release(){
    activePointer=null;mount.classList.remove('dragging');dirty=true;schedule();
  }
  surface.addEventListener('lostpointercapture',release);
  surface.addEventListener('pointerup',event=>{
    if(event.pointerId!==activePointer)return;
    if(!dragged)setPaused(!paused);
    release();
  });
  surface.addEventListener('pointercancel',release);
  surface.addEventListener('keydown',event=>{
    if(event.key==='ArrowLeft'||event.key==='ArrowRight'){
      event.preventDefault();
      targetSpin+=(event.key==='ArrowLeft'?-1:1)*Math.PI/3;velocity=0;dirty=true;schedule();
    }else if(event.key===' '){
      event.preventDefault();
      if(!event.repeat)setPaused(!paused);
    }
  });
  motionQuery.addEventListener('change',()=>setPaused(motionQuery.matches));
  if(view.mode==='webgl')view.canvas.addEventListener('webglcontextlost',async event=>{
    event.preventDefault();visible=false;ready=false;
    if(request)cancelAnimationFrame(request);request=0;
    mount.removeAttribute('data-renderer');surface.removeAttribute('tabindex');view.canvas.hidden=true;
    try{
      view=await createTurntableView();visible=true;previous=0;dirty=true;resize();
    }catch{mount.dataset.renderer='poster'}
  },{once:true});
  resize();updateScroll();
}
activateGlobe().catch(()=>{
  if(mount)mount.dataset.renderer='poster';
});
