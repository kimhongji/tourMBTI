/*!
* Start Bootstrap - Freelancer v7.0.6 (https://startbootstrap.com/theme/freelancer)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-freelancer/blob/master/LICENSE)
*/
window.addEventListener("DOMContentLoaded",()=>{var e=function(){const e=document.body.querySelector("#mainNav");e&&(0===window.scrollY?e.classList.remove("navbar-shrink"):e.classList.add("navbar-shrink"))};e(),document.addEventListener("scroll",e),document.body.querySelector("#mainNav")&&new bootstrap.ScrollSpy(document.body,{target:"#mainNav",offset:72});const n=document.body.querySelector(".navbar-toggler");[].slice.call(document.querySelectorAll("#navbarResponsive .nav-link")).map(function(e){e.addEventListener("click",()=>{"none"!==window.getComputedStyle(n).display&&n.click()})})});