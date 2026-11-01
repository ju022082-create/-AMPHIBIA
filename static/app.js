const form=document.querySelector('#form');const hourMode=document.querySelector('#hourMode');const customHour=document.querySelector('#customHour');const error=document.querySelector('#error');
hourMode.addEventListener('change',()=>{customHour.hidden=hourMode.value!=='custom';});
function row(label,value){return `<div class="row"><span>${label}</span><strong class="${value?'on':'off'}">${value?'ON':'OFF'}</strong></div>`;}
function display(data){const t=data.temperature,h=data.humidity,l=data.lighting,w=data.water;
document.querySelector('#hourLabel').textContent=`SIMULATED TIME · ${String(data.hour).padStart(2,'0')}:00 KST`;
document.querySelector('#tempStatus').textContent=t.status;document.querySelector('#humidTarget').textContent=h.target;
document.querySelector('#tempItems').innerHTML=row('Heater',t.heater)+row('Cooler',t.cooler)+row('Circulation fan',t.circulation_fan);
document.querySelector('#humidItems').innerHTML=row('Misting',h.misting)+row('Ventilation fan',h.ventilation_fan);
document.querySelector('#lightItems').innerHTML=row('Plant light',l.plant_light)+row('UVB light',l.uvb_light)+row('Hot-zone light',l.hot_zone_light);
document.querySelector('#waterItems').innerHTML=row('Low water warning',w.low_warning)+row('High water warning',w.high_warning);
const banner=document.querySelector('#banner');banner.className='banner '+(!t.connected?'emergency':w.low_warning||w.high_warning?'warning':'success');banner.textContent=!t.connected?'EMERGENCY · 40°C 이상: 모든 장비 제어 명령 비활성화':w.low_warning||w.high_warning?'WATER ALERT · 수위 경고 발생':'SYSTEM NORMAL · 제어 시뮬레이션 완료';}
form.addEventListener('submit',async e=>{e.preventDefault();error.hidden=true;const f=new FormData(form);const payload={temperature:f.get('temperature'),humidity:f.get('humidity'),water_level:f.get('water_level'),hour:hourMode.value==='custom'?f.get('hour'):null};try{const res=await fetch('/api/simulate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const data=await res.json();if(!res.ok)throw Error(data.error||'Request failed');display(data);}catch(err){error.textContent=err.message;error.hidden=false;}});
document.querySelector('#reset').addEventListener('click',async()=>{await fetch('/api/reset',{method:'POST'});document.querySelector('#banner').className='banner';document.querySelector('#banner').textContent='수위 경고 상태를 초기화했습니다. 다음 시뮬레이션부터 적용됩니다.';});
