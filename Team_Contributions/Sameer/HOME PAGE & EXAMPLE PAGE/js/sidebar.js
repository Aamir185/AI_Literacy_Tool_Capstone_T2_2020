var open = false;

function checkNav(){
  if(open){
    closeNav();
    open=false;
  }else{
    openNav();
    open=true;
  }
}

function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft= "0";
}