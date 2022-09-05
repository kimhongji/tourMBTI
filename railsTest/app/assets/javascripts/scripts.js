/*!
* Start Bootstrap - Freelancer v7.0.6 (https://startbootstrap.com/theme/freelancer)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-freelancer/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 72,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});

function FindTour() {

        var table = document.getElementById('mytable');

        var url = 'http://apis.data.go.kr/B551011/KorService/locationBasedList?serviceKey=zvyVv9%2BUiLc7SY5wYKup3vpZnaUd05Zj4MfgBo4DqQXjTN3180b3bINu1x5CKbLqduyzU5YO%2BIPHXdIJINwjYQ%3D%3D&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=AppTest&mapX='+ xMap + '&mapY=' + yMap + '&radius=1000&listYN=Y&contentTypeId=12';

        // save marker position
        var positions = [];

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function(){
	        if(xhttp.readyState == 4 && xhttp.status == 200) { //file을 읽어들이는데 성공한 경우
		      var xmlDoc = xhttp.responseXML;
	          var titleTag = xmlDoc.getElementsByTagName("title");

	          var tbody = document.getElementsByTagName("tbody")[0];
              while(tbody.rows.length > 0){
                  tbody.deleteRow(0);
              }

              for (i = 0; i < titleTag.length; i++) {
                    /* var title = arr[i].title;
                    var author = arr[i].author;
                    var price = arr[i].price; */

                    var title = xmlDoc.getElementsByTagName("title")[i].innerHTML;
                    var addr = xmlDoc.getElementsByTagName("addr1")[i].innerHTML;

                    positions.push({
                        title: xmlDoc.getElementsByTagName("title")[i].innerHTML,
                        latlng: new kakao.maps.LatLng(xmlDoc.getElementsByTagName("mapy")[i].innerHTML, xmlDoc.getElementsByTagName("mapx")[i].innerHTML)
                    })

                    var thTitle = document.createTextNode(title);
                    var tdAddr = document.createTextNode(addr);
                    var tr = document.createElement("tr");
                    var th = document.createElement("th");
                    var td1 = document.createElement("td");
                    var td2 = document.createElement("td");

                    th.appendChild(thTitle);
                    td1.appendChild(tdAddr);

                    tr.appendChild(th);
                    tr.appendChild(td1);
                    tr.appendChild(td2);

                    tbody.appendChild(tr);

                    console.log("4");

                    }
                }
            }

        xhttp.open("GET", url, false);
        xhttp.send();

        // 마커 이미지의 이미지 주소입니다
        var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png";

        for (var i = 0; i < positions.length; i ++) {

            // 마커 이미지의 이미지 크기 입니다
            var imageSize = new kakao.maps.Size(24, 35);

            // 마커 이미지를 생성합니다
            var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);

            // 마커를 생성합니다
            var newmarker = new kakao.maps.Marker({
                map: map, // 마커를 표시할 지도
                position: positions[i].latlng, // 마커를 표시할 위치
                title : positions[i].title, // 마커의 타이틀, 마커에 마우스를 올리면 타이틀이 표시됩니다
                image : markerImage // 마커 이미지
            });
        }
}
