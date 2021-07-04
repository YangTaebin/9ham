function sleep(ms) {
  const wakeUpTime = Date.now() + ms;
  while (Date.now() < wakeUpTime) {}
}

function shipmove() {
  var ship = document.getElementsByClassName("ship");
  var n = 0;
  while (true) {
    ship[0].style.marginTop = (100*Math.sin(n)).toString()+"px";
    n = n + 1;
    sleep(1000);
    console.log(ship[0].style.marginTop);
    if(n==100) {
      break;
    }
  }
}
